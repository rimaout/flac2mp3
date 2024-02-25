#from . import custom_functions as cf
import custom_functions as cf
import os, shutil, time, sys

from concurrent.futures import ThreadPoolExecutor # Multithreading
from alive_progress import alive_bar # Progress bar



def single_file_conversion(file_path, output_dir, bar):
    # convert single file to mp3
    
    if file_path.endswith(".flac"):  # if file is a flac file, convert it to mp3
        output_path = output_dir + "/" + os.path.basename(file_path).replace(".flac", ".mp3")
        cf.flac_mp3(file_path, output_path)
        flac_count, file_count = [1], [0]
        bar()

    else:
        print("File is not a flac file")
        sys.exit(1)

    return flac_count, file_count

def flac_conversion(input_file_path, output_file_path, flac_count, bar):
    # convert flac file to mp3
    cf.flac_mp3(input_file_path, output_file_path)
    flac_count[0] += 1
    bar()


def file_copy(input_file_path, output_file_path, file_count, bar):
    # copy file to output directory
    shutil.copy(input_file_path, output_file_path)
    file_count[0] += 1
    bar()


def flac_thread(flac_list, input_dir, output_dir, flac_count, theads_count, bar):
        with ThreadPoolExecutor(max_workers=theads_count) as executor:
            futures = []
            for file_path in flac_list:
            
                output_file_path = file_path.replace(input_dir, output_dir).replace(".flac", ".mp3")
                os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
                futures.append(executor.submit(flac_conversion, file_path, output_file_path, flac_count, bar))
            
            for future in futures:
                future.result()


def file_thread(file_list, input_dir, output_dir, file_count, theads_count, bar):
        with ThreadPoolExecutor(max_workers=theads_count) as executor:
            futures = []
            for file_path in file_list:
                
                output_file_path = file_path.replace(input_dir, output_dir)
                os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
                futures.append(executor.submit(file_copy, file_path, output_file_path, file_count, bar))

            for future in futures:
                future.result()


def main():
    input_path, thread_count, output_path = cf.collect_args()
    input_path = os.path.abspath(input_path)
    output_path = os.path.abspath(output_path)
    start_time = time.time()

    if os.path.isfile(input_path):
        with alive_bar(title="Processing single file:", bar=False, spinner_length=5, receipt=False, elapsed=False, stats=None, monitor=False) as bar:
            flac_count, file_count = single_file_conversion(input_path, output_path, bar)
       
    else:
        flac_count, file_count = [0], [0]
        flac_total, flac_list, file_total, file_list = cf.dir_scan(input_path)
 
        os.makedirs(output_path, exist_ok=True)

        with alive_bar(flac_total, title="Processing flac files:", bar="notes", spinner_length=5, receipt=False, elapsed=False, stats=None) as bar:
            flac_thread(flac_list, input_path, output_path, flac_count, thread_count, bar)

        with alive_bar(file_total, title="Coping other files:", bar="smooth", spinner_length=5, receipt=False, elapsed=False, stats=None) as bar:
            file_thread(file_list, input_path, output_path, file_count, thread_count, bar)

    total_time = time.time() - start_time
    minutes = int(total_time // 60)
    seconds = int(round(total_time % 60))
    print(f"Done! Converted {flac_count[0]} flac files and copied {file_count[0]} files in {minutes}.{seconds} minutes.")

if __name__ == "__main__":
    main()