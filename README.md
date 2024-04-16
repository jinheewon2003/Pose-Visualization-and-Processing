# Audio and Pose Data Processing Pipeline

This repository contains scripts for processing audio and pose data, extracting relevant information, and visualizing the data.

## Setup

To use the scripts in this repository, you need to have Python 3 installed on your system. You also need to install the required dependencies listed below.

## Usage

### 1. Transcribing Audio Segments

To transcribe audio segments and save the segmentation information in a JSON file, run the following script:

python audio_processing.py

This script transcribes the audio segments specified in the `cut_audio.wav` file and saves the segmentation information in the `audio_segmentation.json` file.

### 2. Processing Pose Data

To process pose data, extract keypoints, and associate them with the correct time intervals, run the following script:

python extract_data.py

This script reads pose data from the `cut_poses.jsonl` file, extracts keypoints, associates them with time intervals, and saves the processed data in the `organized_data.json` file.

### 3. Combining Audio and Pose Data

To combine audio and pose data, including force readings, and save the timestamped data in a JSON file, run the following script:

python combine_data.py

This script reads audio segmentation, pose, and force data, combines them, calculates averages, and saves the timestamped data in the `timestamped_data.json` file.

### 4. Visualizing Data

To visualize the processed data, including 3D joint positions, force over time, and displayed words, run the following script:

python visualize_data.py

This script creates an animation of 3D joint positions, plots force over time, and displays words associated with each timestamp. The animation is saved as `completed.mp4` in the `results` folder.

## Folder Structure

- `data`: Contains input and processed data files.
- `processed_data`: Contains output files generated during data processing.
- `results`: Contains the resulting visualizations and animations.

## Dependencies

- `whisper_timestamped`: A custom module for transcribing audio and loading models.
- `json`: For reading and writing JSON files.
- `pathlib`: For working with file paths.
- `pandas`: For data manipulation and analysis.
- `matplotlib`: For data visualization.
- `numpy`: For numerical computing.
- `mpl_toolkits.mplot3d`: For 3D plotting.
- `matplotlib.animation.FuncAnimation`: For creating animations.
- `re`: For regular expressions.
- `typing`: For type hints.

## Author

Jinhee Won

## License

This project is licensed under the [MIT License](LICENSE).
