# webapp.py
 
import time
import re 
 
def app(environ, start_response, poststr):
    """
    #ReDoS Code
    s1 = time.time()
    flaw_regex = re.compile('^(a+)+$')
    flaw_regex.match(poststr)
    time.sleep(15)
    s2 = time.time()
    #print("Consuming time: %.4f" % (s2-s1))
    #self.wfile.write("Consuming time: %.4f" % (s2-s1))
    """

    staus = '200 OK'
    response_handlers = [
        ('Content-Type', 'text/plain;charset=UTF-8')
        ]
    start_response(staus, response_handlers)

    #ReDoS Code
    s1 = time.time()
    flaw_regex = re.compile('^(a+)+$')
    flaw_regex.match(poststr)
    #time.sleep(15)
    s2 = time.time()
    #print("Consuming time: %.4f" % (s2-s1))
    #self.wfile.write("Consuming time: %.4f" % (s2-s1))
 
    return '\n==========simple application==========\n%s\nyour name is %s\n Consuming time is %.4f\n' % (time.ctime(),poststr,(s2-s1))

