


import psychic_bear.conf as conf
import paramiko
from paramiko.py3compat import decodebytes


def validate_conf():
    if not hasattr(conf, "USERS"):
        print("conf should contains an USER variable that describe users")
        return False
    if not hasattr(conf, "SERVERS"):
        print("conf should contains an SERVERS variable that describe local servers")
        return False

    #Validate SERVERS & endpoints :
    for server in conf.SERVERS:
        if not isinstance(server.port, int):
            print("server port should be an INT.")
            return False

        for endpoint in server.endpoints:
            if endpoint.key_file:
                try:
                    key = open(endpoint.key_file, 'rb').read()
                    a = paramiko.RSAKey(data=decodebytes(key.split()[1]))

                except Exception as e:
                    print("{} key file seems invalid.", endpoint.key_file)
                    print(e)
                    return False

        if not len(server.endpoints):
            print("A server must handle at least one endpoint")
            return False
            
    #Validate USERS #TODO :
    return True
