#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
import time

def move_robot():
    # Initialize the node
    rospy.init_node('square_move', anonymous=True)
    # Publisher for /cmd_vel topic
    velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    
    # Create a Twist message
    vel_msg = Twist()
    
    # Wait for publisher to connect
    rospy.sleep(1)

    # Function to move forward
    def move_forward(duration):
        vel_msg.linear.x = 0.1  # Forward speed
        vel_msg.angular.z = 0
        start_time = time.time()
        while time.time() - start_time < duration and not rospy.is_shutdown():
            velocity_publisher.publish(vel_msg)
            rospy.sleep(0.1)

    # Function to rotate
    def rotate(duration):
        vel_msg.linear.x = 0
        vel_msg.angular.z = 0.2  # Rotation speed
        start_time = time.time()
        while time.time() - start_time < duration and not rospy.is_shutdown():
            velocity_publisher.publish(vel_msg)
            rospy.sleep(0.1)

    # Function to stop
    def stop():
        vel_msg.linear.x = 0
        vel_msg.angular.z = 0
        velocity_publisher.publish(vel_msg)
        rospy.sleep(1)

    try:
        # Square movement pattern
        for i in range(4):
            #print(f"Side {i+1} of square")
            move_forward(3)  # Move forward for 3 seconds
            stop()
            print("Rotating...")
            rotate(3.3)      # Rotate for ~90 degrees
            stop()

        print("Square completed!")
        
    except rospy.ROSInterruptException:
        pass

    # Final stop
    stop()
    print("Movement finished")

if __name__ == '__main__':
    move_robot()
