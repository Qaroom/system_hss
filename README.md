# system_hss

A ROS 2 package that brings together URDF modeling, Gazebo simulation, `ros2_control`, and RViz visualization.

## Contents

| Folder | Description |
|---|---|
| `urdf/` | URDF / Xacro definitions of the robot |
| `meshes/` | 3D model files (visual and collision meshes) |
| `gazebo/` | Gazebo simulation worlds and plugin configurations |
| `ros2_control/` | `ros2_control` controller configurations |
| `rviz/` | Ready-to-use RViz visualization configs |
| `config/` | Additional parameter files |
| `launch/` | ROS 2 launch files |

## Requirements

- ROS 2 (Humble or later recommended)
- Gazebo (`gazebo_ros` / `ros_gz_bridge`)
- The following packages:
  - `robot_state_publisher`
  - `joint_state_publisher`
  - `xacro`
  - `ros2_control` and its controllers

On Ubuntu, install the core dependencies with:

```bash
sudo apt install ros-$ROS_DISTRO-robot-state-publisher \
                 ros-$ROS_DISTRO-joint-state-publisher \
                 ros-$ROS_DISTRO-xacro \
                 ros-$ROS_DISTRO-gazebo-ros-pkgs \
                 ros-$ROS_DISTRO-ros-gz-bridge \
                 ros-$ROS_DISTRO-ros2-control \
                 ros-$ROS_DISTRO-ros2-controllers
```

## Installation

Clone the package into your ROS 2 workspace and build it:

```bash
cd ~/ros2_ws/src
git clone https://github.com/Qaroom/system_hss.git
cd ~/ros2_ws
colcon build --packages-select system_hss
source install/setup.bash
```

## Usage

Run one of the launch files included in the package:

```bash
ros2 launch system_hss <launch_file>.launch.py
```

Pick the appropriate file from the `launch/` folder depending on what you want to start (e.g. Gazebo simulation, RViz visualization, or bringing up `ros2_control`).

## License

This project is released under the [MIT License](LICENSE).  
Copyright (c) 2026 Akram Al Qasemi