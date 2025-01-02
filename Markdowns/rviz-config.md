# RViz Configuration Guide

## Basic Setup
1. Fixed Frame: "map"
2. Grid: Enabled
   - Plane Cell Count: 10
   - Normal Cell Count: 0
   - Cell Size: 1
   - Line Style: Lines
   - Color: 160, 160, 164

## Required Displays
1. Map
   - Topic: /map
   - Color Scheme: map
   - Update Rate: 1

2. LaserScan
   - Topic: /scan
   - Style: Points
   - Size: 0.05m

3. TF
   - Show Arrows: true
   - Show Axes: true
   - Show Names: true

4. Robot Model (if available)
   - Robot Description: robot_description
