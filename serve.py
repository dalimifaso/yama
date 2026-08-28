import http.server, functools
D='/private/tmp/claude-501/-Users-danlivne-Documents-Claude-Projects/0d02ebac-a711-42f5-8ac4-fe5c62f260c9/scratchpad'
class H(http.server.SimpleHTTPRequestHandler):
    def guess_type(self, path):
        t = super().guess_type(path)
        return 'text/html; charset=utf-8' if t=='text/html' else t
http.server.test(HandlerClass=functools.partial(H, directory=D), port=8900, bind='127.0.0.1')
