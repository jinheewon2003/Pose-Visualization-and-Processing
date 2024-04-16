import json
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# Define joint connections
JOINT_CONNECTIONS = [
    ("Neck", "ClavicleLeft"),
    ("Neck", "ClavicleRight"),
    ("ClavicleLeft", "ShoulderLeft"),
    ("ClavicleRight", "ShoulderRight"),
    ("ShoulderLeft", "ElbowLeft"),
    ("ShoulderRight", "ElbowRight"),
    ("ElbowLeft", "WristLeft"),
    ("ElbowRight", "WristRight"),
    ("Neck", "Waist"),
]

# Load compiled data from file
with open("compiled_data.json", "r") as file:
    compiled_data = json.load(file)

timestamps = sorted(compiled_data.keys())
num_frames = len(timestamps)

# Initialize the figure
fig = plt.figure(figsize=(18, 10))
ax1 = fig.add_subplot(2, 2, 1, projection='3d')
ax2 = fig.add_subplot(2, 2, 2)
ax3 = fig.add_subplot(2, 1, 2)

# Function to update the plot for each frame
def update(frame):
    ax1.clear()  # Clear the current 3D plot
    ax2.clear()  # Clear the current line plot
    ax3.clear()  # Clear the current word plot
    
    ax1.set_xlim3d(-0.5, 0.75) 
    ax1.set_ylim3d(-0.5, 0.5)
    ax1.set_zlim3d(-1, 1)
    ax1.view_init(elev=-90, azim=-90)
    
    timestamp = timestamps[frame]
    data = compiled_data[timestamp]

    # Plot joint positions for person 1
    for joint, pos in data['person_1'].items():
        x, y, z = pos
        ax1.scatter(x, y, z, color='red')

    # Plot joint positions for person 2
    for joint, pos in data['person_2'].items():
        x, y, z = pos
        ax1.scatter(x, y, z, color='blue')

    # Plot connection lines
    for joint1, joint2 in JOINT_CONNECTIONS:
        x1, y1, z1 = data['person_1'][joint1]
        x2, y2, z2 = data['person_1'][joint2]
        ax1.plot([x1, x2], [y1, y2], [z1, z2], color='red')

        x1, y1, z1 = data['person_2'][joint1]
        x2, y2, z2 = data['person_2'][joint2]
        ax1.plot([x1, x2], [y1, y2], [z1, z2], color='blue')

    # Plot force over time
    ax2.plot(timestamps[:frame+1], [compiled_data[ts]['force'] for ts in timestamps[:frame+1]], color='green')

    # Display words
    for word in compiled_data[str(timestamps[frame])]["words"]:
        ax3.text(0.5, 0.5, word, ha='center', va='center', fontsize=16)

# Create the animation
animation = FuncAnimation(fig, update, frames=num_frames, interval=0.5)
plt.show()
