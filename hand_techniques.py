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


# Might belong to a broader scope
def get_BODY_coords(BODY_25, keypoints):
    """
    :param BODY_25: Definition of each keypoint (dic)
    :param keypoints: Current position of body (dic)
    :return: Dictionary of keypoint to coordinate (dic)
    """
    return {kp: np.array([keypoints[BODY_25[kp] * 3], keypoints[BODY_25[kp] * 3 + 1]]) for kp in BODY_25}


# STRIKES
def is_valid_middlePunch(coords, hand=None):
    """
    :param coords: Dictionary of keypoint to coordinate (dic)
    :param hand: hand of middle punch (str)
    :return: whether middle punch is good (bool)
    """
    if hand != 'left' and hand != 'right':
        raise SyntaxError

    # criterion 1: straight arm
    if hand == 'left' and not arm_angle(coords)[0] <= 175:
        return False
    elif hand == 'right' and not arm_angle(coords)[1] <= 175:
        return False

    # criterion 2: solar plexus height
    if coords['REar'] != np.array([0, 0]) and coords['LEar'] != np.array([0, 0]):
        print("front and back will be dealt with soon!")
    else:
        if hand == 'left' and not (75 < arm_to_body_angle(coords)[0] < 85):  # adjust values
            return False
        elif hand == 'right' and not (75 < arm_to_body_angle(coords)[1] < 85):  # adjust values
            return False

    # criterion 3: opposite hand placed correctly
    if coords['REar'] != np.array([0, 0]) and coords['LEar'] != np.array([0, 0]):
        print("front and back will be dealt with soon!")
    else:
        if not opposite_hand_placement(coords, hand):
            return False

    return True


# BLOCKS
def is_valid_lowBlock(coords, hand=None):
    """
    :param coords: Dictionary of keypoint to coordinate (dic)
    :param hand: hand of low block (str)
    :return: whether low block is good (bool)
    """
    if hand != 'left' and hand != 'right':
        raise SyntaxError

    # criterion 1: straight arm
    if hand == 'left' and not arm_angle(coords)[0] <= 175:
        return False
    elif hand == 'right' and not arm_angle(coords)[1] <= 175:
        return False

    # criterion 2: block at proper angle
    # facing front or back
    if coords['REar'] != np.array([0, 0]) and coords['LEar'] != np.array([0, 0]):
        print("will be dealt with soon!")
    else:
        if hand == 'left' and not (30 < arm_to_body_angle(coords)[0] < 45):  # adjust values
            return False
        elif hand == 'right' and not (30 < arm_to_body_angle(coords)[1] < 45):  # adjust values
            return False

    # criterion 3: opposite hand placed correctly
    if coords['REar'] != np.array([0, 0]) and coords['LEar'] != np.array([0, 0]):
        print("front and back will be dealt with soon!")
    else:
        if not opposite_hand_placement(coords, hand):
            return False

    return True


def is_valid_insideBlock(coords, hand=None):
    """
    :param coords: Dictionary of keypoint to coordinate (dic)
    :param hand: hand of inside block (str)
    :return: whether inside block is good (bool)
    """
    if hand != 'left' and hand != 'right':
        raise SyntaxError

    # criterion 1: blocking arm bent 90 to 120 degrees
    if coords['REar'] != np.array([0, 0]) and coords['LEar'] != np.array([0, 0]):
        print("will be dealt with soon!")
    else:
        if hand == 'left' and not 90 <= arm_angle(coords)[0] <= 120:
            return False
        elif hand == 'right' and not 90 <= arm_angle(coords)[1] <= 120:
            return False

    # criterion 2: blocking arm wrist between center and shoulder level
    if hand == "left":
        height = coords['RWrist'][1]
    elif hand == "right":
        height = coords['LWrist'][1]

    if height > coords['LShoulder'] or height < (coords['Neck'] + coords['MidHip']) / 2:
        return False

    # criterion 3: opposite hand placed correctly
    if coords['REar'] != np.array([0, 0]) and coords['LEar'] != np.array([0, 0]):
        print("front and back will be dealt with soon!")
    else:
        if not opposite_hand_placement(coords, hand):
            return False

    return True

def is_valid_highBlock(coords, hand=None):
    """
    :param coords: Dictionary of keypoint to coordinate (dic)
    :param hand: hand of high block (str)
    :return: whether high block is good (bool)
    """
    if hand != 'left' and hand != 'right':
        raise SyntaxError

    # criterion 1: blocking arm wrist 1 fist width from forehead
    if coords['REar'] != np.array([0, 0]) and coords['LEar'] != np.array([0, 0]):
        print("front and back will be dealt with soon!")
    elif coords["REar"] != np.array([0, 0]):
        length = np.linalg.norm(coords["REye"] - coords["REar"])
        if hand == 'left':
            wrist_to_eye = coords["LWrist"] - coords["REye"]
        elif hand == 'right':
            wrist_to_eye = coords["RWrist"] - coords["REye"]
    elif coords["LEar"] != np.array([0, 0]):
        length = np.linalg.norm(coords["LEye"] - coords["LEar"])
        if hand == 'left':
            wrist_to_eye = coords["LWrist"] - coords["LEye"]
        elif hand == 'right':
            wrist_to_eye = coords["RWrist"] - coords["LEye"]
    else:
        raise SyntaxError

    dist = np.linalg.norm(wrist_to_eye)
    if dist < length or dis > 1.5 * length: # change in future
        return False

    # criterion 2: blocking arm wrist at 45 degree angle from forehead
    angle = np.arccos(wrist_to_eye) * 180/(2 * math.pi)
    if angle < 30 or angle > 60:
        return False

    # criterion 3: blocking arm wrist at centerline of face

    # criterion 4: opposite hand placed correctly
    if coords['REar'] != np.array([0, 0]) and coords['LEar'] != np.array([0, 0]):
        print("front and back will be dealt with soon!")
    else:
        if not opposite_hand_placement(coords, hand):
            return False

    return True


# HELPER FUNCTIONS
def arm_to_body_angle(coords):
    """
    :param coords: Dictionary of keypoint to coordinate (dic)
    :return: [left arm to body angle, right arm to body angle], horizontally given assuming performer is facing the front (array)
    """
    larm = coords['LWrist'] - coords['LShoulder']
    lbody = coords['LHip'] - coords['LShoulder']
    left_arm_angle = np.arccos(np.clip(np.dot(larm / np.linalg.norm(larm), lbody / np.linalg.norm(lbody)), -1.0, 1.0))

    rarm = coords['RWrist'] - coords['RShoulder']
    rbody = coords['RHip'] - coords['RShoulder']
    right_arm_angle = np.arccos(np.clip(np.dot(rarm / np.linalg.norm(rarm), rbody / np.linalg.norm(rbody)), -1.0, 1.0))

    return [left_arm_angle * 180/(2 * math.pi), right_arm_angle * 180/(2 * math.pi)]


def leg_to_body_angle(coords):
    """
    :param coords: Dictionary of keypoint to coordinate (dic)
    :return: [left leg angle, right leg angle], horizontally given assuming performer is facing the front (array)
    """
    lleg = coords['LAnkle'] - coords['LHip']
    lbody = coords['LShoulder'] - coords['LHip']
    left_leg_angle = np.arccos(np.clip(np.dot(lleg / np.linalg.norm(lleg), lbody / np.linalg.norm(lbody)), -1.0, 1.0))

    rleg = coords['RAnkle'] - coords['RHip']
    rbody = coords['RShoulder'] - coords['RHip']
    right_leg_angle = np.arccos(np.clip(np.dot(rleg / np.linalg.norm(rleg), rbody / np.linalg.norm(rbody)), -1.0, 1.0))

    return [left_leg_angle * 180/(2 * math.pi), right_leg_angle * 180/(2 * math.pi)]


def arm_angle(coords):
    """
    :param coords: Dictionary of keypoint to coordinate (dic)
    :return: [left arm angle, right arm angle], horizontally given assuming performer is facing the front (array)
    """
    lforearm = coords['LWrist'] - coords['LElbow']
    lupperarm = coords['LShoulder'] - coords['LElbow']
    left_arm_angle = np.arccos(np.clip(np.dot(lforearm / np.linalg.norm(lforearm), lupperarm / np.linalg.norm(lupperarm)), -1.0, 1.0))

    rforearm = coords['RWrist'] - coords['RElbow']
    rupperarm = coords['RShoulder'] - coords['RElbow']
    right_arm_angle = np.arccos(np.clip(np.dot(rforearm / np.linalg.norm(rforearm), rupperarm / np.linalg.norm(rupperarm)), -1.0, 1.0))

    return [left_arm_angle * 180/(2 * math.pi), right_arm_angle * 180/(2 * math.pi)]


def opposite_hand_placement(coords, hand=None):
    """
    :param coords: Dictionary of keypoint to coordinate (dic)
    :param hand: hand to perform a move (str)
    :return: Whether the opposite hand has been placed correctly (bool)
    """
    if hand == "left":
        hip = coords['RHip'] - coords['MidHip']
        wrist_to_hip = coords['RWrist'] - coords['MidHip']

        height = coords['RWrist'][1]
    elif hand == "right":
        hip = coords['LHip'] - coords['MidHip']
        wrist_to_hip = coords['LWrist'] - coords['MidHip']

        height = coords['LWrist'][1]

    # wrist->midhip and midhip->l/rhip angle should be acute
    hip_vec = hip / np.linalg.norm(hip)
    wrist_to_hip_vec = wrist_to_hip / np.linalg.norm(wrist_to_hip)
    placement = np.arccos(np.clip(np.dot(hip_vec, wrist_to_hip_vec), -1.0, 1.0))
    if placement > 90 or placement < 45:
        return False

    # wrist hieght between chest and hip
    if height < coords['MidHip'] or height > (coords['Neck'] + coords['MidHip'])/2:
        return False

    return True
