"""
sript to get the transcriptions of the audios
"""

import os
import csv
from klaam import SpeechRecognition

# Initialize the SpeechRecognition model
model = SpeechRecognition(lang='egy')

# Directory containing the dataset
dataset_dir = "/home/mariam/tts/EAED/EAED/EAED/AshamIblis"

# Output CSV file to store transcriptions
output_csv = "transcriptions.csv"

# Open the CSV file for writing
with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    # Write the header row
    writer.writerow(["Speaker", "Emotion", "File Name", "Transcription"])
    
    # Walk through the dataset directory
    for root, dirs, files in os.walk(dataset_dir):
        for filename in files:
            if filename.endswith(".wav"):  # Process only .wav files
                # Get full path to the audio file
                file_path = os.path.join(root, filename)
                
                # Extract speaker and emotion from the directory structure
                parts = file_path.replace(dataset_dir, "").strip(os.sep).split(os.sep)
                speaker = parts[0] if len(parts) > 0 else "Unknown"
                emotion = parts[1] if len(parts) > 1 else "Unknown"
                
                try:
                    # Transcribe the audio file
                    transcription = model.transcribe(file_path)
                    
                    # Write the transcription to the CSV file
                    writer.writerow([speaker, emotion, filename, transcription])
                    print(f"Transcribed: {file_path}")
                
                except Exception as e:
                    print(f"Error transcribing {file_path}: {e}")

print(f"Transcriptions saved to {output_csv}")

