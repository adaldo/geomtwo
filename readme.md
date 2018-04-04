# Geomtwo
A wanna-be Python package to handle planar geometry messages with ROS and `rospy`.

## Installation
The package targets modern Ubuntu platforms.
I am not sure if/how it is possible to install it on a different OS.
These instructions assume that you have a recent Ubuntu OS, and that you have ROS, Catkin and `python-catkin-tools` installed.

- Clone this repository in your catkin workspace
```
cd <your-catkin-workspace>/src
git clone https://github.com/adaldo/geomtwo
```
- Make and source
```
cd <your-catkin-workspace>
catkin build
source ./devel/setup.bash
```

## Provided messages
At the moment, the package provides the following messages:
- `Point`;
- `Vector`;
- `Versor`
- `Pose`;
- `Transform`;
- `Twist`.
Each message type corresponds to a python class, which comes with a bunch of functions to perform common operations.

## Demo
Type one of the following in a terminal:
- `roslaunch geomtwo test_point.launch`
- `roslaunch geomtwo test_pose.launch`

## Uninstall
- Just delete the `geomtwo` folder generated when cloning the repository.
- Write a mail to antonio.adaldo.89@gmail.com and let me know what went wrong.
