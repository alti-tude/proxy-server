import time
import urllib.request

class Cache:
    """ LRU cache """

    def __init__(self, max_size=3):
        self.cache = {}
        self.request_count = {}
        self.MAX_SIZE = max_size
    

    def get_cache(self, request):
        """
        Get cached request
        """
        if request in self.cache:
            check_request = urllib.request.Request(request)
            timestamp = time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime(self.cache[request]['access_time']))
            check_request.add_header('If-Modified-Since', timestamp)
            try:
                _ = urllib.request.urlopen(check_request)
            except urllib.error.HTTPError as err:
                if err.code == 304:
                    self.cache[request]['access_time'] = time.time()
                    return self.cache[request]['content']
                elif err.code == 200:
                    del self.cache[request]
                else:
                    print("ERROR: Could not retrieve URL")
        return None
    
    
    def set_cache(self, request, content):
        """
        Add / Update value to cache
        """
        if request not in self.cache and len(self.cache) >= self.MAX_SIZE:
            self.remove_lru()
        self.cache[request] = {'access_time':time.time(), 'content':content}


    def update(self, request, content):
        """
        Cache all requests made thrice in last 5 minutes, else remove
        """
        self.clear_request_count()
        if request not in self.request_count:
            self.request_count[request] = {'request_time':time.time(), 'count':0}
        else:
            if self.request_count[request]['count'] < 3:
                self.request_count[request]['count'] += 1
            else:
                self.set_cache(request, content)
                del self.request_count[request]
        return


    def clear_request_count(self):
        """
        Remove all requests not made thrice in last 5 minutes
        """
        for request in self.request_count:
            if (
                    time.time() - self.request_count[request]['request_time'] >= 5*60 and
                    self.request_count[request]['count'] < 3
                ):
                del self.request_count[request]
        return


    def remove_lru(self):
        """
        Remove least recently used cache
        """
        oldest_request = None
        for request in self.cache:
            if (
                    oldest_request is None or
                    self.cache[request]['access_time'] < self.cache[oldest_request]['access_time']
                ):
                oldest_request = request
        del self.cache[oldest_request]

