# Robot Configuration Settings

## Navigation Parameters
- Robot Parameters:
  * Radius: 0.2m
  * Max velocity: 0.3 m/s
  * Min velocity: 0.1 m/s
  * Max rotation: 0.8 rad/s
  * Map resolution: 0.05m

## Critical Topics
1. Motion Control:
   - /cmd_vel: Robot velocity commands
   - /move_base/*: Navigation commands and feedback

2. Sensor Data:
   - /scan: Laser scanner data
   - /map: Environment map
   - /odom: Robot odometry
   - /tf: Transform tree

## Launch File Parameters
1. SLAM Server:
   - IP: 192.168.11.1
   - Fixed frames: map, odom, base_link, laser
   - Update frequencies:
     * Map: 0.1 Hz
     * Scan: 0.1 Hz
     * Robot pose: 0.05 Hz

2. Navigation:
   - Global costmap update: 3.0 Hz
   - Local costmap update: 3.0 Hz
   - Controller frequency: 3.0 Hz
