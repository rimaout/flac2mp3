# flac2mp3

Python-based CLI audio format converter specifically designed for FLAC to MP3 conversions.

### Install Package
```shell
pip install flac2mp3-cli
```
# FLAC to MP3 Converter

This program is a multi-threaded FLAC to MP3 converter. It can convert a single FLAC file, or it can convert multiple FLAC files in a directory. Non-FLAC files in the directory are copied without conversion. The metadata of the original FLAC files is maintained in the converted MP3 files.

## Usage

To run the program, use the following command:

```bash
python main.py <input_path> [<thread_count>] [<output_path>]
```

**Where:**

- `<input_path>` is the path to the FLAC file or directory of FLAC files to convert.
- `<thread_count>` (optional) is the number of threads to use for conversion. If not provided, the program will use a default value.
- `<output_path>` (optional) is the path to the directory where the converted MP3 files (and copied non-FLAC files) should be saved. If not provided, the program will save the files in a default directory.

### Converting a Single File

To convert a single FLAC file, provide the path to the file as the `<input_path>`:

```bash
python main.py python main.py /path/to/your/file.flac
```

### Converting a Directory

To convert all FLAC files in a directory, provide the path to the directory as the `<input_path>`:

```bash
python main.py /path/to/your/directory
```

All FLAC files in the directory (and its subdirectories) will be converted to MP3.

## Dependencies

This program uses the following Python packages:

- `alive_progress` for progress bars
- `concurrent.futures` for multi-threading
- `os` and `shutil` for file and directory operations
- `sys` and `time` for system operations

## License

This program is released under the MIT License. See the `LICENSE` file for more details.