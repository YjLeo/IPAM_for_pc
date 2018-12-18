#!/usr/bin/python
#-*- coding: utf-8 -*-

import jenkins
import pcPython.pcGroup.util.JsonResultUtil as JsonResultUtil

class jenkinsUtil():
    '''
        :param url : jenkins链点
        :param username :  jenkins  用户名
        :param passwd :  jenkins 登录密码
    '''
    def __init__(self , url , username = "liaowenjie" , passwd = "liaowenjie"):
        self.url = url
        self.username = username
        self.passwd = passwd
        self.server = jenkins.Jenkins(self.url , self.username , self.passwd)
        self.xmlTemple = '<?xml version=\'1.1\' encoding=\'UTF-8\'?><project><actions/><description>java program bigdata build test</description><keepDependencies>false</keepDependencies><properties/><scm class="hudson.plugins.git.GitSCM" plugin="git@3.9.1"><configVersion>2</configVersion><userRemoteConfigs><hudson.plugins.git.UserRemoteConfig><url>GITTEMPLE</url></hudson.plugins.git.UserRemoteConfig></userRemoteConfigs><branches><hudson.plugins.git.BranchSpec><name>*/master</name></hudson.plugins.git.BranchSpec></branches><doGenerateSubmoduleConfigurations>false</doGenerateSubmoduleConfigurations><submoduleCfg class="list"/><extensions/></scm><canRoam>true</canRoam><disabled>false</disabled><blockBuildWhenDownstreamBuilding>false</blockBuildWhenDownstreamBuilding><blockBuildWhenUpstreamBuilding>false</blockBuildWhenUpstreamBuilding><triggers/><concurrentBuild>false</concurrentBuild><builders><hudson.tasks.Maven><targets>TARGETS</targets><mavenName>maven3</mavenName><pom>/root/.jenkins/workspace/JOBNAME/pom.xml</pom><usePrivateRepository>false</usePrivateRepository><settings class="jenkins.mvn.DefaultSettingsProvider"/><globalSettings class="jenkins.mvn.DefaultGlobalSettingsProvider"/><injectBuildVariables>false</injectBuildVariables></hudson.tasks.Maven><hudson.tasks.Shell><command>echo &quot;bulid java program success!&quot;</command></hudson.tasks.Shell></builders><publishers/><buildWrappers/></project>'

    '''
        :return : list of jobs, [ { str: str} ]	
        [{"url": "http://192.168.12.74:8080/job/bigdata_javaTest/", "color": "blue", "fullname": "bigdata_javaTest", "_class": "hudson.model.FreeStyleProject", "name": "bigdata_javaTest"}]
    '''
    def getJobs(self):
        return  self.server.get_all_jobs()

    '''
        获取任务信息
    '''
    def getJobInfo(self,jobName):
        return self.server.get_job_info(jobName)

    def getJobConfig(self , jobName):
        return  self.server.get_job_config(jobName)

    '''
        @:param jobName : 任务名字
        @:return   True or None
    '''
    def jobExist(self , jobName):
        return self.server.job_exists(jobName)

    '''
        @:param jobNmae :  任务名字
        @:return   :  0:创建失败 ; 1 已存在job ; 2创建成功 
    '''
    def jobCreate(self , jobName , configXml):
        if self.jobExist(jobName):
            return 1
        else:
            if self.server.create_job(jobName , configXml) == None:
                return 2

    '''
        @:param jobName :  任务名字
        @:return : 0删除失败  1删除成功 2不存在job
    '''
    def jobDelete(self , jobName):
        if self.jobExist(jobName):
            if self.server.delete_job(jobName) == None:
                return 1
            else:
                return 0
        else:
            return 2

    '''
        运行Job
    '''
    def jobBuild(self , jobName):
        return self.server.build_job(jobName)

    '''
        获取构建id号
    '''
    def getBuildNum(self , jobName):
        return self.server.get_job_info(jobName)['nextBuildNumber']

    '''
        控制台输出
    '''
    def jobConsoleOutput(self , jobName):
        if self.jobExist(jobName):
            bID = self.getBuildNum(jobName) - 1
            return self.server.get_build_console_output(jobName , bID)

if __name__ == "__main__":
    jenkinsutil = jenkinsUtil("http://192.168.12.74:8080")
    #print  jenkinsutil.getJobs()
    #print jenkinsutil.getJobConfig("test-eureka-server-3")

    #print jenkinsutil.jobCreate("test-eureka-server-3" , jenkinsutil.xmlTemple.replace("GITTEMPLE" , "http://192.168.10.58:3000/liaowenjie/eureka-server.git").replace("JOBNAME","test-eureka-server-3").replace("TARGETS","clean package install"))
    #print  jenkinsutil.getJobs()
    #print jenkinsutil.jobDelete("test-eureka-server-3")
    #jenkinsutil.jobBuild("test-eureka-server-3")
    jenkinsutil.jobConsoleOutput("test-eureka-server-3")
    #print jenkinsutil.getJobInfo("test-eureka-server-3")