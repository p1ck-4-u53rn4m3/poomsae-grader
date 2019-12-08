import json
import math
import numpy as np

BODY_25 = {
    "Nose": 0,
    "Neck": 1,
    "RShoulder": 2,
    "RElbow": 3,
    "RWrist": 4,
    "LShoulder": 5,
    "LElbow": 6,
    "LWrist": 7,
    "MidHip": 8,
    "RHip": 9,
    "RKnee": 10,
    "RAnkle": 11,
    "LHip": 12,
    "LKnee": 13,
    "LAnkle": 14,
    "REye": 15,
    "LEye": 16,
    "REar": 17,
    "LEar": 18,
    "LBigToe": 19,
    "LSmallToe": 20,
    "LHeel": 21,
    "RBigToe": 22,
    "RSmallToe": 23,
    "RHeel": 24,
    "Background": 25
}

def arm_angle(keypoints):
    ''' 
    output: [left arm angle, right arm angle], horizontally given assuming performer is facing the front
    '''
    lwrist = np.array([keypoints[BODY_25["LWrist"]*3], keypoints[BODY_25["LWrist"]*3+1]])
    lshoulder = np.array([keypoints[BODY_25["LShoulder"]*3], keypoints[BODY_25["LShoulder"]*3+1]])
    lhip = np.array([keypoints[BODY_25["LHip"]*3], keypoints[BODY_25["LHip"]*3+1]])
    larm = lwrist-lshouder
    lbody = lhip-lshoulder
    left_arm_angle = np.arccos(np.clip(np.dot(larm/np.linalg.norm(larm),lbody/np.linalg.norm(lbody)),-1.0,1.0))

    rwrist = np.array([keypoints[BODY_25["RWrist"]*3], keypoints[BODY_25["RWrist"]*3+1]])
    rshoulder = np.array([keypoints[BODY_25["RShoulder"]*3], keypoints[BODY_25["RShoulder"]*3+1]])
    rhip = np.array([keypoints[BODY_25["RHip"]*3], keypoints[BODY_25["RHip"]*3+1]])
    rarm = rwrist-rshouder
    rbody = rhip-rshoulder
    right_arm_angle = np.arccos(np.clip(np.dot(rarm/np.linalg.norm(rarm),rbody/np.linalg.norm(rbody)),-1.0,1.0))

    return [left_arm_angle,right_arm_angle]

def leg_angle(keypoints):
    ''' 
    output: [left leg angle, right leg angle], horizontally given assuming performer is facing the front
    '''
    lankle = np.array([keypoints[BODY_25["LAnkle"]*3], keypoints[BODY_25["LAnkle"]*3+1]])
    lshoulder = np.array([keypoints[BODY_25["LShoulder"]*3], keypoints[BODY_25["LShoulder"]*3+1]])
    lhip = np.array([keypoints[BODY_25["LHip"]*3], keypoints[BODY_25["LHip"]*3+1]])
    lleg = lankle-lhip
    lbody = lshoulder-lhip
    left_left_angle = np.arccos(np.clip(np.dot(lleg/np.linalg.norm(lleg),lbody/np.linalg.norm(lbody)),-1.0,1.0))

    rwrist = np.array([keypoints[BODY_25["RWrist"]*3], keypoints[BODY_25["RWrist"]*3+1]])
    rshoulder = np.array([keypoints[BODY_25["RShoulder"]*3], keypoints[BODY_25["RShoulder"]*3+1]])
    rhip = np.array([keypoints[BODY_25["RHip"]*3], keypoints[BODY_25["RHip"]*3+1]])
    rleg = rankle-rhip
    rbody = rshoulder-rhip
    right_leg_angle = np.arccos(np.clip(np.dot(rleg/np.linalg.norm(rleg),rbody/np.linalg.norm(rbody)),-1.0,1.0))

    return [left_leg_angle,right_leg_angle]

# STRIKES
def is_valid_middlePunch(p, dir=None):
    """
    :param p: current position of body (dic)
    :param dir: direction of middle punch (str)
    :return: whether middle punch is good (bool)
    """
    #criterion 1: straight arms


# BLOCKS
def is_valid_lowBlock(p, dir=None):
    """
    :param p: current position of body (dic)
    :param dir: direction of low block (str)
    :return: whether low block is good (bool)
    """


def is_valid_insideBlock(p, dir=None):
    """
    :param p: current position of body (dic)
    :param dir: direction of inside block (str)
    :return: whether inside block is good (bool)
    """


def is_valid_highBlock(p, dir=None):
    """
    :param p: current position of body (dic)
    :param dir: direction of high block (str)
    :return: whether high block is good (bool)
    """
