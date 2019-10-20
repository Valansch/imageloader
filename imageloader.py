import requests
import argparse
import os
import re
import sys


def download(url, dest):
    try:
        response = requests.get(url)
        if not "image" in response.headers["Content-Type"]:
            print("Source is not an image.")
            return False
    except requests.exceptions.RequestException:
        print("Could not connect to server with url: " + url)
        return False
    if response.status_code == 200:
        with open(dest, "wb") as file:
            file.write(response.content)
        return True
    else:
        print("Not found.")
        return False

def parse_arguments():
    parser = argparse.ArgumentParser(description='Download images in bulk.')
    parser.add_argument('input_file', metavar='<Input file>', type=str, help='The file containing urls of pictures to download.')
    parser.add_argument('-o', '--output_path', metavar='<Output folder>', default=os.getcwd(), type=str, help='Where the images will be stored.')
    return vars(parser.parse_args())

def read_unique_lines(file_name):
    lines = []
    with open(file_name, "r") as file:
        line = file.readline()
        while line:
            trimmed = re.sub(r'(\s)+', '', line)
            if len(trimmed) > 0:
                lines.append(trimmed)
            line = file.readline()
    
    lines = list(dict.fromkeys(lines)) #Remove duplicates
    return lines

def validate_arguments(arguments):
    if not os.path.exists(arguments["input_file"]):
        #TODO: Paste error
        sys.exit(-1)
    if arguments["output_path"] != None:
        if not os.path.exists(arguments["output_path"]):
            #TODO: Paste error
            sys.exit(-1)


def main():
    arguments = parse_arguments()
    validate_arguments(arguments)
    urls = read_unique_lines(arguments["input_file"])
    for i, url in enumerate(urls, start=1):
        download(url, os.path.join(arguments["output_path"], str(i) + ".jpg"))
main()


