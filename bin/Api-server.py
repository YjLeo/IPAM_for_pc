# coding=utf-8
from flask import Flask
from flask import request
from flask_restful import Resource, Api

from core.control import ip, Store


class get_ip(Resource):
    @staticmethod
    def get():
        if request.method == 'GET':
            ips=ip.get_ip()
            return ips
class recover_ip(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            data=request.args.get('ip')
            rev=ip.rec_ip(data)
            return rev

class store(Resource):
    @staticmethod
    def post():
        if request.method =='POST':
            id=request.args.get('id')
            ip=request.args.get('ip')
            rev=Store.put_dockerid(id,ip)
            return rev

    @staticmethod
    def get():
        if request.method == "GET":
            id=request.args.get('id')
            rev=Store.get_dockerip(id)
            #return null or ip
            return rev
    @staticmethod
    def delete():
        if request.method=="DELETE":
            id=request.args.get('id')
            rev=Store.del_dockerid(id)
            return rev



app = Flask(__name__)
api = Api(app)
if __name__ == '__main__':
    api.add_resource(get_ip, '/api/v1/get_free_ip/', '/api/v1/get_free_ip/')
    api.add_resource(recover_ip, '/api/v1/rec_free_ip/', '/api/v1/rec_free_ip/<string:ip>')
    api.add_resource(store,'/api/v1/map_store/','/api/v1/map_store/<string:id>/<string:ip>')

    app.run(host='0.0.0.0',port=5000,debug=False,threaded=True)
