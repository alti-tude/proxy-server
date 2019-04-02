import ipaddress

class Blacklist:

    def __init__(self, filename="proxy/blacklist.txt"):
        self.__blacklist_addr = []
        file = open(filename, 'r')
        for cidr in file:
            self.__blacklist_addr.append(cidr.rstrip())
        file.close()


    def blacklisted(self, ip):
        try:
            ip = ipaddress.ip_address(ip)
        except Exception as e:
            print("ERROR: Given string is not an IP")
            print("Sys Error: ", e)
            return None
        for cidr in self.__blacklist_addr:
            net = ipaddress.ip_network(cidr)
            if ip in net:
                return True
        return False


if __name__ == '__main__':
    blacklist = Blacklist("fil")
    print(blacklist.blacklisted("192.168.43.208"))
