#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
import time
import math

class ObstacleAvoidanceRobot:
    def __init__(self):
        # Initialize ROS node
        rospy.init_node('obstacle_avoidance', anonymous=True)
        
        # Publisher for robot motion
        self.cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        
        # Subscriber for laser data
        self.scan_sub = rospy.Subscriber('/scan', LaserScan, self.scan_callback)
        
        # Robot parameters
        self.forward_speed = 0.1  # m/s
        self.rotation_speed = 0.2  # rad/s
        self.min_distance = 0.5   # minimum distance to obstacle (meters)
        self.is_rotating = False   # Flag to track if robot is currently rotating
        self.start_time = time.time()
        self.duration = 60  # Run for 60 seconds (1 minute)
        
        # Initialize Twist message
        self.cmd = Twist()
        
        # Wait for laser scan data
        rospy.sleep(1)

    def scan_callback(self, scan_data):
        # Check front area for obstacles (assume front is around 0 degrees)
        # Get front ranges (use 30 degrees arc in front)
        front_ranges = scan_data.ranges[-15:] + scan_data.ranges[:15]
        
        # Filter out invalid readings
        front_ranges = [r for r in front_ranges if not math.isinf(r) and not math.isnan(r)]
        
        if front_ranges:
            min_front_distance = min(front_ranges)
            rospy.loginfo(f"Minimum front distance: {min_front_distance}")
            
            if min_front_distance < self.min_distance:
                # Obstacle detected - stop and rotate
                self.is_rotating = True
                self.cmd.linear.x = 0.0
                self.cmd.angular.z = self.rotation_speed  # Rotate clockwise
                rospy.loginfo("Obstacle detected! Rotating...")
            
            elif self.is_rotating:
                # Complete 90-degree rotation (approximately)
                self.cmd.linear.x = 0.0
                self.cmd.angular.z = self.rotation_speed
                rospy.sleep(math.pi/4/self.rotation_speed)  # Time to rotate 90 degrees
                self.is_rotating = False
                rospy.loginfo("Rotation complete, moving forward...")
            
            else:
                # No obstacle - move forward
                self.cmd.linear.x = self.forward_speed
                self.cmd.angular.z = 0.0
                rospy.loginfo("Moving forward...")

    def run(self):
        rate = rospy.Rate(10)  # 10 Hz
        
        rospy.loginfo("Starting obstacle avoidance for 1 minute...")
        
        while not rospy.is_shutdown():
            # Check if time is up
            if time.time() - self.start_time > self.duration:
                rospy.loginfo("Time's up! Stopping robot...")
                # Stop the robot
                self.cmd.linear.x = 0.0
                self.cmd.angular.z = 0.0
                self.cmd_vel_pub.publish(self.cmd)
                break
                
            # Publish command
            self.cmd_vel_pub.publish(self.cmd)
            rate.sleep()

if __name__ == '__main__':
    try:
        robot = ObstacleAvoidanceRobot()
        robot.run()
    except rospy.ROSInterruptException:
        pass
