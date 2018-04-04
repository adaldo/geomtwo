#!/usr/bin/env python
import rospy as rp
import geomtwo.msg as gms
import geomtwo.impl as gmi
import threading as thd



rp.init_node(name="point_simulator")
FREQUENCY = 3e1
RATE = rp.Rate(FREQUENCY)
TIME_STEP = 1/FREQUENCY

LOCK = thd.Lock()

point = gmi.Point(1,0)
velocity = None

def callback(msg):
    global velocity
    LOCK.acquire()
    velocity = gmi.Vector(msg)
    LOCK.release()

rp.Subscriber(name="velocity", data_class=gms.Vector, callback=callback)

pub = rp.Publisher(name="point", data_class=gms.Point, queue_size=10)

read_velocity = None
while not rp.is_shutdown():
    LOCK.acquire()
    if not velocity is None:
        point += velocity*TIME_STEP
        velocity = None
    LOCK.release()
    pub.publish(point.message)
    RATE.sleep()
