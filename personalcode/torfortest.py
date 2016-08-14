#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os,time,datetime
import requests
import requesocks
import socket
import socks

url = 'http://icanhazip.com/'


def getip_requests(url):
    print "(+) Sending request with plain requests..."
    r = requests.get(url)
    print "(+) IP is: " + r.text.replace("\n", "")


def getip_requesocks(url):
    print "(+) Sending request with requesocks..."
    session = requesocks.session()
    session.proxies = {'http': 'socks5://127.0.0.1:9050',
                       'https': 'socks5://127.0.0.1:9050'}
    r = session.get(url)
    print "(+) IP is: " + r.text.replace("\n", "")

def main():
    print "Running tests..."
    getip_requests(url)
    getip_requesocks(url)
    os.system("""(echo authenticate '"yourpassword"'; echo signal newnym; echo quit) | nc localhost 9051""")
    getip_requesocks(url)
    #main()
    url='https://api.ipify.org?format=json'
    print getip_requests(url)
    print getip_requesocks(url)
    os.system("""(echo authenticate '"yourpassword"'; echo signal newnym; echo quit) | nc localhost 9051""")
    print getip_requesocks(url)

def reset_ip_address(reset=False):
    import os
    import socket
    import socks
    if reset:
        os.system("""(echo authenticate '"mypassword"'; echo signal newnym; echo quit) | nc localhost 9051""")
    else:
        pass
    socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)
    socket.socket = socks.socksocket


if __name__ == "__main__":
    url='http://ifconfig.me/ip'
    #print getip_requesocks(url)
    reset_ip_address(reset=False)

    #print datetime.datetime.now()

    print (requests.get(url).text)
