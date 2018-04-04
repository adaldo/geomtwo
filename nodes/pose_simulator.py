#!/usr/bin/env python
import rospy as rp
import geomtwo.msg as gms
import geomtwo.impl as gmi
import threading as thd



rp.init_node(name="pose_simulator")
FREQUENCY = 3e1
RATE = rp.Rate(FREQUENCY)
TIME_STEP = 1/FREQUENCY

LOCK = thd.Lock()

pose = gmi.Pose()
twist = None

def callback(msg):
    global twist
    LOCK.acquire()
    twist = gmi.Twist(msg)
    LOCK.release()

rp.Subscriber(name="twist", data_class=gms.Twist, callback=callback)

pub = rp.Publisher(name="pose", data_class=gms.Pose, queue_size=10)

read_velocity = None
while not rp.is_shutdown():
    LOCK.acquire()
    if not twist is None:
        pose += twist.integrate(TIME_STEP)
        twist = None
    LOCK.release()
    pub.publish(pose.message)
    RATE.sleep()
