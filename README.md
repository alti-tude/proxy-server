proxy-server
============

# Proxy Server
```shell
python3 main.py
```

# Client (using curl)
### With HTTP authentication
```shell
export http_proxy=localhost:20100
export https_proxy=localhost:20100
curl --local-port 20000-20099 -u trial:trial http://www.fortune.com
```
### Without HTTP authentication
```shell
curl --proxy 127.0.0.1:20100 --local-port 20000-20099 http://www.fortune.com
```


