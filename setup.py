from setuptools import find_packages, setup


VERSION = '1.0.1'
DESCRIPTION = 'A Python CLI tool to convert FLAC to MP3'
LONG_DESCRIPTION = 'A robust package for converting FLAC files to MP3 and copying files. It supports single file and directory conversion, and leverages multithreading for efficient processing.'


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

    #metadata to display on PyPI
    author="mariout",
    url='https://github.com/yourusername/your-repo',  # replace with your repository URL
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
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
