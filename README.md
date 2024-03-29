# Imageloader

A tool to download images in bulk. The urls are provided via a text file passed to the tool via commandline arguments.



# Installation

Simply clone the repository. No further requirements are needed.

```
git clone https://github.com/Valansch/imageloader.git
```



# Run

Use python3 to call imageloader.py directly:

```
python3 imageloader input.txt
```



# Usage



```
usage: imageloader.py [-h] [-o <Output path>] [-t <Number>] <Input file>

Download images in bulk.

positional arguments:
  <Input file>          The file containing urls of pictures to download.

optional arguments:
  -h, --help            show this help message and exit
  -o <Output path>, --output_path <Output path>
                        Where the images will be stored.
  -t <Number>, --threads <Number>
                        Number of concurrent download threads.

```

