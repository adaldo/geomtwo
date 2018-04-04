#!/usr/bin/env python
import rospy as rp
import geomtwo.msg as gms
import math as m


rp.init_node(name="velocity_publisher")
FREQUENCY = 3e1
RATE = rp.Rate(FREQUENCY)
TIME_STEP = 1/FREQUENCY

pub = rp.Publisher(name="velocity", data_class=gms.Vector, queue_size=10)

while not rp.is_shutdown():
    time = rp.get_time()
    pub.publish(gms.Vector(x=m.cos(time), y=m.sin(time)))
    RATE.sleep()
