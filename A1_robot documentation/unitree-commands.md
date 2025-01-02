# Unitree Robot Command Reference Guide

## Initial Setup and Dependencies
```bash
# Check SDK Version
echo $UNITREE_SDK_VERSION    # Should show 3_2
echo $UNITREE_PLATFORM       # Should show arm64 for A1 robot

# SDK Location check
ls ~/unitree_legged_sdk
ls ~/unitree_legged_sdk/lib/
```

## Build System Configuration
```bash
# Initial workspace setup
cd ~/catkin_ws
catkin clean

# Build order (important!)
catkin build unitree_legged_msgs  # Build messages first
catkin build unitree_legged_real  # Build main package
source devel/setup.bash

# Debug build configuration
catkin config -DCMAKE_BUILD_TYPE=Debug
catkin build

# Check package presence
rospack list | grep unitree
rosmsg list | grep High
```

## Network Configuration and Troubleshooting
```bash
# Check interfaces
ifconfig

# Robot network settings
sudo nano /etc/network/interfaces
# Content:
auto eth0
iface eth0 inet static
    address 192.168.123.10
    netmask 255.255.255.0
    gateway 192.168.123.1
    dns-nameservers 8.8.8.8 8.8.4.4

# Check connections
ping 192.168.123.1    # Router
ping 192.168.123.10   # Robot
ping 8.8.8.8          # Internet

# Monitor network traffic
sudo tcpdump -i eth0 port 8080
sudo netstat -tupln | grep UDP
```

## LCM System
```bash
# LCM Installation (version 1.4.0)
git clone https://github.com/lcm-proj/lcm.git
cd lcm
git checkout v1.4.0
mkdir build
cd build
cmake ..
make
sudo make install

# LCM Tools
lcm-logger output.lcm    # Record data
lcm-logplayer output.lcm # Playback
lcm-spy                  # Monitor channels

# Check LCM environment
echo $LCM_DEFAULT_URL
export LCM_DEFAULT_URL="udpm://239.255.76.67:7667?ttl=1"
```

## Running the Robot System
```bash
# Terminal 1 - ROS Core
roscore

# Terminal 2 - LCM-ROS Bridge
sudo su
source /home/unitree/catkin_ws/devel/setup.bash
rosrun unitree_legged_real lcm_ros_bridge a1 --ros-args --log-level debug

# Terminal 3 - Topic Monitoring
rostopic list
rostopic echo /unitree_legged_msgs/HighCmd
rostopic echo /unitree_legged_msgs/HighState
rostopic hz /unitree_legged_msgs/HighCmd

# Terminal 4 - Walk Control
sudo su
source /home/unitree/catkin_ws/devel/setup.bash
rosrun unitree_legged_real walk_lcm
```

## Debug and Monitoring
```bash
# ROS debugging
rosnode list
rosnode info /node_lcm_server
rostopic info /unitree_legged_msgs/HighCmd
rostopic info /unitree_legged_msgs/HighState

# Process monitoring
ps aux | grep lcm
ps aux | grep ros

# Check message flow
rostopic hz /unitree_legged_msgs/HighCmd
rostopic type /unitree_legged_msgs/HighCmd
```

## Common Issues and Solutions
1. Network Connectivity:
   - Check physical connections
   - Verify IP configurations
   - Test with ping
   - Monitor with tcpdump

2. Message Flow Issues:
   - Verify topic existence with rostopic list
   - Check subscribers/publishers with rostopic info
   - Monitor message rate with rostopic hz
   - Use lcm-spy for LCM verification

3. Build Issues:
   - Build messages package first
   - Check package dependencies
   - Verify SDK version and platform
   - Use debug build for more information

4. Robot Control:
   - Verify standing position before commands
   - Check mode settings (1 for body adjustment, 2 for motion)
   - Monitor UDP communication
   - Verify LCM message conversion

## Code Modification Locations
```bash
# Main configuration files
~/catkin_ws/src/unitree_ros_to_real/unitree_legged_real/include/convert.h
~/catkin_ws/src/unitree_ros_to_real/unitree_legged_real/src/exe/walk_mode.cpp
~/catkin_ws/src/unitree_ros_to_real/unitree_legged_real/src/bridge/lcm_ros_bridge.cpp
```

Would you like me to add anything else or expand on any particular section?