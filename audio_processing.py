import whisper_timestamped as whisper
import json

audio = whisper.load_audio("cut_audio.wav")
model = whisper.load_model("medium.en")
result = whisper.transcribe(model, audio, language="en")

with open("audio_segmentation.json", "w") as f:
    # Iterate over each segment
    for segment in result["segments"]:
        segment_dict = {
            "start": segment["start"] + 1707189581.1579618,
            "end": segment["end"] + 1707189581.1579618,
            "words": []  # Initialize a list to store words and their timestamps
        }
        # Iterate over each word in the segment
        for word in segment["words"]:
            word_dict = {
                "word": word["text"],
                "timestamp": word["start"] + 1707189581.1579618  # Add the word's timestamp
            }
            segment_dict["words"].append(word_dict)  # Append the word object to the list
        # Write the segment dictionary to the output file
        f.write(json.dumps(segment_dict) + "\n")
