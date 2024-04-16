import json

# Define joint names and connections
JOINT_NAMES = [
    "Neck", "ShoulderRight", "ElbowRight", "WristRight", 
    "ShoulderLeft", "ElbowLeft", "WristLeft", "ClavicleLeft", 
    "ClavicleRight", "Waist"
]

def process_segment(segment, compiled_data):
    start = segment["start"]
    end = segment["end"]
    words = segment["output"]
    positions = segment["positions"]
    forces = segment["force"]
    
    for timestamp in range(int(float(start) * 10), int(float(end) * 10) + 1):
        timestamp /= 10
        compiled_data[timestamp] = {}
        working_with = compiled_data[timestamp]
        working_with["words"] = []
        working_with["force"] = 0
        working_with["person_1"] = {}
        working_with["person_2"] = {}
        
        # Process words
        for word in words:
            if timestamp <= word["timestamp"] < timestamp + 0.1:
                working_with["words"].append(word["word"])
            elif (timestamp + 0.1) < word["timestamp"]:
                break
        
        # Process forces
        working_force = 0
        force_count = 0
        for force_timestamp, force_value in forces.items():
            if timestamp <= float(force_timestamp) < timestamp + 0.1:
                working_force += force_value
                force_count += 1
        if force_count != 0:
            working_with["force"] = working_force / force_count
                
        # Process positions
        position_count = 0
        for position_timestamp, position_data in positions.items():
            if timestamp <= float(position_timestamp) < timestamp + 0.1:
                for joint in JOINT_NAMES:
                    for i in range(3):
                        working_with["person_1"].setdefault(joint, [0, 0, 0])[i] += position_data[0][joint][i]
                        working_with["person_2"].setdefault(joint, [0, 0, 0])[i] += position_data[1][joint][i]
                position_count += 1
        
        # Calculate averages
        if position_count != 0:
            for person_data in (working_with["person_1"], working_with["person_2"]):
                for joint in JOINT_NAMES:
                    for i in range(3):
                        person_data[joint][i] /= position_count

def main():
    # Load organized data from file
    with open("organized_data.json", "r") as file:
        organized_data = json.load(file)

    # Create compiled data dictionary
    compiled_data = {}

    # Process organized data
    for segment in organized_data:
        process_segment(segment, compiled_data)

    # Write the updated data to a file
    with open("compiled_data.json", "w") as outfile:
        json.dump(compiled_data, outfile, indent=4)

main()
