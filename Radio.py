import tornado.ioloop
import tornado.web
import os
import sys
import Display

class HomeHandler(tornado.web.RequestHandler):
    
    def get(self):
        self.render('index.html')

class select_station(tornado.web.RequestHandler):
                
    def post(self):
        selected_button = self.get_argument('channel')      
        for i in range (1,6):
            if(selected_button.__eq__(i)):
                os.system("mpc play"+" " + selected_button)
                obj1 = Display.DisplayLcd()
                obj1.send_to_LCD()
                break    

settings={
    "static_path" : os.path.join(os.path.dirname(__file__), "static")
    }
    
#define API URLs and map them to corresponding classes
application=tornado.web.Application([(r"/radio-stations/select/",select_station),
                                     (r"/",HomeHandler),
                                     (r"/img/(.*)",tornado.web.StaticFileHandler, dict(path=settings['static_path'])),
                                     (r"/css/(.*)",tornado.web.StaticFileHandler, dict(path=settings['static_path'])),
                                     (r"/js/(.*)",tornado.web.StaticFileHandler, dict(path=settings['static_path'])),
                                                                           ],**settings)

#start Tornado service
if __name__=="__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()