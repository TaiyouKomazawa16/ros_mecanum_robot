#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist
from std_msgs.msg import Int8MultiArray
from std_msgs.msg import MultiArrayDimension

BUTTONS_NUM = 11
vel_msg = Twist()
button = Int8MultiArray()
button.data = [0 for _ in range(BUTTONS_NUM)]

rospy.init_node('joy_converter')

x_gain = rospy.get_param('~x', 1)
y_gain = rospy.get_param('~y', 1)
z_gain = rospy.get_param('~z', 1)

def callback(_data):
    vel_msg.linear.x = _data.axes[1] * x_gain
    vel_msg.linear.y = _data.axes[0] * y_gain
    vel_msg.angular.z = _data.axes[3] * z_gain
    for i in range(BUTTONS_NUM):
        button.data[i] = _data.buttons[i]
def main():
    pub_cmd_vel = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    pub_buttons = rospy.Publisher('/buttons', Int8MultiArray, queue_size=10)
    r = rospy.Rate(10)
    button.layout.dim.append(MultiArrayDimension())
    button.layout.dim[0].size = BUTTONS_NUM
    rospy.Subscriber("joy", Joy, callback)
    while not rospy.is_shutdown():
        pub_cmd_vel.publish(vel_msg)
        pub_buttons.publish(button)
        r.sleep()

if __name__ == '__main__':
    main()
