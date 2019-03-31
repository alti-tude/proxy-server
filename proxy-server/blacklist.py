import ipaddress

class Blacklist:

    def __init__(self, filename="proxy/blacklist.txt"):
        self.__blacklist_addr = []
        file = open(filename, 'r')
        for cidr in file:
            self.__blacklist_addr.append(cidr)
        file.close()


    def blacklisted(self, ip):
        for cidr in self.__blacklist_addr:
            net = ipaddress.ip_network(cidr)
            if ip in net:
                return True
        return False
    
