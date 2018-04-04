#!/usr/bin/env python
import rospy as rp
import geomtwo.msg as gms
import geomtwo.impl as gmi
import threading as thd
import matplotlib.pyplot as plt


rp.init_node(name="point_plotter")
FREQUENCY = 3e1
RATE = rp.Rate(FREQUENCY)
TIME_STEP = 1/FREQUENCY

LOCK = thd.Lock()

point = None
artists = None

def callback(msg):
    global point
    LOCK.acquire()
    point = gmi.Point(msg)
    LOCK.release()

rp.Subscriber(name="point", data_class=gms.Point, callback=callback)



plt.ion()
plt.figure()
plt.grid(True)
while not rp.is_shutdown():
    LOCK.acquire()
    if not point is None:
        if not artists is None:
            for artist in artists:
                artist.remove()
        artists = point.draw()
        point = None
    LOCK.release()
    plt.draw()
    RATE.sleep()
