from datetime import *
from pathlib import Path
# If this is a windows environment then import winsound, otherwise we'll use os to run a command.
try:
    import winsound
except:
    import os

class Chime:
    def __init__(self, chime_path: Path, sleep_start_time: time, sleep_end_time: time):
        # Set the sound file from the config.
        self.sound_file = chime_path
        # Get the start time and end time for the sleep period.
        self.sleep_start_time = sleep_start_time
        self.sleep_end_time = sleep_end_time

    def make_noise(self):
        #Check that we are outside of the sleep time.
        if datetime.now().time() > self.sleep_start_time or datetime.now().time() < self.sleep_end_time:
            print('Inside sleep time, not making a sound.')
            return
        #Try and play a sound using winsound, if that fails try aplay for linux.
        try:
            print('Trying to play chime using winsound.')
            winsound.Play_sound(self.sound_file, winsound.SND_FILENAME)
        except:
            print(f'Winsound failed, trying aplay.')
            os.system(f'aplay -D plughw:1,0 {self.sound_file}')