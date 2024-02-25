from setuptools import find_packages, setup
import os

VERSION = '1.0.5'
DESCRIPTION = 'A Python CLI tool to convert FLAC to MP3'

# Read the contents of your README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="flac2mp3-cli",
    version=VERSION,
    packages=find_packages(),
    install_requires=['alive_progress', 'mutagen', 'pydub'],
    entry_points={
        'console_scripts': [
            'flac2mp3=flac2mp3.main:main',
        ],
    },

    author="mariout",
    url='https://github.com/rimaout/flac2mp3',  # replace with your repository URL
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT', 
    keywords=['python', 'audio coverter', 'flac', 'mp3', 'multithreading'],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
    ]
)
