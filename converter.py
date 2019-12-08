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

def read_file(f):
    ''' reads the json file of people arrays produced by OpenPose
    input: name of json file
    output: array of keypoints
    '''
    with open(f,'r') as file:
        data = file.read()
    obj = json.loads(data)
    return obj["people"][0]["pose_keypoints_2d"]


def analyze(f, optimal):
    ''' reads the json file of people arrays produced by OpenPose
    input: name of json file
    output: [arm angle, leg angle]
    '''
    keypoints = read_file(f)



