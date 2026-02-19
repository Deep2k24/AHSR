import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue # <-- New import!

def generate_launch_description():
    # Package Directories
    pkg_shopmate_description = get_package_share_directory('shopmate_bot_description')
    pkg_rplidar = get_package_share_directory('rplidar_ros')

    # 1. Process the URDF file
    # [FIX 1: Pointing to the exact file name in your repo]
    xacro_file = os.path.join(pkg_shopmate_description, 'urdf', 'shopmate_bot.urdf.xacro')
    
    # [FIX 2: Wrapping the Command in ParameterValue for ROS 2 Jazzy]
    robot_description = {'robot_description': ParameterValue(Command(['xacro ', xacro_file]), value_type=str)}

    # RViz Configuration Path
    rviz_config_path = os.path.join(pkg_shopmate_description, 'config', 'display.rviz')

    # 2. Robot State Publisher (Loads the TF tree for the real robot)
    rsp_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[robot_description, {'use_sim_time': False}] 
    )

    # 3. RPLidar C1 Node
    lidar_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_rplidar, 'launch', 'rplidar_c1_launch.py')
        ),
        launch_arguments={
            'serial_port': '/dev/ttyUSB0', 
            'frame_id': 'lidar_link_1'
        }.items()
    )

    # 4. RViz2 Node
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config_path],
        parameters=[{'use_sim_time': False}] 
    )

    return LaunchDescription([
        rsp_node,
        lidar_launch,
        rviz_node
    ])