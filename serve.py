import os
import SimpleHTTPServer
import SocketServer

import monitor
from blog import main as blog_main

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

OUTPUT_DIR = os.path.join(PROJECT_DIR, 'output')

POSTS_DIR = os.path.join(PROJECT_DIR, 'posts')
STATIC_DIR = os.path.join(PROJECT_DIR, 'static')
TEMPLATES_DIR = os.path.join(PROJECT_DIR, 'templates')
BLOG_FILE = os.path.join(PROJECT_DIR, 'blog.py')

BLOG_SCRIPT = 'python %s' % (BLOG_FILE,)


def main():
    os.chdir(OUTPUT_DIR)
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
    monitor.start(interval=1.0)
    monitor.track_paths([POSTS_DIR, STATIC_DIR, TEMPLATES_DIR, BLOG_FILE])
    main()
