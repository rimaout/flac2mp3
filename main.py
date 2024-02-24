from pydub import AudioSegment  # Audio conversion 
from mutagen.flac import FLAC   # Metadata

import os, shutil # file system
import itertools, threading, time, sys # Animation

def main():
    
    input_dir = input("Enter file path to flac file or directory:")
    
    done = False
    start_time = time.time()

    # if input is a file, convert it to mp3
    if os.path.isfile(input_dir):
        single_file_conversion(input_dir)
        done = True
        return
    
    # input is a directory
    else:
        # create output directory
        output_dir = f"{input_dir}_converted" 
        os.makedirs(output_dir, exist_ok=True)

        # convert flac files to mp3 recursively
        count = [0]
        directory_flac_to_mp3(input_dir, output_dir, count)
        
        # print number of files converted (end)
        done = True
        print(f"Done!, {count[0]} flac files converted to mp3 in {time.time() - start_time} seconds")
        return

# convert single file to mp3
def single_file_conversion(file):
    # if file is a flac file, convert it to mp3
    if input_dir.endswith(".flac"):
        output_dir = f"{input_dir[:-5]}.mp3"
        flac_mp3(input_dir, output_dir)
        print(f"Converted {input_dir} to {output_dir}")
        
    # if file is not a flac file
    else:
        print("File is not a flac file")



def directory_flac_to_mp3(input_dir, output_dir, count):
    # recursive function to convert flac files to mp3, and subdirectories
    
    for file in os.listdir(input_dir):
        
        # if file is a flac file, convert it to mp3
        if file.endswith(".flac"):
            flac_mp3(f"{input_dir}/{file}", f"{output_dir}/{file[:-5]}.mp3")
            count[0] += 1

        # if file is a directory, call the function recursively
        elif os.path.isdir(f"{input_dir}/{file}"):
            os.makedirs(f"{output_dir}/{file}", exist_ok=True)
            directory_flac_to_mp3(f"{input_dir}/{file}", f"{output_dir}/{file}", count)

        # if file is not flac, copy file to output directory
        else:
            shutil.copy(f"{input_dir}/{file}", f"{output_dir}/{file}")

def get_metadata(file):
    # get metadata from flac file
    metadata = FLAC(file)
    tags = {}
    for data in metadata:
        tags[data] = metadata[data][0]
    return tags

def flac_mp3(file_in, file_out):
    # convert flac to mp3
    flac_audio = AudioSegment.from_file(file_in, format="flac")
    flac_audio.export(file_out, format="mp3", bitrate="320k", tags=get_metadata(file_in))

if __name__ == "__main__":
    main()