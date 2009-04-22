from xmlrpclib import Server
myserver = Server("http://192.168.0.10:8086")
print myserver.get_list(0)

