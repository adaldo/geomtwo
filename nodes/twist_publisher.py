#!/usr/bin/env python
import rospy as rp
import geomtwo.msg as gms
import geomtwo.impl as gmi
import math as m


rp.init_node(name="twist_publisher")
FREQUENCY = 3e1
RATE = rp.Rate(FREQUENCY)
TIME_STEP = 1/FREQUENCY

pub = rp.Publisher(name="twist", data_class=gms.Twist, queue_size=10)


while not rp.is_shutdown():
    time = rp.get_time()
    pub.publish(gmi.Vector(magnitude=1.0, angle=time).message, m.cos(time))
    #pub.publish(gms.Vector(), 1.0)
    RATE.sleep()
