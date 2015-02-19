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
                 timeout=5, keep_alive=False, authorized_users=None, *args, **kwargs):
        self.username = username
        self.password = password
        self.key_file = key_file
        self.timeout = timeout
        self.keep_alive = keep_alive
        self.authorized_users = authorized_users
        super().__init__(*args, **kwargs)

    def __str__(self):
        return "{}@{}:{}".format(self.username, self.host, self.port)

class User:
    def __init__(self, username='user', password=None, key_file=None,
                 *args, **kwargs):
        self.username = username
        self.password = password
        self.key_file = key_file


AUTHORISED_KEYS = "authorized_keys"
USERS = {
    "user_default" : User(username="thomas",
                          password="food"),
                          #key_file="/home/thomas/.ssh/id_rsa.pub"),
    "user_std" : User(username="jondo",
                      password="foo"),
    "user_key" : User(username="toto",
                      key_file="/home/thomas/.ssh/id_rsa.pub")

}

USERNAMES = [i.username for i in USERS.values()]

SERVERS = [
    Server(
        host='0.0.0.0',
        port=2200,
        endpoints = [
            Endpoint(
                host="localhost",
                port=22,
                username="thomas",
                password="aloalo",
                authorized_users=[USERS["user_default"].username],
                timeout=2,
            ),
            Endpoint(
                host="localhost",
                port=22,
                username="thomas",
                password="aloalo",
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
                password="flop flop",
            ),
            Endpoint(
                host="creamy.hd.free.fr",
                username="publication",
                key_file="/home/thomas/.ssh/id_rsa.pub",
            )

        ]
    )
]
