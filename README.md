nao_teleop_gamepad_addon
========================

**This is a rosbuild package!**

This special version of nao_teleop currently maps button 4 on the gamepad to the object pickup motion (works best with a cube).
To drop the object, simply press button 1 to go into the initial position.  
Other pickup/drop motions have been disabled due to them not being reliable / the robot falling during motion execution.

Install:
* remove old nao_teleop
* git clone https://github.com/sboettcher/nao_teleop_gamepad_addon.git nao_teleop
* roscd nao_teleop
* rosmake
* roslaunch nao_teleop gamepad_addon.launch
