import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import SetEnvironmentVariable
from launch_ros.actions import Node
import xacro

def generate_launch_description():
    pkg = get_package_share_directory("robot_description")
    pkg_gz = get_package_share_directory("ros_gz_sim")
    soft_gl = SetEnvironmentVariable("LIBGL_ALWAYS_SOFTWARE", "1")

    # --- Gazebo world with SDF robot ---
    world = os.path.join(pkg, "worlds", "industrial-warehouse.sdf")
    set_res = SetEnvironmentVariable(
        "GZ_SIM_RESOURCE_PATH",
        os.path.join(pkg, "models")
    )
    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gz, "launch", "gz_sim.launch.py")),
        launch_arguments={"gz_args": world}.items()
    )

    # --- URDF/Xacro for RViz/TF ---
    #xacro_path = os.path.join(pkg, "urdf", "rescue_robot.xacro")
    #robot_desc = xacro.process_file(xacro_path).toxml()
    #rsp = Node(
    #    package="robot_state_publisher",
    #    executable="robot_state_publisher",
    #    parameters=[{"use_sim_time": True}, {"robot_description": robot_desc}],
    #)
    #jsp = Node(
    #    package="joint_state_publisher",
    #    executable="joint_state_publisher",
    #    parameters=[{"use_sim_time": True}],
    #)

    # --- Bridge config ---
    bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        parameters=[{
            "config_file": os.path.join(pkg, "config", "ros_gz_bridge.yaml"),
            "qos_overrides./tf_static.publisher.durability": "transient_local",
        }],
        output="screen"
    )

    # --- RViz config ---
    #rviz_config = os.path.join(pkg, "rviz", "navigation_config.rviz")
    #rviz = Node(
    #    package="rviz2",
    #    executable="rviz2",
    #    arguments=["-d", rviz_config],
    #    parameters=[{"use_sim_time": True}],
    #)

    #return LaunchDescription([soft_gl, set_res, gz_sim, rsp, jsp, bridge, rviz])
    return LaunchDescription([soft_gl, set_res, gz_sim, bridge])
