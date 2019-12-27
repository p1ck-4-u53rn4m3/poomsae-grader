# poomsae-grader
PoomsAI: An Accuracy Auto-grader Using Bottom-up Human Pose Estimation

## Requirements
We used OpenPose (https://github.com/CMU-Perceptual-Computing-Lab/openpose) to generate human pose estimations from videos of athlete performances. You will need some kind of GPU if you wish to recreate the results from the data. In our case, we used AWS to run the networks provided by OpenPose. 

## Descriptions of Files

PoomsAI Paper.pdf - 6.819 project paper

converter.py - algorithm for stopping point detection

hand_techniques.py - grading algorithm for hands

kicks.py - grading algorithm for kicks

stances.py - grading algorithm for stances 

Taegeuk1.txt - Description for each stopping point

data - videos for modeling

results - processed videos
