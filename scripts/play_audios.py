import csv
import os
from pynput import keyboard
import simpleaudio as sa  # For playing audio

DATA_PATH = "/home/mariam/tts/EAED/EAED/EAED/AshamIblis"
# DATA_PATH = "C:/Users/mahmoud/projects/TTS/EAED/AshamIblis"

# Path to the transcriptions.csv file
transcriptions_csv = "transcriptions.csv"



# Function to wait for key press actions
def wait_for_key():
    with keyboard.Listener(on_press=on_key_press) as listener:
        listener.join()

# Action for key press
def on_key_press(key):
    global play_obj, wave_obj
    try:
        if key == keyboard.Key.enter:
            return False  # Stop listener (move to next audio)
        elif key.char == 'r':
            if play_obj:
                play_obj.stop()  # Stop the current playback if any
            play_audio(wave_obj)  # Repeat the audio
    except AttributeError:
        pass  # Handle special keys like 'Enter' or other non-character keys

# Function to play audio
def play_audio(wave_obj):
    global play_obj
    play_obj = wave_obj.play()
    play_obj.wait_done()  # Wait for the audio to finish



# Start index for audio files 
start = 0

# Play audios in reverse order if True
reversed = False
# reversed = True

# Read the CSV file
with open(transcriptions_csv, mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)

    rows = list(reader)

    # Counter for processed audio files
    audio_counter = start



    

    # Iterate through the rows in the CSV
    if reversed:
        rows = rows[start::-1]
    else:
        rows = rows[start:]

    
    for row in rows:
        # Extract file path and other details
        speaker = row["Speaker"]
        emotion = row["Emotion"]
        file_name = row["File Name"]
        transcription = row["Transcription"]
        
        # Construct the full file path
        file_path = os.path.join(DATA_PATH , speaker, emotion, file_name)
        
        if not os.path.isfile(file_path):
            print(f"Audio file not found: {file_path}")
            continue
        
        try:
            # Increment audio counter
            if reversed:
                audio_counter -= 1
            else:
                audio_counter += 1
            
            # Print details before playing audio
            print(f"\nPlaying audio {audio_counter}: {file_name}")
            print(f"Speaker: {speaker}, Emotion: {emotion}, Transcription: {transcription}")
            
            # Load the audio
            wave_obj = sa.WaveObject.from_wave_file(file_path)
            
            # Play the audio
            play_audio(wave_obj)
            
            # Wait for Enter key to proceed to next audio
            print("Press Enter to continue or 'r' to repeat the audio...")
            wait_for_key()
        
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

