#!/usr/bin/env python

"""
Copyright 2013 by Sebastian Boettcher
"""


import roslib
roslib.load_manifest('nao_teleop')
import rospy

import logging
logging.basicConfig()


from nao_driver import *

from nao_teleop.srv import *
from std_srvs.srv import *

import recm_pickup_cube
import recm_drop_cube
import recm_pickup_bucket_right_3
import recm_drop_bucket_right_2

class NaoTidyupGamepadService(NaoNode):
  def __init__(self):
    NaoNode.__init__(self)
    rospy.init_node('nao_tidyup_gamepad_service')

    motionServiceName = rospy.get_param("/nao_tidyup_gamepad_service", '/nao_tidyup_gamepad_service')

    motion = rospy.Service(motionServiceName, nao_motion, self.motionCB)

    rospy.wait_for_service("/read_foot_gait_config_srv")
    self.footgait_service = rospy.ServiceProxy("/read_foot_gait_config_srv", Empty)

    self.mp = self.getProxy("ALMotion")
    if self.mp is None:
      rospy.logerr("Could not get proxy to ALMotion, exit")
      exit(1)

    self.mp.setWalkArmsEnabled(True, True)
    self.armsEnabled = True

    rospy.loginfo("tidyup gamepad service ready")

  def motionCB(self, req):

    if req.motion == 'pickup_cube':
      rospy.loginfo("picking up cube")
      recm_pickup_cube.exec_pickup_cube(self.mp)

      gaitConfig = self.mp.getFootGaitConfig("Default")
      gaitConfig[6] = ["TorsoWy", -0.122]
      rospy.set_param('/nao_walker/use_foot_gait_config', True)
      rospy.set_param('/nao_walker/foot_gait_config', gaitConfig)
      try:
        self.srvResponse = self.footgait_service()
      except rospy.ServiceException, e:
        rospy.logerr("Service call to nao_walker (footGaitConfig) failed: %s", e)

      self.arms(False)
      self.mp.angleInterpolationWithSpeed("HeadPitch", -0.672, 0.1)
    elif req.motion == 'drop_cube':
      rospy.loginfo("dropping cube")
      recm_drop_cube.exec_drop_cube(self.mp)

      self.mp.angleInterpolationWithSpeed("HeadPitch", 0.0, 0.1)
      rospy.set_param('/nao_walker/use_foot_gait_config', False)
      try:
        self.srvResponse = self.footgait_service()
      except rospy.ServiceException, e:
        rospy.logerr("Service call to nao_walker (footGaitConfig) failed: %s", e)

      self.arms(True)
    elif req.motion == 'pickup_bucket':
      if self.armsEnabled == False:
        self.arms(True)
      elif self.armsEnabled == True:
        rospy.loginfo("picking up bucket")
        recm_pickup_bucket_right_3.exec_pickup_bucket_right(self.mp)

        gaitConfig = self.mp.getFootGaitConfig("Default")
        gaitConfig[6] = ["TorsoWy", -0.090]
        rospy.set_param('/nao_walker/use_foot_gait_config', True)
        rospy.set_param('/nao_walker/foot_gait_config', gaitConfig)
        try:
          self.srvResponse = self.footgait_service()
        except rospy.ServiceException, e:
          rospy.logerr("Service call to nao_walker (footGaitConfig) failed: %s", e)

        self.arms(False)
        self.mp.angleInterpolationWithSpeed("HeadPitch", -0.0, 0.1)
    elif req.motion == 'drop_bucket':
      rospy.loginfo("dropping bucket")
      recm_drop_bucket_right_2.exec_drop_bucket_right(self.mp)

      self.mp.angleInterpolationWithSpeed("HeadPitch", 0.0, 0.1)
      rospy.set_param('/nao_walker/use_foot_gait_config', False)
      try:
        self.srvResponse = self.footgait_service()
      except rospy.ServiceException, e:
        rospy.logerr("Service call to nao_walker (footGaitConfig) failed: %s", e)

      self.arms(True)
    # elif req.motion == 'arms':
    #   if self.armsEnabled == True:
    #     rospy.loginfo("arms disabled")
    #     self.arms(False)
    #   else:
    #     rospy.loginfo("arms enabled")
    #     rospy.set_param('/nao_walker/use_foot_gait_config', False)
    #     try:
    #       self.srvResponse = self.footgait_service()
    #     except rospy.ServiceException, e:
    #       rospy.logerr("Service call to nao_walker (footGaitConfig) failed: %s", e)
    #     self.arms(True)


    return {'success': True}


  def arms(self, enable):
    self.mp.setWalkArmsEnabled(enable, enable)
    self.armsEnabled = enable



if __name__ == "__main__":
  obj = NaoTidyupGamepadService()
  rospy.spin()

  exit(0)
