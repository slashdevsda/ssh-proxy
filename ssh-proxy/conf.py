MOTD = lambda : """Welcome on the gate""" 

PASSWD = {
    "thomas":"foo",
    "francis":"foo"

}

ENDPOINTS = {
    ("localhost", 22)  : {"thomas" : "aloalo"},
    ("10.0.8.24", 1201): {"thomas" : "aloalo"},
}

SERVERS = {
    ("localhost", 2200) : ENDPOINTS,
    ("localhost", 2201) : ENDPOINTS,
}

HOST = "localhost"
PORT = 2200


class SSHService:
    """Define a basic SSH service"""
    def __init__(self, host="localhost", port=22):
        self.host = host
        self.port = port        

class Server(SSHService):
    def __init__(self, endpoints=[], *args, **kwargs):
        self.endpoints = endpoints
        super().__init__(*args, **kwargs)

class Endpoint(SSHService):
    def __init__(self, username='user', password=None, key_file=None,
                 timeout=5, keep_alive=False, *args, **kwargs):
        self.username = username
        self.password = password
        self.key_file = key_file
        self.timeout = timeout
        self.keep_alive = keep_alive
        super().__init__(*args, **kwargs)

    def __str__(self):
        return "{}@{}:{}".format(self.username, self.host, self.port)


SERVERS = [
    Server(
        host='0.0.0.0',
        port=2200,
        endpoints = [
            Endpoint(
                host="localhost",
                port=22,
                username="thomas",
                password="qwerty",
            ),
            Endpoint(
                host="94.23.37.56",
                port=22,
                username="thomas",
                password="azerty",
                timeout=20,
                keep_alive=10,
            ),
            Endpoint(
                host="5.39.76.111",
                username="thomas",
                password="apSv20Yy",
            ),
            Endpoint(
                host="192.168.0.42",
                username="publication",
                key_file="/home/thomas/.ssh/id_rsa.pub",
            )

        ]
    )
]
