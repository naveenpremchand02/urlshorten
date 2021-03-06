import cgi,random, string,wsgiref.handlers

from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class Datastore(db.Model):
    url1=db.StringProperty(multiline=True)
    url2=db.StringProperty(multiline=True)
     

class MainPage(webapp.RequestHandler):
    def get(self):
        
        self.response.out.write("""
          <html>
		<head>
			<head>
	<title>URL SHORTNER</title>
	
		</head>
		
      
            <body >
		
	
		<center><img src="http://icrunched.co/wp-content/uploads/2012/10/java_url.jpg" width="500" height="250"/></center>
              <center><h1>Please enter a valid url </h1></center>
             <center>

              <form action="/sign" method="post">
                <div><textarea name="content" rows="1" cols="60"></textarea></div>
                <div><input type="submit" value="Enter URL"></div>
		<p><input type="reset" /></p>
              </form>
		</center>
            </body>
          </html>""")
 
class Guestbook(webapp.RequestHandler):
    def post(self): 
        urlcontent=cgi.escape(self.request.get('content'))
        urlcon='http://'+urlcontent
           
        greeting=db.GqlQuery('SELECT * FROM Datastore WHERE url1 =:1 ',urlcon).fetch(1)
        if greeting:
                    self.response.out.write("""
                      <html>
                        
   
                    <body>
                         <p>
                       
                       <div>SHORTENED URL : http://tinynaveenz.appspot.com/%s</div></p>
                         
             
                    </body>
                  </html>""" %(greeting[0].url2))      
        else:
                    prntmesg=Datastore()    
                    url3=urlcon     
		    list=[]
                    nwurl=''
		    for i in range(len(url3)):
			if i%20==0:
				list.append(url3[i])

		    nwurl=''.join(list)+random.choice(string.ascii_letters)
		    prntmesg.url1=urlcon
                    prntmesg.url2=nwurl
                    prntmesg.put()
                 
             
                    self.response.out.write("""
                     <html>
                     <head>
			<title>YOU SHORTNED URL</title>
    
                      </head>
                     <body>
			<center><img src="http://talknerdy2me.org/wp-content/uploads/2012/02/quotes-on-success.jpg" width="500" height="250"/>
                   
                  <p><p>  <div>Shortned url is : http://tinynaveenz.appspot.com/%s</div></p></p>
			
			<div> Want to check url please click below</div>
			
			<p><p><div><a href=http://tinynaveenz.appspot.com/%s>http://tinynaveenz.appspot.com/%s</a></p></p>
</centre>
                   
                    
                </body>
                </html>""" % (nwurl,nwurl,nwurl))


class Redirecting(webapp.RequestHandler):
    def get(self):
        urlp=self.request.path
        url=urlp[1:]
        
        greeting=db.GqlQuery('SELECT * FROM Datastore WHERE url2 =:1 ',url).fetch(1)
        if greeting:
            self.redirect(greeting[0].url1)         
        
            
     

application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/sign', Guestbook),
                                     ('/.*', Redirecting)],
                                      debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":

    main()

