#!/bin/bash
cd ~/RobotVisionSystem/ 
./build/RobotVisionSystem -i "./build/Src/SystemInputPlugin/vision.so -fps 30" -o "./build/Src/SystemOutputPlugin/httpd.so -w ./WWW/"
