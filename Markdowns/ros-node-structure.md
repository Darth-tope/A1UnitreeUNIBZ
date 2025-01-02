# ROS Node Structure and Communication Flow

## Active Nodes
1. /base_controller_node
   - Publications: /rosout
   - Subscriptions: /cmd_vel

2. /slam_planner_node
   - Publications:
     * /cmd_vel
     * /move_base/* (feedback, goal, result, status)
     * Costmap and planning topics
   - Subscriptions:
     * /map
     * /odom
     * /scan
     * /tf

3. /slamware_ros_sdk_server_node
   - Publications:
     * /map
     * /odom
     * /scan
     * /tf
   - Subscriptions:
     * Various control commands

4. Transform Publishers
   - /base2laser
   - /laser2foot
   - /map2odom

## Key Data Flows
1. Motion Control:
   slam_planner_node -> /cmd_vel -> base_controller_node -> Robot Hardware

2. Sensor Data:
   Robot Hardware -> slamware_ros_sdk_server_node -> (/scan, /map, /odom) -> slam_planner_node

3. Transform Chain:
   map -> odom -> base_link -> laser -> base_footprint
