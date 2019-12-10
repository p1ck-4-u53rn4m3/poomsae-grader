import json
import math

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


# STRIKES
def is_valid_frontKick(coords, foot=None):
    """
    :param coords: Dictionary of keypoint to coordinate (dic)
    :param foot: kicking foot of front kick (str)
    :return: whether front kick is good (bool)
    """
    if foot != 'left' and foot != 'right':
        raise SyntaxError

    if foot == 'left':
        kicking = 'L'
        support = 'R'
    else:
        kicking = 'R'
        support = 'L'

    # criterion 1: instep in line with leg
    ankle_toe = (coords['LBigToe'] - coords[kicking+'Ankle'])/np.linalg.norm(coords['LBigToe'] - coords[kicking+'Ankle'])
    ankle_knee = (coords['LKnee'] - coords[kicking+'Ankle'])/np.linalg.norm(coords['LKnee'] - coords[kicking+'Ankle'])
    instep_angle = np.arccos(np.clip(np.dot(ankle_toe, ankle_knee))) * 180/(2*math.pi)
    if instep_angle > 30:
        return False

    # criterion 2: head high kick
    if coords[kicking + 'BigToe'][1] < coords["Neck"][1]:
        return False

    # criterion 3: support heel flat on the floor
    if coords[support + 'Heel'][1] > coords[support + 'BigToe']:
        return False

    # criterion 4: support foot pivot up to 30 deg
    x = np.array([1, 0])
    toe = coords[support + 'BigToe']
    heel = coords[support + 'Heel']
    support_vec = (toe - heel) / np.linalg.norm(toe - heel)
    angle = np.arccos(np.clip(np.dot(support_vec, x))) * 180 / (2 * math.pi)
    if angle > 30:
        return False

    return True
