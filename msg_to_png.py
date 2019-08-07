#!/usr/bin/env python3
#########################################################################
#
#              Author: b51
#                Mail: b51live@gmail.com
#            FileName: msg_to_png.py
#
#          Created On: Wed 07 Aug 2019 02:21:50 PM CST
#     Licensed under The MIT License [see LICENSE for details]
#
#########################################################################

import sys
import numpy
import rospy
import rosbag
import math
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

msgs_count = 0


def image_msgs_cb(msg):
    global msgs_count
    cv_image = CvBridge().imgmsg_to_cv2(msg, desired_encoding="passthrough")
    image_name = "images/mono_image_{:08d}.png".format(msgs_count)
    cv2.imwrite(image_name, cv_image);


def main(argv):
    bags = []
    with open(argv[1]) as f:
        bags = f.read().splitlines()

    global msgs_count
    if len(argv) < 2:
        print("please input a bag file")
        return
    for i in range(len(bags)):
        bag = rosbag.Bag(bags[i])
        for topic, msg, t in bag.read_messages(topics=argv[2] if len(argv) > 2 else "/mynteye/right/image_color"):
            image_msgs_cb(msg)
            msgs_count += 1
    print("%d image msgs extracted" % msgs_count)


if __name__ == "__main__":
    main(sys.argv)
