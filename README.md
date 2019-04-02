proxy-server
============

# Client
```shell
export http_proxy=localhost:20100
export https_proxy=localhost:20100
curl --local-port 20000-20099 http://www.fortune.com
```

# Server
```shell
python3 main.py
```