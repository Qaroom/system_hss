
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription ,AppendEnvironmentVariable
from launch.conditions import IfCondition, UnlessCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, FindExecutable, PathJoinSubstitution, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():

    pkg_share = get_package_share_directory('system_hss')
    yaml_path = os.path.join(pkg_share, 'config', 'hssconfig.yaml')
    set_env_vars_resources = AppendEnvironmentVariable(
        'GZ_SIM_RESOURCE_PATH',
        os.path.dirname(pkg_share)
    )

    # Declare arguments
    declared_arguments = []
    declared_arguments.append(
        DeclareLaunchArgument(
            "gui",
            default_value="true",
            description="Start RViz2 automatically with this launch file.",
        )
    )

    # Initialize Arguments
    gui = LaunchConfiguration("gui")

    # gazebo
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [FindPackageShare("ros_gz_sim"), "/launch/gz_sim.launch.py"]
        ),
        launch_arguments=[("gz_args", f" -r -v 3  {pkg_share}/launch/system_gazebo.sdf")],
        condition=IfCondition(gui),
    )
    gazebo_headless = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [FindPackageShare("ros_gz_sim"), "/launch/gz_sim.launch.py"]
        ),
        launch_arguments=[("gz_args", [f"--headless-rendering -s -r -v 3 {pkg_share}/launch/system_gazebo.sdf"])],
        condition=UnlessCondition(gui),
    )

    # Gazebo bridge
    # gazebo_bridge = Node(
    #     package="ros_gz_bridge",
    #     executable="parameter_bridge",
    #     arguments=["/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock"],
    #     output="screen",
    # )

    gazebo_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=['--ros-args','-p', f'config_file:={yaml_path}'],
        output='screen'
        )

    gz_spawn_entity = Node(
        package="ros_gz_sim",
        executable="create",
        output="screen",
        arguments=[
            "-topic",
            "/robot_description",
            "-name",
            "system_hss_position",
            "-allow_renaming",
            "true",
        ],
    )

    # Get URDF via xacro
    robot_description_content = Command(
        [
            PathJoinSubstitution([FindExecutable(name="xacro")]),
            " ",
            PathJoinSubstitution(
                [FindPackageShare("system_hss"), "urdf", "system_hss_.urdf.xacro"]
            ),
            " ",
            "use_gazebo:=true",
        ]
    )
    robot_description = {"robot_description": robot_description_content}

    robot_controllers = PathJoinSubstitution(
        [
            FindPackageShare("system_hss"),
            "config",
            "ros2_controllers_with_trajctory.yaml",
        ]
    )
    robot_controllers2 = PathJoinSubstitution(
        [
            FindPackageShare("system_hss"),
            "config",
            "ros2_controllers.yaml",
        ]
    )
    pkg_share_rviz = get_package_share_directory('system_hss')
    # rviz_config_file = os.path.join(pkg_share_rviz, 'rviz', 'xacroconfigration.rviz')

    rviz_config_file = f"{pkg_share_rviz}/rviz/xacroconfigration.rviz"

    node_robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[robot_description],
    )

    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster", "--param-file", robot_controllers2],
    )
    

    # trajectory_controller_spawner = Node(
    #     package="controller_manager",
    #     executable="spawner",
    #     arguments=["joint_trajectory_controller", "--param-file", robot_controllers],
    # )


    # robot_controller_spawner = Node(
    #     package="controller_manager",
    #     executable="spawner",
    #     arguments=["forward_position_controller", "--param-file", robot_controllers],
    # )
    velocity_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["forward_velocity_controller", "--param-file", robot_controllers2],
    )
    controller_manager_node = Node(
        package='controller_manager',
        executable='ros2_control_node',
        parameters=[robot_controllers],  # yaml dosyan
        output='screen'
    )

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="log",
        arguments=["-d", rviz_config_file],
        condition=IfCondition(gui),
    )
    

    nodes = [
        set_env_vars_resources,
        gazebo,
        gazebo_headless,
        gazebo_bridge,
        node_robot_state_publisher,
        gz_spawn_entity,
        controller_manager_node,
        joint_state_broadcaster_spawner,
        # robot_controller_spawner,
        # trajectory_controller_spawner,
        rviz_node,
        velocity_controller_spawner,
    ]

    return LaunchDescription(declared_arguments + nodes)






