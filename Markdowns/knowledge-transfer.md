# Unitree A1 ROS Navigation Project Knowledge Transfer

## Project Overview
Working on ROS navigation and visualization for a Unitree A1 quadruped robot, focusing on:
- Interactive marker control
- 2D navigation goals
- Path planning and visualization
- Robot state visualization

## Key Files and Modifications

### 1. Launch Files
- `slam_rplidar_start.launch`: Base launch file for SLAM and basic robot functionality
- `slam_planner_online.launch`: Navigation stack integration

### 2. Python Scripts
- `robot_marker_control.py`: Handles interactive markers and navigation goals
- `trajectory_tracker.py`: (Proposed) For tracking robot's actual path
- `robot_visualization.py`: Handles robot state visualization

### 3. Configuration Files
Location: `~/catkin_ws/src/slamrplidar/slamplanner/`
- `params/base_local_planner_params.yaml`
- `params/costmap_common_params.yaml`
- `params/local_costmap_params.yaml`
- `params/global_costmap_params.yaml`

## Key Functionalities Implemented

### Interactive Marker Control
- Added marker-based robot control
- Implemented 'O' for move and 'X' for stop commands
- Added goal visualization markers

### Navigation Integration
- Integrated move_base action client
- Added path visualization
- Implemented goal reaching behavior
- Added marker cleanup on goal completion

## Current Issues and Solutions

### 1. VNC Display Resolution
Solution: Add to `/etc/X11/xorg.conf`:
```
Section "Screen"
    Identifier "Screen0"
    DefaultDepth 24
    SubSection "Display"
        Depth 24
        Modes "1920x1080"
        Virtual 1920 1080
    EndSubSection
EndSection
```

### 2. Navigation Parameters
Key areas for tuning:
```yaml
TrajectoryPlannerROS:
  max_vel_theta: 0.5
  min_vel_theta: 0.1
  max_rotational_vel: 0.5
  yaw_goal_tolerance: 0.1
  xy_goal_tolerance: 0.15
  latch_xy_goal_tolerance: true
```

## Project Dependencies
- ROS Melodic
- Unitree Legged SDK
- slam_planner package
- move_base
- interactive_markers
- visualization_msgs

## Network Configuration
- Robot IP: 192.168.123.12
- Uses ROS network setup for communication

## Useful Commands
```bash
# Building the workspace
cd ~/catkin_ws
catkin build
source devel/setup.bash

# Running the system
roslaunch slam_planner slam_rplidar_start.launch

# Checking node communication
rostopic list
rostopic echo /robot_joint_states
rosnode info /base_controller_node
```

## Next Steps and Improvements
1. Implement trajectory tracking
2. Tune navigation parameters
3. Add multi-waypoint navigation
4. Improve goal reaching behavior
5. Add recovery behaviors

## Known Issues
1. Robot sometimes spins at goal positions
2. VNC display resolution needs manual setting
3. Interactive marker control can conflict with RViz controls

## Required RViz Configuration
1. Add Marker display for goal visualization
2. Add Path display for planned path
3. Add InteractiveMarkers display
4. Configure robot model visualization

## Useful Resources
- Unitree ROS documentation
- ROS Navigation stack documentation
- Interactive Markers tutorial
- move_base documentation

This knowledge should allow continuation of the project with the same level of understanding. Additional code and configuration files can be found in the repository structure detailed above.
