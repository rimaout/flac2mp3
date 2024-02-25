#script description: 
# This script converts flac files to mp3 files. It can be used to convert a single file or a directory containing flac files. 

# Audio conversion
from pydub import AudioSegment  # Audio conversion 
from mutagen.flac import FLAC   # Metadata

# Progress bar
from alive_progress import alive_bar
import time

#File handling
import os, shutil

# Command line arguments
import argparse

def collect_args():
    parser = argparse.ArgumentParser(description='This script converts .flac files to .mp3 files, It provides functionality to convert a single FLAC file or all FLAC files within a directory and its subdirectories.')
    parser.add_argument('filepath', type=str, nargs='?', default=os.getcwd(), help='The path to the directory containing the files to process. Default is the current directory.')
    parser.add_argument('--num_threads', type=int, default=1, help='The number of threads to use. Default is 1.')

    args = parser.parse_args()
    
    #Is a path
    if not os.path.exists(args.filepath):
        parser.error("The file_path %s does not exist!" % args.filepath)

    # check if the number of threads is an integer
    if not isinstance(args.num_threads, int):
        parser.error("The number of threads must be an integer")
        
    if args.num_threads < 1:
        parser.error("The number of threads must be at least 1")
    
    return args.filepath, args.num_threads

def count_flac(input_path):
    # if input is a single file, return 1
    if os.path.isfile(input_path):
        if input_path.endswith(".flac"):
            return 1
        else:
            return 0
    
    # if input is a directory, count flac files recursively
    flac_count = 0
    for elem in os.listdir(input_path):
        elem_path = os.path.join(input_path, elem)

        # if file is a flac file, convert it to mp3
        if elem.endswith(".flac"):
            flac_count += 1

        # if file is a directory, call the function recursively
        elif os.path.isdir(elem_path):
            flac_count += count_flac(elem_path)
            
    return flac_count

def replace_extension(file, new_extension):
    # replace file extension
    return os.path.splitext(file)[0] + new_extension


def single_file_conversion(file):
    # convert single file to mp3
    
    if file.endswith(".flac"):  # if file is a flac file, convert it to mp3
        flac_mp3(file, replace_extension(file, ".mp3"))
        count[0] += 1
        bar()

    else:
        print("File is not a flac file")


def directory_flac_to_mp3(input_dir, output_dir, flac_count):
    # recursive function to convert flac files to mp3, and subdirectories
   
    for file in os.listdir(input_dir):
        input_file_path = os.path.join(input_dir, file)
        output_file_path = os.path.join(output_dir, file)

        # if file is a flac file, convert it to mp3
        if file.endswith(".flac"):
            flac_mp3(input_file_path, replace_extension(output_file_path, ".mp3"))
            flac_count[0] += 1
            bar()

        # if file is a directory, call the function recursively
        elif os.path.isdir(input_file_path):
            os.makedirs(output_file_path, exist_ok=True)
            directory_flac_to_mp3(input_file_path, output_file_path, flac_count)

        # if file is not flac, copy file to output directory
        else:
            shutil.copy(input_file_path, output_file_path)


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


def main(input_dir, start_time, flac_count):
    
    # if input is a single file, convert it to mp3
    if os.path.isfile(input_dir):
        single_file_conversion(input_dir)

    # input is a directory
    else:
        # create output directory
        output_dir = f"{input_dir}_converted" 
        os.makedirs(output_dir, exist_ok=True)

        # convert flac files to mp3 recursively
        directory_flac_to_mp3(input_dir, output_dir, flac_count)

if __name__ == "__main__":
    input_path, thread_count = collect_args()

    start_time = time.time()
    flac_count = [0]
    flac_total = count_flac(input_path)

    with alive_bar(flac_total, title="Processing:", bar="notes", spinner_length=5, receipt=False, elapsed=False, stats=None) as bar:
        main(input_path, start_time, flac_count)

    total_time = time.time() - start_time
    minutes = int(total_time // 60)
    seconds = int(round(total_time % 60))
    print(f"Done! Converted {flac_count[0]} files in {minutes}:{seconds} minutes.")