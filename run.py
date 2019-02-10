from valve.rcon import RCON
import subprocess
import time
import json
import sys
import re
import os

rrd_path = os.getenv('RRD_PATH', '')
timeout = int(os.getenv('TIMEOUT', 1))


def get_filename(sv):
    addr = get_addr(sv)
    return re.sub(r"[^A-Za-z0-9]", "_", addr)


def get_addr(sv):
    return "{0}:{1}".format(sv['ip'], sv['port'])


def connect_server(sv):
    addr = get_addr(sv)
    try:
        connections[addr] = RCON((sv['ip'], sv['port']), password=sv['rcon'], timeout=5)
        connections[addr].connect()
        connections[addr].authenticate()
    except Exception as e:
        print(e)
        print('Error while authenticating server {0}'.format(addr))
        
    sys.stdout.flush()


def clamp(a, b):
    if a > b:
        return b
    else:
        return a


connections = {}
content = open('servers.json')
servers = json.load(content)
regex = re.compile("\s+")

for sv in servers:
    connect_server(sv)

print("Waiting for connections...")
sys.stdout.flush()
time.sleep(1)

print("Running loop")
sys.stdout.flush()

while True:
    for sv in servers:
        addr = get_addr(sv)
        rcon = connections[addr]
        try:
            response = rcon.execute("stats")
        except Exception as e:
            print("Error while executing stats on console, reconnecting...")
            connect_server(sv)
            continue
            
        split = regex.split(response.text)
        
        fps = clamp(float(split[16]), 128)
        players = split[17]
        svms = split[18]
        stdvar = split[19]
        var = split[20]

        print("{0}:\t{1:.1f} FPS\t+- {2} with {3:02d} players".format(addr, round(fps, 2), svms, int(players)))
        subprocess.call("rrdtool update {0}performance_{1}.rrd N:{2}:{3}:{4}".format(rrd_path, get_filename(sv), fps, svms, players), shell=True)

    sys.stdout.flush()
    time.sleep(timeout)
