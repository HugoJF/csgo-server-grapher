import valve.rcon
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import sys
import re

servers = {
    "CSGO-1": {
        "address": ("143.202.39.221", 27001),
        "rcon": "xxxxxx",
        "color": "red",
        "fps": 128
    }
}

regex = re.compile("\s+")

def connect_server(svname):
    print("Connection to server ", svname, servers[svname]["address"], servers[svname]["rcon"])
    sys.stdout.flush()
    try:
        servers[svname]["connection"] = valve.rcon.RCON(servers[svname]["address"], servers[svname]["rcon"])
        servers[svname]["connection"].connect()
        servers[svname]["connection"].authenticate()
        servers[svname]["file"] = open(svname + ".csv", "a+", 1)
    except Exception  as e:
        print('Error while authenticating server {0}'.format(svname))
        exit(1)
        
    sys.stdout.flush()

def clamp(a, b):
    if a > b:
        return b
    else:
        return a

for svname in servers.keys():
    connect_server(svname)

print("Waiting for connections...")
sys.stdout.flush()
time.sleep(1)

print("Running loop")
sys.stdout.flush()


fig = plt.figure()
ax = fig.add_subplot(111)
plt.ion()

fig.show()
fig.canvas.draw()
patches = []
patched = False
while True:
    print("################### LOOPING SERVERS ###################")

    ax.clear()
    patches.clear()

    for svname in sorted(servers):
        svname
        rcon = servers[svname]["connection"]
        out = servers[svname]["file"]
        try:
            response = rcon.execute("stats")
        except Exception as e:
            print("Error while executing stats on console, reconnecting...")
            connect_server(svname)
            
        split = regex.split(response.text)
        
        fps = clamp(float(split[16]), 128)
        players = split[17]
        svms = split[18]
        stdvar = split[19]
        var = split[20]
        if 'stats' in servers[svname]:
            below_min = sum(1 for x in servers[svname]['stats'] if x < (servers[svname]['fps'] * 0.9))
            tot = len(servers[svname]['stats'])
        else:
            below_min = 0
            tot = 1
        
        out.write("{},{},{},{},{}".format(fps, players.zfill(2), svms, stdvar, var))

        if 'stats' not in servers[svname]:
            servers[svname]['stats'] = []
        servers[svname]["stats"].append(float(fps))
        if len(servers[svname]['stats']) > 120:
            servers[svname]['stats'].pop(0)

        ax.plot(servers[svname]["stats"], label=svname, color=servers[svname]['color'])
        # plt.pause(0.5)
        if patched == False:
            patch = mpatches.Patch(color=servers[svname]['color'], label=svname + "[" + players + "]")
            patches.append(patch)

        print("{0}:\t{1:.1f} FPS\t+- {2} with {3:02d} players <{4}%".format(svname, round(fps, 2), svms, int(players), round(below_min / tot * 100)))
    sys.stdout.flush()

    if patched == False:
        fig.legend(handles=None)
        fig.legend(handles=patches)
        patched = True

    fig.canvas.draw()
    # time.sleep(0.5)
    plt.pause(0.01)
