#coding=utf-8
import tornado.ioloop
import tornado.web
import pymysql
import json

class MainHandler(tornado.web.RequestHandler):
    def post(self):
    	nickname = self.get_body_argument('nickname').encode('utf-8')
    	email = self.get_body_argument('email').encode('utf-8')
    	pwd = self.get_body_argument('pwd').encode('utf-8')
    	pubkey = self.get_body_argument('pubkey').encode('utf-8')
    	
    	#建立连接
    	connection = pymysql.connect(host='localhost',port=3306,user='root',passwd='',db='securechat')
    	#执行sql语句
    	try:
    		with connection.cursor() as cursor:
    			reg_req = "insert into `users` (`nickname`, `email`, `salt`, `spwd`) values (%s, %s, %s, %s) "
    			result = cursor.execute(reg_req,(nickname,email,'1',pwd))
    		#提交sql语句
    		connection.commit()
    	finally:
    		connection.close()
    	

    	if result:
    		status = "ok"
    	else:
    		status = "error"

    	feedback = {
    		'status' : status,
    		#'cert' : pubkey.decode('utf-8')
    		'cert' : create_cert(pubkey)
    	}

    	feedback = json.dumps(feedback)
    	self.write(feedback)

def create_cert(pubkey):
	#root = ET.fromstring(country_data_as_string)root = ET.fromstring(country_data_as_string)
	return "<info>233</info>"

def make_app():
    return tornado.web.Application([
        (r"/reg", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()