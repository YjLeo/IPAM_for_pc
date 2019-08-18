// Copyright 2017 CNI authors
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

// This is a sample chained plugin that supports multiple CNI versions. It
// parses prevResult according to the cniVersion
package main

import (
	"bytes"
	"encoding/json"
	"errors"
	"fmt"
	"io/ioutil"
	"log"
	"net"
	//"net"
	"net/http"
	"os"
	"os/exec"
	"strings"
	"time"

	"github.com/containernetworking/cni/pkg/skel"
	"github.com/containernetworking/cni/pkg/types"
	"github.com/containernetworking/cni/pkg/types/current"
	"github.com/containernetworking/cni/pkg/version"
)

const (
	CNIVerion = "0.2.0"

	BinAddPath = "/bin/cni-docker-config"
	BinDelPath = "/bin/cni-docker-config"
)
const defaultBrName = "br0"

////
type Test struct {
	vlan string `json:"vlan"`
}

type NetConf struct {
	types.NetConf
	BrName       string `json:"bridge"`
	IsGW         bool   `json:"isGateway"`
	IsDefaultGW  bool   `json:"isDefaultGateway"`
	ForceAddress bool   `json:"forceAddress"`
	IPMasq       bool   `json:"ipMasq"`
	MTU          int    `json:"mtu"`
	HairpinMode  bool   `json:"hairpinMode"`
	PromiscMode  bool   `json:"promiscMode"`
}

func loadNetConf(bytes []byte) (*NetConf, string, error) {
	n := &NetConf{
		BrName: defaultBrName,
	}
	if err := json.Unmarshal(bytes, n); err != nil {
		return nil, "", fmt.Errorf("failed to load netconf: %v", err)
	}
	return n, n.CNIVersion, nil
}

// PluginConf is whatever you expect your configuration json to be. This is whatever
// is passed in on stdin. Your plugin may wish to expose its functionality via
// runtime args, see CONVENTIONS.md in the CNI spec.
type PluginConf struct {
	types.NetConf // You may wish to not nest this type
	RuntimeConfig *struct {
		SampleConfig map[string]interface{} `json:"sample"`
	} `json:"runtimeConfig"`
	RawPrevResult     *map[string]interface{} `json:"prevResult"`
	PrevResult        *current.Result         `json:"-"`
	MyAwesomeFlag     bool                    `json:"myAwesomeFlag"`
	AnotherAwesomeArg string                  `json:"anotherAwesomeArg"`
}

func parseConfig(stdin []byte) (*PluginConf, error) {
	conf := PluginConf{}

	if err := json.Unmarshal(stdin, &conf); err != nil {
		return nil, fmt.Errorf("failed to parse network configuration: %v", err)
	}

	return &conf, nil
}

// cmdAdd is called for ADD requests
func cmdAdd(args *skel.CmdArgs) error {
	client := &http.Client{}
	var getip string

	file := "/" + "pod_add" + ".txt"

	logFile, err := os.OpenFile(file, os.O_RDWR|os.O_CREATE|os.O_APPEND, 0766)
	if nil != err {
		panic(err)
	}
	loger := log.New(logFile, "k8stest", log.Ldate|log.Ltime|log.Lshortfile)
	args.Path = "/opt/cni/bin"
	contID := args.ContainerID
	ifName := args.IfName
	conf := string(args.StdinData)
	var data map[string]interface{}
	json.Unmarshal([]byte(conf), &data)
	gw := data["gateway"]
	sub := data["subnet"]
	/////////////////////////////////////////////////////
	_, cniVersion, err := loadNetConf(args.StdinData)
	//璇诲彇閰嶇疆
	if err != nil {
		loger.Println(err)
	}
	resp_ip, err := http.Get("http://172.18.3.48:5000/api/v1/get_free_ip/")
	if err != nil {
		return errors.New("IPAMserver connect faild")
		time.Sleep(10000 * time.Millisecond)
		loger.Println("get_ip error ")
		// handle error
	}
	defer resp_ip.Body.Close()

	ip, ioerr := ioutil.ReadAll(resp_ip.Body)
	if ioerr != nil {
		loger.Println("ioutil.read failure")
		// handle error
	}
	if strings.Replace(string(ip), "\n", "", -1) == "null" {
		loger.Println("ip is None")
		time.Sleep(1000 * time.Millisecond)
		return errors.New("IP is None")
	} else {
		getip = strings.Replace(strings.Replace(string(ip), "\n", "", -1), "\"", "", -1)
	}
	loger.Println("ip=" + getip + "&id=" + contID)
	request, _ := http.NewRequest("POST", "http://172.18.3.48:5000/api/v1/map_store/?"+"ip="+getip+"&id="+contID, strings.NewReader(""))
	request.Header.Set("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8")
	resp, resperr := client.Do(request)
	if resperr != nil {
		loger.Println("map_store:post ip error")
	}
	defer resp.Body.Close()
	ipadd := string(strings.Replace(strings.Replace(string(ip), "\n", "", -1), "\"", "", -1) + "/" + sub.(string))
	gateway := gw.(string)
	loger.Println(gateway)
	loger.Println(ipadd)
	cmd := exec.Command(BinAddPath, "add-port", "br0", ifName, contID, "--ipaddress="+ipadd, "--gateway="+gateway)
	var out bytes.Buffer
	var stderr bytes.Buffer
	cmd.Stdout = &out
	cmd.Stderr = &stderr
	if err := cmd.Run(); err != nil {
		loger.Println(stderr.String())
		loger.Println(err)
		loger.Println("cmd run falure")
	}
	loger.Println("cmd done!")
	loger.Println(getip)
	result := &current.Result{
		CNIVersion: CNIVerion,
		IPs: []*current.IPConfig{
			&current.IPConfig{
				Version: "4",
				Address: net.IPNet{
					IP:   net.ParseIP(getip),
					Mask: net.ParseIP("255.255.0.0").DefaultMask(),
				},
			},
		},
	}
	return types.PrintResult(result, cniVersion)
}

// cmdDel is called for DELETE requests
func cmdDel(args *skel.CmdArgs) error {
	client := &http.Client{}
	file := "/" + "pod_del" + ".txt"
	logFile, err := os.OpenFile(file, os.O_RDWR|os.O_CREATE|os.O_APPEND, 0766)
	if nil != err {
		panic(err)
	}
	loger := log.New(logFile, "k8stest", log.Ldate|log.Ltime|log.Lshortfile)
	_, cniVersion, err := loadNetConf(args.StdinData)
	//璇诲彇閰嶇疆
	if err != nil {
		loger.Println(err)
	}
	args.Path = "/opt/cni/bin"
	contID := args.ContainerID
	cmd := exec.Command(BinDelPath, "del-port", "br0", "eth0", args.ContainerID)
	var out bytes.Buffer
	var stderr bytes.Buffer
	cmd.Stdout = &out
	cmd.Stderr = &stderr
	if err := cmd.Run(); err != nil {
		loger.Println(err)
	}
	resp_ip, resperr := http.Get("http://172.18.3.48:5000/api/v1/map_store/?id=" + contID)
	if resperr != nil {
		loger.Println("map_store:get ip error")
	}
	ip, ioerr := ioutil.ReadAll(resp_ip.Body)
	if ioerr != nil {
		loger.Printf("ioutil.read failure")
		// handle error
	}
	defer resp_ip.Body.Close()
	var getip string
	if ip != nil {
		getip := strings.Replace(strings.Replace(string(ip), "\n", "", -1), "\"", "", -1)
		waste, _ := http.NewRequest("POST", "http://172.18.3.48:5000/api/v1/rec_free_ip/?ip="+getip, strings.NewReader(""))
		waste.Header.Set("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8")
		resp, posterr := client.Do(waste)
		if posterr != nil {
			log.Println("rev free_ip error,skip")
			// handle error
		} else {
			loger.Println("del map:store Start ")
		}
		defer resp.Body.Close()
		waste1, _ := http.NewRequest("DELETE", "http://172.18.3.48:5000/api/v1/map_store/?id="+contID, strings.NewReader(""))
		waste1.Header.Set("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8")
		resp1, posterr1 := client.Do(waste1)
		if posterr1 != nil {
			log.Println("del map:store error,Skip")
		} else {
			loger.Println("del map:store Down")
		}
		defer resp1.Body.Close()
	} else {
		getip = "0.0.0.0"
		loger.Println("rev_ip none ,check redis or initied it")
	}

	result := &current.Result{
		CNIVersion: CNIVerion,
		IPs: []*current.IPConfig{
			&current.IPConfig{
				Version: "4",
				Address: net.IPNet{
					IP:   net.ParseIP(getip),
					Mask: net.ParseIP("255.255.0.0").DefaultMask(),
				},
			},
		},
	}
	return types.PrintResult(result, cniVersion)

}

func main() {
	// TODO: implement plugin version
	skel.PluginMain(cmdAdd, cmdGet, cmdDel, version.All, "TODO")
}

func cmdGet(args *skel.CmdArgs) error {
	// TODO: implement
	return fmt.Errorf("not implemented")
}

