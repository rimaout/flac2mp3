
# Command line arguments
import argparse, os
from mutagen.flac import FLAC   # Metadata
from pydub import AudioSegment  # Audio processing


def collect_args():
    parser = argparse.ArgumentParser(description='This script converts .flac files to .mp3 files, It provides functionality to convert a single FLAC file or all FLAC files within a directory and its subdirectories.')
    parser.add_argument('input_path', type=str, nargs='?', default=os.getcwd(), help='The path to the directory containing the files to process. Default is the current directory.')
    parser.add_argument('--num_threads', '-t', type=int, default=1, help='The number of threads to use. Default is 1.')
    parser.add_argument('--output_path', '-o', type=str, default=None, help='The path to the directory where the output files will be saved. Default is the same directory as the input file.')

    args = parser.parse_args()
    
    #Is a path
    if not os.path.exists(args.input_path):
        parser.error("The file_path %s does not exist!" % args.input_path)

    # check if the number of threads is an integer
    if not isinstance(args.num_threads, int):
        parser.error("The number of threads must be an integer")
        
    if args.num_threads < 1:
        parser.error("The number of threads must be at least 1")
    
    if args.output_path is None: 
        # if the output_path is not specified

        if os.path.isfile(args.input_path): 
            # if the input_path is a file, the output_path is the directory of the input_path
            args.output_path = os.path.dirname(args.input_path) 
        
        else: 
            # if the input_path is a directory, the output_path is the input_path + "_converted"
            args.output_path = args.input_path + "_converted" 

    if not os.path.isdir(args.output_path):
        parser.error("The output_path %s is not a directory!" % args.output_path)

    return args.input_path, args.num_threads, args.output_path
  
    
def dir_scan(input_dir):
    '''
    Funcion that scans a given directory and return the number of files, and a list of the file_paths to the files
    '''

    flac_count = 0
    flac_list = []
    file_count = 0
    file_list = []

    for elem in os.listdir(input_dir):
        elem_path = os.path.join(input_dir, elem)

        # if file is a directory, call the function recursively
        if os.path.isdir(elem_path):
            recursive_flac_count, recursive_flac_list, recursive_file_count, recursive_file_list = dir_scan(elem_path)
            
            flac_count += recursive_flac_count
            flac_list.extend(recursive_flac_list)
            
            file_count += recursive_file_count
            file_list.extend(recursive_file_list)
            
        elif elem.endswith(".flac"):
            flac_count += 1
            flac_list.append(elem_path)
        
        else:
            file_count += 1
            file_list.append(elem_path)
            
    return flac_count, flac_list, file_count, file_list


def replace_extension(file, new_extension):
    # replace file extension
    return os.path.splitext(file)[0] + new_extension


def get_metadata(file):
    # get metadata from flac file

    metadata = FLAC(file)
    tags = {}
    for data in metadata:
        tags[data] = metadata[data][0]
    return tags


def flac_mp3(input_file_path, output_file_path):
    # convert flac file to mp3
    flac_audio = AudioSegment.from_file(input_file_path, format="flac")
    flac_audio.export(output_file_path, format="mp3", bitrate="320k", tags=get_metadata(input_file_path))