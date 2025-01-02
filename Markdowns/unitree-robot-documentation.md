# UNITREE A1 ROBOT - COMPLETE SYSTEM DOCUMENTATION

## SYSTEM ARCHITECTURE
### Overview
```
Development Machine (192.168.123.254) ─── SSH ──→ Robot (192.168.123.10)
                                                  ├── ROS Core
                                                  ├── LCM Bridge
                                                  │   └── UDP (8080/8007)
                                                  ├── Walk LCM Controller
                                                  └── Robot Control System
```

### Communication Flow
```
┌─────────────────────── Robot System ───────────────────────┐
│                                                           │
│  ┌─────────┐    ┌──────────┐    ┌──────────┐    ┌─────┐  │
│  │ROS Core │◄──►│Walk_LCM  │◄──►│LCM Bridge│◄──►│Robot│  │
│  └─────────┘    └──────────┘    └──────────┘    └─────┘  │
│                                      │                     │
│                                   UDP 8080                 │
│                                   UDP 8007                 │
└───────────────────────────────────────────────────────────┘
```

## NETWORK CONFIGURATION
### Current Settings
```bash
# Robot Network
IP: 192.168.123.10
Gateway: 192.168.123.2 (changed from .1)
Netmask: 255.255.255.0

# Development Machine
IP: 192.168.123.254
Gateway: 192.168.123.2
```

### Network Setup Commands
```bash
# Check interfaces
ifconfig eth0

# Modify network settings
sudo nano /etc/network/interfaces
auto eth0
iface eth0 inet static
    address 192.168.123.10
    netmask 255.255.255.0
    gateway 192.168.123.2
    dns-nameservers 8.8.8.8 8.8.4.4

# Apply changes
sudo systemctl restart networking
# or
sudo ifdown eth0 && sudo ifup eth0
```

## SOFTWARE SETUP
### SDK Installation
```bash
# Clone specific version
cd ~
git clone https://github.com/unitreerobotics/unitree_legged_sdk.git
cd unitree_legged_sdk
git checkout v3.2

# Build SDK
mkdir build
cd build
cmake ..
make
```

### ROS Workspace Setup
```bash
cd ~/catkin_ws
catkin clean
catkin build unitree_legged_msgs
catkin build unitree_legged_real
source devel/setup.bash
```

## LAUNCH SEQUENCE
### 1. Prerequisites
```bash
# SSH into robot
ssh unitree@192.168.123.10

# Check network
ping 192.168.123.2
ping 8.8.8.8
```

### 2. Start Systems
```bash
# Terminal 1: ROS Core
roscore

# Terminal 2: UDP Monitor
sudo tcpdump -vvv -i eth0 'port 8080 or port 8007'

# Terminal 3: Bridge
sudo su
source /home/unitree/catkin_ws/devel/setup.bash
rosrun unitree_legged_real lcm_ros_bridge a1

# Terminal 4: Walk Control
sudo su
source /home/unitree/catkin_ws/devel/setup.bash
rosrun unitree_legged_real walk_lcm
```

## DEBUGGING
### Common Issues and Solutions
1. Network Connectivity
```bash
# Check gateway
route -n
# Fix routes if needed
sudo ip route del default
sudo ip route add default via 192.168.123.2 dev eth0
```

2. UDP Communication
```bash
# Test local UDP
nc -ul 8080
echo "test" | nc -u localhost 8080

# Monitor traffic
sudo tcpdump -i lo udp
sudo tcpdump -i eth0 udp
```

3. Process Status
```bash
# Check running processes
ps aux | grep ros
ps aux | grep lcm

# Check ports
sudo ss -upn
sudo netstat -tulnp | grep '8080\|8007'
```

### Known Issues
1. UDP Port Conflicts
- Solution: Kill conflicting processes
```bash
sudo pkill -f RobotVisi
```

2. Build Errors
- ARM64/AMD64 library mismatch
- Solution: Use correct library in CMakeLists.txt
```cmake
set(EXTRA_LIBS -pthread libunitree_legged_sdk_arm64.so lcm)
```

## CODE MODIFICATIONS
### LCM Bridge Debug Prints
```cpp
// In constructor
std::cout << "UDP Details:" << std::endl;
std::cout << " - Target IP: " << server_->udp.targetIP << std::endl;
std::cout << " - Local Port: " << server_->udp.localPort << std::endl;
std::cout << " - Target Port: " << server_->udp.targetPort << std::endl;
```

### Walk Mode Subscriber Info
```cpp
if(motiontime % 500 == 0) {
    std::cout << "\n=== Publishing to ROS ===" << std::endl;
    std::cout << "Publishing to topic: " << cmd_pub.getTopic() << std::endl;
    std::cout << "Number of subscribers: " << cmd_pub.getNumSubscribers() << std::endl;
    
    XmlRpc::XmlRpcValue args, result, payload;
    args[0] = ros::this_node::getName();
    args[1] = cmd_pub.getTopic();
    if (ros::master::execute("getSystemState", args, result, payload, true)) {
        auto subscribers = result[2][1][1];
        std::cout << "Subscribers: ";
        for (int i = 0; i < subscribers.size(); ++i) {
            std::cout << subscribers[i] << " ";
        }
        std::cout << std::endl;
    }
}
```

## REFERENCE
### Important Files
```
~/catkin_ws/src/unitree_ros_to_real/unitree_legged_real/
├── src/
│   ├── bridge/
│   │   └── lcm_ros_bridge.cpp
│   └── exe/
│       └── walk_mode.cpp
└── include/

~/unitree_legged_sdk/
├── include/
│   └── unitree_legged_sdk/
│       ├── udp.h
│       └── lcm_server.h
└── lib/
```

### Critical Commands
```bash
# Build
catkin build unitree_legged_real

# Debug
sudo tcpdump -i eth0 udp
rostopic list
rostopic echo /unitree_legged_msgs/HighCmd
```
