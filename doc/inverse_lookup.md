# 逆引き (Inverse Lookup)

## bagファイルのデータをプロットしたい
やり方は4パターン.

1. `rosbag play`しながら[rqt_plot](https://ros.org/wiki/rqt_plot)を利用する。
2. [rqt_bag](https://ros.org/wiki/rqt_plot)を利用してプロットする。
3. [jsk_topic_toolsのbag2csv.py](https://github.com/jsk-ros-pkg/jsk_common/blob/master/jsk_topic_tools/scripts/bag2csv.py)を利用して一度csvに変換する。
4. [jsk_dataのbag_plotter.py](http://jsk-docs.readthedocs.org/en/latest/jsk_common/doc/jsk_tools/cltools/bag_plotter.html)を利用してbagファイルから直接プロットする。

## bagファイルを右クリックからプロットしたい
[nautilus-scripts](https://doc.ubuntu-fr.org/nautilus_scripts)という枠組みを利用します。

JAXONなら[ここ](https://github.com/jsk-ros-pkg/trans_system/blob/master/jaxon_ros_bridge/README.md#bagファイルのplot)を参考にしてください。

## `geometry_msgs/PoseStamped`にオフセットを加えたい
[jsk_topic_toolsのstatic_transform_pose_stamped](https://github.com/jsk-ros-pkg/jsk_common/blob/master/jsk_topic_tools/src/static_transform_pose_stamped.cpp)を利用する。

## rvizにプランニング途中のロボットモデルなどを表示したい。
2つのパターン。

1. `moveit_msgs/DisplayRobotState`を利用する.
2. jsk_interactive_markerのurdf_model_markerを利用する.

## rvizの動画を保存したい
[参考](https://jsk-visualization.readthedocs.org/en/latest/tips/index.html#record-rviz)

## ZMPやCapture Pointを可視化したい
[jsk_footstep_controllerのfootstep_visualizer.py](https://github.com/jsk-ros-pkg/jsk_control/blob/master/jsk_footstep_controller/scripts/footstep_visualizer.py)を利用する.
