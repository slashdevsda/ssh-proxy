#!/usr/bin/env python

# Copyright (C) 2003-2007  Robey Pointer <robeypointer@gmail.com>
#
# This file is part of paramiko.
#
# Paramiko is free software; you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation; either version 2.1 of the License, or (at your option)
# any later version.
#
# Paramiko is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Paramiko; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA.

import base64
from binascii import hexlify
import os
import socket
import sys
import threading
import traceback
import threading, multiprocessing
import paramiko
from paramiko.py3compat import b, u, decodebytes
import conf
import time
import select
from pprint import pprint
# setup logging
paramiko.util.log_to_file('demo_server.log')

host_key = paramiko.RSAKey(filename='test_rsa.key')
#host_key = paramiko.DSSKey(filename='test_dss.key')

print('Read key: ' + u(hexlify(host_key.get_fingerprint())))


class ParamikoServer(paramiko.ServerInterface):
    # 'data' is the output of base64.encodestring(str(key))
    # (using the "user_rsa_key" files)
    data = (b'AAAAB3NzaC1yc2EAAAABIwAAAIEAyO4it3fHlmGZWJaGrfeHOVY7RWO3P9M7hp'
            b'fAu7jJ2d7eothvfeuoRFtJwhUmZDluRdFyhFY/hFAh76PJKGAusIqIQKlkJxMC'
            b'KDqIexkgHAfID/6mqvmnSJf0b5W8v5h2pI/stOSwTQ+pxVhwJ9ctYDhRSlF0iT'
            b'UWT10hcuO4Ks8=')
    good_pub_key = paramiko.RSAKey(data=decodebytes(data))

    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        if username in conf.PASSWD:
            if conf.PASSWD[username] == password:
                return paramiko.AUTH_SUCCESSFUL
            
        return paramiko.AUTH_FAILED

    def check_auth_publickey(self, username, key):
        print('Auth attempt with key: ' + u(hexlify(key.get_fingerprint())))
        if (username == 'robey') and (key == self.good_pub_key):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED
    
    def get_allowed_auths(self, username):
        return 'password,publickey'

    def check_channel_shell_request(self, channel):
        self.event.set()
        return True

    def check_channel_pty_request(self, channel, term, width, height, pixelwidth,
                                  pixelheight, modes):
        return True


DoGSSAPIKeyExchange = True



class SSHTransport(threading.Thread):
    """Composition class for threaded SSH Transport.
    This ..."""
    def __init__(self, cient, addr, endpoints, *args, **kwargs):
        self._client, self._addr = cient, addr
        self._endpoints = endpoints
        self.channels = {}
        self.buffers = {}
        self.proxy_chan = None
        self.main_chan = None
        super().__init__(*args, **kwargs)

    def make_bridge(self, file1, file2):
        """ """
        #os.pipe(file1, file2)

    def proxify_channel(self, chan, endpoint):

        #chan.send("\r\n{}\r\n".format(conf.MOTD()))
        #chan.send('\r\n\r\#Nouvelle Rolls Royce, sur du 22 !!\r\n\r\n')

        #availables_endpoints = ""
        #for index, i in enumerate(self._endpoints):
        #    availables_endpoints += "[%s] - %s%s"  %(str(index), i, "\r\n")
        #chan.send(availables_endpoints)
        #chan.send('Choice: ')
        #f = chan.makefile('rwU')
        #selected = f.readline().strip('\r\n')
        #f.write("YOOOO")
        #chan.send('\r\nSelected : ' + selected + '.\r\n')

        try:
            c = ClientProxy(endpoint.host,
                            endpoint.port,
                            endpoint.username,
                            endpoint.password,
                            endpoint.timeout,
                            endpoint.keep_alive,
                            endpoint.key_file)
            proxy_chan = c.get_channel()
        except socket.timeout:
            chan.send("Timeout. Can't reach host {}\r\n".format(endpoint))
            return

        self.client = c
        proxy_chan.get_pty(term="xterm")
        proxy_chan.invoke_shell()
        #time.sleep(0.5)
        self.proxy_chan = proxy_chan
        # push in channels for event polling
        #self.channels[chan] = proxy_chan
        #self.channels[proxy_chan] = chan

        self.buffers[chan] = b""
        self.buffers[proxy_chan] = b""

    
        

    def run(self):
        print("start new transport thread")
        transport = paramiko.Transport(self._client) #ERRoR ?
        transport.add_server_key(host_key)
        server = ParamikoServer()
        try:
            transport.start_server(server=server)
        except paramiko.SSHException:
            print('*** SSH negotiation failed.')
            sys.exit(1)

        # wait for auth
        self.main_chan = transport.accept(20)
        chan = self.main_chan
        if chan is None:
            print('*** No channel.')
            return
        print('Authenticated!')

        server.event.wait(10)
        if not server.event.isSet():
            print('*** Client never asked for a shell.')
            return
        self.run_basic_console()
        #self.proxify_channel(chan)
        #self.run_proxy_main_loop()

    def run_basic_console(self):
        """Communicate with user"""
        self.main_chan.send("\r\n{}\r\n".format(conf.MOTD()))

        availables_endpoints = ""
        for index, i in enumerate(self._endpoints):
            availables_endpoints += "[%s] - %s%s"  %(str(index), i, "\r\n")
            

        while 1:
            self.main_chan.send(availables_endpoints)
            self.main_chan.send('type n for next page, p for previous, q to exit.\r\n')
            self.main_chan.send('Choice: ')
            choice = self.main_chan.recv(1)
            self.main_chan.send(choice)
            self.main_chan.send('\r\n')
            if choice == b'n': pass
            elif choice == b'p': pass
            elif choice == b'q':
                self.main_chan.send("goodbye\r\n")
                self.main_chan.close()
                return
            else:
                try:
                    endpoint = self._endpoints[int(choice, 10)]
                except ValueError:
                    self.main_chan.send("goodbye\r\n")
                    self.main_chan.close()
                    return
                    
                self.proxify_channel(self.main_chan, endpoint)
                self.run_proxy_main_loop()
                #return
                self.main_chan.send("\r\n\t <! back on gate !>\r\n")                
                
        #f = self.main_chan.makefile('rwU')
        #selected = f.readline().strip('\r\n')
        #f.write(selected)
        #self.main_chan.send('\r\nSelected : ' + selected + '.\r\n')
        
        #while 1:
        #    if self.main_chan.recv_ready():

    
    def run_proxy_main_loop(self):
        if self.proxy_chan == None or  self.main_chan == None:
            return
        print("avant select")
        while 1:
            rfs = [self.proxy_chan, self.main_chan] #list(self.channels.keys())
            efs = rfs
            r, w, e = select.select(rfs, [], [], 1.5)
            #sys.stdout.flush()
            # reading
            for fd in r:
                #try:
                readed = fd.recv(4096)
                if len(readed) and readed[0] == 4:
                    print("EOF")
                    #self.proxy_chan.close()
                    #fd.close() ICI
                    return
                if readed != b"":
                    if fd == self.main_chan:
                        self.buffers[self.proxy_chan] += readed
                    elif fd == self.proxy_chan:
                        self.buffers[self.main_chan] += readed

            for fd in e:
                print("error fd : ", fd)
                #self.remove_fd(fd)


            # writing
            for key in self.buffers:
                if len(self.buffers[key]):
                    #print(self.buffers[key][0:min(len(self.buffers[key]), 4096)])
                    try:
                        key.send(self.buffers[key][0:min(len(self.buffers[key]), 4096)])
                    except KeyboardInterrupt:
                        print("KI")
                    self.buffers[key] = self.buffers[key][min(len(self.buffers[key]), 4096):]



            #if self.proxy_chan.exit_status_ready() and not self.proxy_chan.get_transport().is_active():
                #print("QUIT QUIT")
                #return

        self.channels = {}
        self.buffers = {}


class Server(multiprocessing.Process):
    """Server Process"""
    def __init__(self, host, port, endpoints, *args, **kwargs):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((host, port))
        self.sock.listen(100)
        self._endpoint = endpoints
        super().__init__(*args, **kwargs)


    def run(self):
        jobs = []
        while 1:
            client, addr = self.sock.accept()
            s = SSHTransport(client, addr, self._endpoint)
            jobs.append(s)
            s.start()


class ClientProxy(threading.local):
    """PROXY -----> REMOTE SSH SERVER"""
    def __init__(self, host, port, username, password, timeout=5.0, keep_alive=False, key_file=None):
        super().__init__()
        self.connection = paramiko.SSHClient()
        self.connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.connection.connect(host, port, username=username, password=password, timeout=timeout,key_filename=key_file)
        self.chan = self.connection.get_transport().open_channel("session")
        if keep_alive:
            self.connection.get_transport().set_keepalive(keep_alive)
        else:
            self.connection.get_transport().set_keepalive(0)

        
    def get_channel(self):
        return self.chan



if __name__ == "__main__":
    services = []
    for conf_server in conf.SERVERS:
        hostname, port, endpoints = conf_server.host, conf_server.port, conf_server.endpoints
        s = Server(hostname, port,  endpoints)
        services.append(s)
        s.start()

    for service in services:
        service.join()
