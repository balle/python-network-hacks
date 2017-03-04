#!/usr/bin/python

from libmproxy import controller, proxy

class Sniffer(controller.Master):
    def run(self):
        try:
            return controller.Master.run(self)
        except KeyboardInterrupt:
            self.shutdown()


    def handle_request(self, request):
        print "Got request\n" + str(request.headers)
        request._ack()

    def handle_response(self, response):
        print "Got response\n" + str(response.headers)
        print response.content
        response._ack()


port = 1337
ssl_config = proxy.SSLConfig("cert.pem")
proxy_server = proxy.ProxyServer(ssl_config, port)
m = Sniffer(proxy_server)

print "Running proxy on port " + str(port)
m.run()
