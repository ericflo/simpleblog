import os
import SimpleHTTPServer
import SocketServer

import monitor
from blog import main as blog_main

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

POSTS_DIR = os.path.join(PROJECT_DIR, 'posts')
STATIC_DIR = os.path.join(PROJECT_DIR, 'static')
BLOG_FILE = os.path.join(PROJECT_DIR, 'blog.py')

BLOG_SCRIPT = 'python %s' % (BLOG_FILE,)


def main():
    monitor.start(interval=1.0)
    monitor.track_paths([POSTS_DIR, STATIC_DIR, BLOG_FILE])
    httpd = SocketServer.TCPServer(
        ('', 8000),
        SimpleHTTPServer.SimpleHTTPRequestHandler,
    )
    print 'Serving at port', 8000
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.shutdown()


if __name__ == '__main__':
    blog_main()
    main()
