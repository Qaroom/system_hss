import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
import xacro

def generate_launch_description():
    # this is the robot name in the Xacro file
    robotXacroName='system_hss'

    # this is the name of our package
    packageName = 'system_hss'
    # this is the robot name in the Xacro file
    roboFilePath = "/home/ros2/Desktop/ros_ws/src/system_hss/urdf/system_hss.urdf"
    rviz_path="/home/ros2/Desktop/ros_ws/src/firstrobot/rviz/xacroconfigration.rviz"
    yaml_path  = "/home/ros2/Desktop/ros_ws/src/system_hss/config/hssconfig.yaml"

    robotDescription = xacro.process_file(roboFilePath).toxml()

    gazebo_rosPackageLaunch = PythonLaunchDescriptionSource (os.path.join
                                                             (get_package_share_directory('ros_gz_sim'),'launch','gz_sim.launch.py'))
    
    # this is the launch description
    # loading empty world model
    gazeboLaunch = IncludeLaunchDescription (gazebo_rosPackageLaunch, 
                                             launch_arguments={'gz_args': ['-r -v -v4 empty.sdf '],'on_exit_shutdown': 'true'}.items())

    
    spawnModelNodeGazebo = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=['-name', robotXacroName, '-string', robotDescription],
        output='screen',
    )

    robot_description = {'robot_description': ParameterValue(robotDescription, value_type=str)}
    
    # Robot State Publisher Node
    nodeRobotStatePublisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[robot_description, {'use_sim_time': True}],
        output='screen'
    )

    # # gazebo ros bridging
    # bridge_params = os.path.join(get_package_share_directory(packageName),'config','diff_drive_controller.yaml')

    start_gazebo_ros_bridge_cmd = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=['--ros-args','-p', f'config_file:={yaml_path}'],
        output='screen'
        )
    
    joint_state_publisher_node = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui"
    )

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        arguments=['-d', rviz_path],
        parameters=[{'use_sim_time': True}]
    )

    scan_fixer_node = Node(
        package="testpkg",
        executable="republisherlazer",
        parameters=[{'use_sim_time': True}],
        output="screen"
    )

    static_tf_node = Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        name="map_to_odom_broadcaster",
        arguments=["0", "0", "0", "0", "0", "0", "map", "odom"],
        output="screen"
    )

    gz_ros2_control = Node(
        package="gz_ros2_control",
        executable="gz_ros2_control",
        output="screen",
        parameters=[{'robot_description': robotDescription,
                    'use_sim_time': True},
                    "/home/ros2/Desktop/ros_ws/src/system_hss/config/ros2_controllers.yaml"]
    )


    # joint_state_broadcaster spawner
    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster"],
        output="screen"
    )

    # joint_trajectory_controller spawner
    forward_position_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["forward_position_controller"],
        output="screen"
    )




 
    # here we create an empty launch description object 
    launchDescriptionObject = LaunchDescription()
    # we add gazeboLaunch
    launchDescriptionObject.add_action(gazeboLaunch)
    # we add the two nodes
    launchDescriptionObject.add_action(spawnModelNodeGazebo)
    launchDescriptionObject.add_action(nodeRobotStatePublisher)
    launchDescriptionObject.add_action(start_gazebo_ros_bridge_cmd)
    launchDescriptionObject.add_action(joint_state_publisher_node)
    launchDescriptionObject.add_action(rviz_node)
    launchDescriptionObject.add_action(scan_fixer_node)
    launchDescriptionObject.add_action(static_tf_node)
    launchDescriptionObject.add_action(gz_ros2_control)
    launchDescriptionObject.add_action(joint_state_broadcaster_spawner)
    launchDescriptionObject.add_action(forward_position_controller_spawner)



    
    return launchDescriptionObject