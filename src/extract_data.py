from ast import Tuple
import json
from pathlib import Path
import re
import pandas as pd
from typing import TypedDict, List, Dict, Union
import time
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

# Define joint names and connections
JOINT_NAMES = [
    "Neck", "ShoulderRight", "ElbowRight", "WristRight", 
    "ShoulderLeft", "ElbowLeft", "WristLeft", "ClavicleLeft", 
    "ClavicleRight", "Waist"
]

# Define data structures for poses
class Joint(TypedDict):
    confidence: float
    projection: List[float]
    pos3D: List[float]
    orientation: List[List[float]]

Skeleton = Dict[str, Union[Joint, int]]

class Poses(TypedDict):
    timestamp: float
    skeletons: List[Skeleton]

def main():
    # Create compiled data json
    data = []
    root_folder = Path(__file__).parents[1]
    input_file_path = root_folder / ("data/audio_segmentation.json")
    with open(input_file_path, "r") as file:
        for line in file:
            segment = json.loads(line)
            data.append({"start": segment["start"], "end": segment["end"], "output": segment["words"], "positions": {}, "force": {}})
    print(f"Loaded {len(data)} audio segments")
        
    # Load force data from CSV file
    force_data_path = root_folder / ("data/force_data.csv")
    force_data = pd.read_csv(force_data_path)
    print(f"Loaded {len(force_data)} entries from force data CSV")
    
    # Load poses from file
    poses: List[Poses] = []
    poses_path = root_folder / ("data/cut_poses.jsonl")
    with open(poses_path, "r") as file:
        for line in file:
            poses.append(Poses(json.loads(line)))
    print(f"Loaded {len(poses)} poses")

    # Extract keypoints from poses and associate them with the correct time intervals
    keypoints_by_interval: Dict[Tuple[float, float], List[List[np.ndarray]]] = {}
    
    # Extract keypoints from poses
    all_keypoints: List[List[np.ndarray]] = []
    timestamps: List[float] = []
        
    for pose in poses:
        if len(pose["skeletons"]) == 0:
            continue
        pose_keypoints: List[np.ndarray] = []
        adding_keypoints = []
        for skel in pose["skeletons"]:
            current_keypoints: List[List[float]] = []
            adding_keypoint = {}
            for joint_name in JOINT_NAMES:
                if joint_name not in skel:
                    continue
                joint: Joint = skel[joint_name]
                # if joint["confidence"] < 0.7:
                #     continue
                joint["pos3D"][2] *= 1.5
                adding_keypoint[joint_name] = joint["pos3D"]
                current_keypoints.append(joint["pos3D"])
            if len(current_keypoints) > 0:
                pose_keypoints.append(np.array(current_keypoints))
                adding_keypoints.append(adding_keypoint)
        if pose_keypoints:
            timestamps.append(pose["timestamp"])
            all_keypoints.append(pose_keypoints)
            
            # Add poses to data file
            timestamp = pose["timestamp"]
            # Find the corresponding time interval for this timestamp
            interval = None
            for seg in data:
                if seg["start"] <= timestamp <= seg["end"]:
                    interval = (seg["start"], seg["end"])
                    break
            if interval is not None:
                if interval not in keypoints_by_interval:
                    keypoints_by_interval[interval] = []
                keypoints_by_interval[interval].append(adding_keypoints)
                # Add pose_keypoints to the 'positions' field of the corresponding entry in data
                seg["positions"][str(timestamp)] = adding_keypoints
            
    # Now, let's add force data to the correct time intervals in the 'positions' field of data
    for index, row in force_data.iterrows():
        timestamp = row["timestamp"]
        force_unparsed = row["reading"]
        force = float_value = float(re.search(r'\d+\.\d+', force_unparsed).group())
        
        for seg in data:
            print(seg["start"])
            if seg["start"] <= timestamp <= seg["end"]:
                seg["force"][str(timestamp)] = force
                break


    # Write the updated data to a file
    
    organized_path = root_folder / ("data/organized_data.json")
    with open(organized_path, "w") as outfile:
        json.dump(data, outfile, indent=4)
        
main()