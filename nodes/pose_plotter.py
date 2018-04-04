#!/usr/bin/env python
import rospy as rp
import geomtwo.msg as gms
import geomtwo.impl as gmi
import threading as thd
import matplotlib.pyplot as plt


rp.init_node(name="pose_plotter")
FREQUENCY = 3e1
RATE = rp.Rate(FREQUENCY)
TIME_STEP = 1/FREQUENCY

LOCK = thd.Lock()

pose = None
artists = None

def callback(msg):
    global pose
    LOCK.acquire()
    pose = gmi.Pose(msg)
    LOCK.release()

rp.Subscriber(name="pose", data_class=gms.Pose, callback=callback)



plt.ion()
plt.figure()
plt.grid(True)
plt.axis([-5,5,-5,5])

while not rp.is_shutdown():
    LOCK.acquire()
    if not pose is None:
        if not artists is None:
            for artist in artists:
                artist.remove()
        artists = pose.draw()
        pose = None
    LOCK.release()
    plt.draw()
    RATE.sleep()
