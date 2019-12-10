import json
import math
import numpy as np
import importlib
import stances, kicks

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

    if hand == 'left':
        punch_arm = coords["LWrist"]
        off_arm = coords["RWrist"]
    else:
        punch_arm = coords["RWrist"]
        off_arm = coords["LWrist"]

    # criterion 1: straight arm
    if (coords['REar'][0] != 0 and coords['REar'][1] != 0) and (coords['LEar'][0] != 0 and coords['LEar'][1] != 0):
        print("front and back will be dealt with soon!")
    else:
        if hand == 'left' and arm_angle(coords)[0] <= 165:
            print("arm angle is: " + str(arm_angle(coords)[0]) + " arm not straight")
            return False
        elif hand == 'right' and arm_angle(coords)[1] <= 165:
            print("arm angle is: " + str(arm_angle(coords)[1]) + " arm not straight")
            return False

    # criterion 2: solar plexus height
    if (coords['REar'][0] != 0 and coords['REar'][1] != 0) and (coords['LEar'][0] != 0 and coords['LEar'][1] != 0):
        print("front and back will be dealt with soon!")
    else:
        middle_torso = (coords["MidHip"][1] + coords["Neck"][1]) / 2
        y1 = min(middle_torso, coords["Neck"][1])
        y2 = max(middle_torso, coords["Neck"][1])
        if not (y1 < punch_arm[1] < y2):  # adjust values
            print("not solar plexus height: " + str(punch_arm[1]) + " not between " + str((y1, y2)))
            return False

    # criterion 3: opposite hand placed correctly
    if (coords['REar'][0] != 0 and coords['REar'][1] != 0) and (coords['LEar'][0] != 0 and coords['LEar'][1] != 0):
        print("front and back will be dealt with soon!")
    else:
        if not opposite_hand_placement(coords, hand):
            print("opposite hand not placed correctly")
            return False

    # criterion 4: punch is to the centerline of body
    if (coords['REar'][0] != 0 and coords['REar'][1] != 0) and (coords['LEar'][0] != 0 and coords['LEar'][1] != 0):
        if (coords['REye'][0] != 0 and coords['REye'][1] != 0) and (coords['LEye'][0] != 0 and coords['LEye'][1] != 0):
            x1 = coords['LEar'][0]
            x2 = coords['REar'][0]
            if (punch_arm[0] - x1) * (punch_arm[0] - x2) > 0:
                print("punch not at centerline", punch_arm[0], x1, x2)
                return False
    else:
        print("sides will be dealt with soon!")

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

    if hand == 'left':
        block_arm = coords["LWrist"]
        off_arm = coords["RWrist"]
    else:
        block_arm = coords["RWrist"]
        off_arm = coords["LWrist"]

    # criterion 1: straight arm
    if (coords['REar'][0] != 0 and coords['REar'][1] != 0) and (coords['LEar'][0] != 0 and coords['LEar'][1] != 0):
        print("will be dealt with soon!")
    else:
        if hand == 'left' and arm_angle(coords)[0] <= 165:
            print("arm angle is: " + str(arm_angle(coords)[0]) + " arm not straight")
            return False
        elif hand == 'right' and arm_angle(coords)[1] <= 165:
            print("arm angle is: " + str(arm_angle(coords)[1]) + " arm not straight")
            return False

    # criterion 2: block two fist widths from quadricep
    # Fist length approximation
    fist = max(np.linalg.norm(coords['LEar'] - coords['LEye']), np.linalg.norm(coords['REar'] - coords['REye']))
    # facing front or back
    if (coords['REar'][0] != 0 and coords['REar'][1] != 0) and (coords['LEar'][0] != 0 and coords['LEar'][1] != 0):
        print("will be dealt with soon!")
    else:
        if hand == 'left':  # adjust values
            dist = np.linalg.norm(coords['LWrist'] - coords['LHip'])
        elif hand == 'right':
            dist = np.linalg.norm(coords['RWrist'] - coords['RHip'])

        if abs(dist - 2 * fist) > fist / 2:
            print("low block dist off: " + str(dist) + " instead of " + str(2 * fist))
            return False

    # criterion 3: opposite hand placed correctly
    if (coords['REar'][0] != 0 and coords['REar'][1] != 0) and (coords['LEar'][0] != 0 and coords['LEar'][1] != 0):
        print("front and back will be dealt with soon!")
    else:
        if not opposite_hand_placement(coords, hand):
            print("opposite hand not placed correctly")
            return False

    # criterion 4: low block above quadricep
    if (coords['REar'][0] != 0 and coords['REar'][1] != 0) and (coords['LEar'][0] != 0 and coords['LEar'][1] != 0):
        x1 = coords['MidHip'][0]
        x2 = (2 * coords['LHip'] - coords['MidHip'])[0]

        if (block_arm[0] - x1) * (block_arm[0] - x2) > 0:
            print("low block not above quadricep")
            return False
    else:
        print("sides will be dealt with soon!")

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
    if (coords['REar'][0] != 0 and coords['REar'][1] != 0) and (coords['LEar'][0] != 0 and coords['LEar'][1] != 0):
        print("will be dealt with soon!")
    else:
        if hand == 'left' and not 85 <= arm_angle(coords)[0] <= 125:
            print("arm angle is off: " + str(arm_angle(coords)[0]))
            return False
        elif hand == 'right' and not 90 <= arm_angle(coords)[1] <= 120:
            print("arm angle is off: " + str(arm_angle(coords)[1]))
            return False

    # criterion 2: blocking arm wrist between center and shoulder level
    if hand == "left":
        height = coords['LWrist'][1]
    elif hand == "right":
        height = coords['RWrist'][1]

    y1 = coords['LShoulder'][1]
    y2 = (coords['Neck'][1] + coords['MidHip'][1]) / 2
    if (height - y1) * (height - y2) > 0:
        print("wrist is not in right height: " + str(height) + " instead of: " + str((y1, y2)))
        return False

    # criterion 3: opposite hand placed correctly
    if (coords['REar'][0] != 0 and coords['REar'][1] != 0) and (coords['LEar'][0] != 0 and coords['LEar'][1] != 0):
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
    if (coords['REar'][0] != 0 and coords['REar'][1] != 0) and (coords['LEar'][0] != 0 and coords['LEar'][1] != 0):
        print("front and back will be dealt with soon!")
    elif coords['REar'][0] != 0 and coords['REar'][1] != 0:
        length = np.linalg.norm(coords["REye"] - coords["REar"])
        if hand == 'left':
            wrist_to_eye = coords["LWrist"] - coords["REye"]
        elif hand == 'right':
            wrist_to_eye = coords["RWrist"] - coords["REye"]
    elif coords['LEar'][0] != 0 and coords['LEar'][1] != 0:
        length = np.linalg.norm(coords["LEye"] - coords["LEar"])
        if hand == 'left':
            wrist_to_eye = coords["LWrist"] - coords["LEye"]
        elif hand == 'right':
            wrist_to_eye = coords["RWrist"] - coords["LEye"]
    else:
        raise SyntaxError

    dist = np.linalg.norm(wrist_to_eye)
    if dist < length or dist > 2 * length:  # change in future
        print('dist is off: ' + str(dist) + ', ' + str(length))
        return False

    # criterion 2: blocking arm wrist at 45 degree angle from forehead
    angle = np.arccos(np.clip(np.dot(wrist_to_eye / dist, np.array([1, 0])), -1.0, 1.0)) * 180 / math.pi
    if angle > 90:
        angle = 180 - angle
    if angle < 30 or angle > 60:
        print('angle is off: ' + str(angle))
        return False

    # criterion 3: blocking arm wrist at centerline of face

    # criterion 4: opposite hand placed correctly
    if (coords['REar'][0] != 0 and coords['REar'][1] != 0) and (coords['LEar'][0] != 0 and coords['LEar'][1] != 0):
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

    return [left_arm_angle * 180 / math.pi, right_arm_angle * 180 / math.pi]


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

    return [left_leg_angle * 180 / math.pi, right_leg_angle * 180 / math.pi]


def arm_angle(coords):
    """
    :param coords: Dictionary of keypoint to coordinate (dic)
    :return: [left arm angle, right arm angle], horizontally given assuming performer is facing the front (array)
    """
    lforearm = coords['LWrist'] - coords['LElbow']
    lupperarm = coords['LShoulder'] - coords['LElbow']
    left_arm_angle = np.arccos(
        np.clip(np.dot(lforearm / np.linalg.norm(lforearm), lupperarm / np.linalg.norm(lupperarm)), -1.0, 1.0))

    rforearm = coords['RWrist'] - coords['RElbow']
    rupperarm = coords['RShoulder'] - coords['RElbow']
    right_arm_angle = np.arccos(
        np.clip(np.dot(rforearm / np.linalg.norm(rforearm), rupperarm / np.linalg.norm(rupperarm)), -1.0, 1.0))

    return [left_arm_angle * 180 / math.pi, right_arm_angle * 180 / math.pi]


def opposite_hand_placement(coords, hand=None):
    """
    :param coords: Dictionary of keypoint to coordinate (dic)
    :param hand: hand of the technique, so we will work with the opposite hand (str)
    :return: Whether the opposite hand has been placed correctly (bool)
    """
    if hand == "left":
        wrist = coords['RHip']
        hip = coords['RHip'] - coords['MidHip']
        wrist_to_hip = coords['RWrist'] - coords['MidHip']

        height = coords['RWrist'][1]
    elif hand == "right":
        wrist = coords['LHip']
        hip = coords['LHip'] - coords['MidHip']
        wrist_to_hip = coords['LWrist'] - coords['MidHip']

        height = coords['LWrist'][1]

    # # midhip->wrist and midhip->l/rhip angle should be acute
    # hip_vec = hip / np.linalg.norm(hip)
    # wrist_to_hip_vec = wrist_to_hip / np.linalg.norm(wrist_to_hip)
    # print(hip_vec, wrist_to_hip_vec)
    # placement = np.arccos(np.clip(np.dot(hip_vec, wrist_to_hip_vec), -1.0, 1.0)) * 180/math.pi
    # if placement > 90 or placement < 40:
    #     print(str(placement) + ' angle')
    #     return False

    # wrist x-coord between back heel and center of body
    if coords['LEar'][0] != 0 and coords['LEar'][1] != 0:
        eye = coords['LEye'][0]
    else:
        eye = coords['REye'][0]

    if (coords['MidHip'][0] - eye) * (coords['MidHip'][0] - coords['LHeel'][0]) <= 0:
        back = coords['LHeel'][0]
    else:
        back = coords['RHeel'][0]

    if (wrist[0] - eye) * (wrist[0] - back) > 0:
        print(wrist[0], eye, back)
        print("ayy no")
        return False

    # wrist height between chest and hip
    y1 = coords['MidHip'][1]
    y2 = (coords['Neck'][1] + coords['MidHip'][1]) / 2
    if (height - y1) * (height - y2) > 0:
        print(str(height) + ' height')
        return False

    return True


if __name__ == "__main__":
    # # good andrew
    # path = '/Users/kj/Documents/GitHub/poomsae-grader/results/T1/good_andrew/2D_keypoints/'
    # name = 'andrew_good_'
    # stopping_frames = [72, 105, 141, 170, 204, 215, 252, 286, 324, 356, 390, 408, 438, 463, 498, 531, 555, 585, 622, 657]

    # mediocre andrew
    path = '/Users/kj/Documents/GitHub/poomsae-grader/results/T1/mediocre_andrew/2D_keypoints/'
    name = 'mediocre_andrew_'
    stopping_frames = [57, 91, 126, 158, 188, 201, 239, 275, 310, 345, 378, 389, 425, 452, 481, 520, 549, 578, 622, 658]

    def check(moves, stop_coords):
        def convert(tech, stance, coords):
            technique_dic = {
                "leftMiddlePunch": (is_valid_middlePunch, 'left'),
                "rightMiddlePunch": (is_valid_middlePunch, 'right'),

                "leftLowBlock": (is_valid_lowBlock, 'left'),
                "rightLowBlock": (is_valid_lowBlock, 'right'),
                "leftHighBlock": (is_valid_highBlock, 'left'),
                "rightHighBlock": (is_valid_highBlock, 'right'),
                "leftInsideBlock": (is_valid_insideBlock, 'left'),
                "rightInsideBlock": (is_valid_insideBlock, 'right'),

                "leftFrontKick": (kicks.is_valid_frontKick, 'left'),
                "rightFrontKick": (kicks.is_valid_frontKick, 'right'),
            }

            stance_dic = {
                "leftWalkingStance": (stances.is_valid_walkingStance, 'left'),
                "rightWalkingStance": (stances.is_valid_walkingStance, 'right'),

                "leftFrontStance": (stances.is_valid_frontStance, 'left'),
                "rightFrontStance": (stances.is_valid_frontStance, 'right')
            }

            t = technique_dic.get(tech, None)
            s = stance_dic.get(stance, None)

            return t[0](coords, t[1]) if t else True, s[0](coords, s[1]) if s else True

        deduction = 0
        bad_moves = []
        for i in range(len(moves)):
            print("MOVE NUMBER " + str(i))
            a, b = convert(moves[i][0], moves[i][1], stop_coords[i])
            print("Hand Tech: " + str(a))
            print("Stance Tech: " + str(b))

            deduction += 0.1 if not a else 0
            deduction += 0.1 if not b else 0
            if not a or not b:
                bad_moves.append(i)

        return deduction, bad_moves

    with open('/Users/kj/Documents/GitHub/poomsae-grader/Taegeuk1.txt', 'r') as file:
        moves = eval(file.read())

    stop_coords = []
    for i in stopping_frames:
        n = len(str(i))
        k = ''.join(['0' for j in range(12 - n)])

        f = path + name + k + str(i) + '_keypoints.json'
        with open(f, 'r') as file:
            data = file.read()
        obj = json.loads(data)
        keypoints = obj["people"][0]["pose_keypoints_2d"]
        coords = get_BODY_coords(BODY_25, keypoints)
        stop_coords.append(coords)

    total, moves = check(moves, stop_coords)
    print("FINAL ACCURACY SCORE: " + str(4 - total))
    print("INCORRECT MOVE #'s: " + str(moves))


