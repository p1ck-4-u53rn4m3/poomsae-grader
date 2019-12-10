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


def is_valid_walkingStance(coords, dir=None):
    """
    :param coords: Dictionary of keypoint to coordinate (dic)
    :param dir: direction of walking stance - which foot is in front (str)
    :return: whether walking stance is good (bool)
    """
    if hand != 'left' and hand != 'right':
        raise SyntaxError

    # criterion 1: legs are straight
    lknee_to_lhip = (coords['LHip'] - coords['LKnee'])/np.linalg.norm(coords['LHip'] - coords['LKnee'])
    lknee_to_lankle = (coords['LAnkle'] - coords['LKnee'])/np.linalg.norm(coords['LAnkle'] - coords['LKnee'])
    left_leg = np.arccos(np.clip(np.dot(lknee_to_lhip, lknee_to_lankle))) * 180/(2*math.pi)

    rknee_to_rhip = (coords['RHip'] - coords['RKnee'])/np.linalg.norm(coords['RHip'] - coords['RKnee'])
    rknee_to_rankle = (coords['RAnkle'] - coords['RKnee'])/np.linalg.norm(coords['RAnkle'] - coords['RKnee'])
    right_leg = np.arccos(np.clip(np.dot(rknee_to_rhip, rknee_to_rankle))) * 180/(2*math.pi)

    if left_leg < 170 or right_leg < 170:
        return False

    # criterion 2: weight is centered - left/right hip are between ankles
    if coords['REar'] != np.array([0, 0]) and coords['LEar'] != np.array([0, 0]):
        print("front and back will be dealt with soon!")
    else:
        if (coords['LHip']-coords['RAnkle']) * (coords['LHip']-coords['LAnkle']) > 0:
            if (coords['RHip']-coords['RAnkle']) * (coords['RHip']-coords['RAnkle']) > 0:
                return False

    # criterion 3: one foot length between feet
    foot_length = max(np.linalg.norm(coords['LHeel']-coords['LBigToe']), np.linalg.norm(coords['RHeel']-coords['RBigToe']))
    if coords['REar'] != np.array([0, 0]) and coords['LEar'] != np.array([0, 0]):
        print("front and back will be dealt with soon!")
    else:
        dist = min(np.linalg.norm(coords['LHeel']-coords['RBigToe']), np.linalg.norm(coords['RHeel']-coords['LBigToe']))
        if abs(dist - foot_length) > foot_length/3:
            return False

    # criterion 4: front foot is straight & back foot is at 30 degrees
    if coords['REar'] != np.array([0, 0]) and coords['LEar'] != np.array([0, 0]):
        print("front and back will be dealt with soon!")
    else:
        x = np.array([1, 0])
        left_foot = (coords['LBigToe'] - coords['LHeel'])/np.linalg.norm(coords['LBigToe'] - coords['LHeel'])
        right_foot = (coords['RBigToe'] - coords['RHeel'])/np.linalg.norm(coords['RBigToe'] - coords['RHeel'])
        if dir == 'left':
            fangle = np.arccos(np.clip(np.dot(left_foot, x))) * 180/(2*math.pi)
            bangle = np.arccos(np.clip(np.dot(right_foot, x))) * 180/(2*math.pi)
        elif dir == 'right':
            fangle = np.arccos(np.clip(np.dot(right_foot, x))) * 180/(2*math.pi)
            bangle = np.arccos(np.clip(np.dot(left_foot, x))) * 180/(2*math.pi)

        if fangle > 10 or bangle > 35:
            return False

    return True


def is_valid_frontStance(p, dir=None):
    """
    :param p: current position of body (dic)
    :param dir: direction of front stance (str)
    :return: whether front stance is good (bool)
    """
    # criterion 1: 2.5 feet length between feet

    # criterion 2: back leg is straight

    # criterion 3: front leg is bent

    # criterion 4: front foot is straight & back foot is at 30 degrees

    # criterion 5: ~2/3 weight on front foot

    # criterion 6: 1 fist width

    return True
