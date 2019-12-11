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

focal_parts = {"RElbow","RWrist","LElbow","LWrist","RKnee","RAnkle","LKnee","LAnkle","LHeel","RHeel"}

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
    output: total score
    '''
    keypoints = read_file(f)


def stop_points(file_list):
    stops = []
    current_frame = read_file(file_list[0])
    velocity = {}
    for i in range(1,len(file_list)):
        prev_frame = current_frame
        current_frame = read_file(file_list[i])
        diff=0
        for n in range(24):# Simple Velocity Drop
            diff += abs(prev_frame[3*n] - current_frame[3*n])
            diff += abs(prev_frame[3*n+1] - current_frame[3*n+1])
        if diff < 50:
            stops.append(i)
        for part in focal_parts:
            n = BODY_25[part]
            velo = np.array([prev_frame[3*n] - current_frame[3*n],prev_frame[3*n+1] - current_frame[3*n+1]])
            if i > 1:
                acc = velo - velocity[part]
                if np.linalg.norm(acc) > 15 and diff < 90:
                    print("hi", np.linalg.norm(acc),i,part)
            velocity[part] = velo
    ret = [stops[0]]
    for i in range(len(stops)-1):
        if stops[i+1]-stops[i] > 3:
            ret.append(stops[i])
            ret.append(stops[i+1])
    return ret

f_list = []
for i in range(796):
    name = 'good_kevin_'+('00000000000'+str(i))[-12:]+'_keypoints.json'
    f_list.append(name)
print(stop_points(f_list))
"""
<<<<<<< HEAD
    lwrist = (keypoints[], keypoints[])
=======
<<<<<<< HEAD
    lwrist = (keypoints[], keypoints[])
=======



>>>>>>> b94a4f2543cfd2a6cb3a08dc4a7dbdcf3d81830c
>>>>>>> 884c8fad1dffd3d2a989a7a3adca10ae7f3740dc
"""
