# -*- coding: utf-8 -*-
# author:yangtao
# time: 2021/04/16


import os


HUMAN_IK_CODES = {
    "Reference": 0,
    "Hips": 1,
    "LeftUpLeg": 2,
    "LeftLeg": 3,
    "LeftFoot": 4,
    "RightUpLeg": 5,
    "RightLeg": 6,
    "RightFoot": 7,
    "Spine": 8,
    "LeftArm": 9,
    "LeftForeArm": 10,
    "LeftHand": 11,
    "RightArm": 12,
    "RightForeArm": 13,
    "RightHand": 14,
    "Head": 15,
    "LeftToeBase": 16,
    "RightToeBase": 17,
    "LeftShoulder": 18,
    "RightShoulder": 19,
    "Neck": 20,
    "Spine1": 23,
    "Spine2": 24,
    "LeftUpLegRoll": 41,
    "LeftLegRoll": 42,
    "RightUpLegRoll": 43,
    "RightLegRoll": 44,
    "LeftArmRoll": 45,
    "LeftForeArmRoll": 46,
    "RightArmRoll": 47,
    "RightForeArmRoll": 48,
    "LeftHandThumb1": 50,
    "LeftHandThumb2": 51,
    "LeftHandThumb3": 52,
    "LeftHandIndex1": 54,
    "LeftHandIndex2": 55,
    "LeftHandIndex3": 56,
    "LeftHandMiddle1": 58,
    "LeftHandMiddle2": 59,
    "LeftHandMiddle3": 60,
    "LeftHandRing1": 62,
    "LeftHandRing2": 63,
    "LeftHandRing3": 64,
    "LeftHandPinky1": 66,
    "LeftHandPinky2": 67,
    "LeftHandPinky3": 68,
    "RightHandThumb1": 74,
    "RightHandThumb2": 75,
    "RightHandThumb3": 76,
    "RightHandIndex1": 78,
    "RightHandIndex2": 79,
    "RightHandIndex3": 80,
    "RightHandMiddle1": 82,
    "RightHandMiddle2": 83,
    "RightHandMiddle3": 84,
    "RightHandRing1": 86,
    "RightHandRing2": 87,
    "RightHandRing3": 88,
    "RightHandPinky1": 90,
    "RightHandPinky2": 91,
    "RightHandPinky3": 92,
    "LeftInHandIndex": 147,
    "LeftInHandMiddle": 148,
    "LeftInHandRing": 149,
    "LeftInHandPinky": 150,
    "RightInHandIndex": 153,
    "RightInHandMiddle": 154,
    "RightInHandRing": 155,
    "RightInHandPinky": 156,
}

HIK_CODES_SORT = {
    "Body": [
        ["RightShoulder", "RightArm", "RightForeArm", "RightHand", "RightUpLeg", "RightLeg", "RightFoot"],
        ["Head", "Neck", "Spine", "Spine1", "Hips"],
        ["LeftShoulder", "LeftArm", "LeftForeArm", "LeftHand", "LeftUpLeg", "LeftLeg", "LeftFoot"]
    ],
    "Foot": [
        ["RightToeBase"],
        ["LeftToeBase"],
    ]
}

FILE_EXT = ".HIKM"
INSTRUCTION_FILE = os.path.join(os.path.dirname(__file__), "../doc/instruction.html")
