import argparse
import logging
import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor

import requests


def download(url, dest):
    try:
        response = requests.get(url)
        if "image" not in response.headers["Content-Type"]:
            logging.warning(f"{url} - Response object not of type image.")
            return False
    except requests.exceptions.RequestException:
        logging.warning(f"{url} - Could not connect to server.")
        return False
    if response.status_code == 200:
        with open(dest, "wb") as file:
            file.write(response.content)
        logging.info(f"{url} - SUCCESS.")
        return True
    else:
        logging.warning(f"{url} - Image not found on server.")
        return False


def parse_arguments():
    parser = argparse.ArgumentParser(description="Download images in bulk.")
    parser.add_argument(
        "input_file",
        metavar="<Input file>",
        type=str,
        help="The file containing urls of pictures to download.",
    )
    parser.add_argument(
        "-o",
        "--output_path",
        metavar="<Output folder>",
        default=os.getcwd(),
        type=str,
        help="Where the images will be stored.",
    )
    parser.add_argument(
        "-t",
        "--threads",
        metavar="<Output folder>",
        default=8,
        choices=range(1, 256),
        type=int,
        help="Number of concurrent download threads.",
    )
    return vars(parser.parse_args())


def read_unique_lines(file_name):
    lines = []
    with open(file_name, "r") as file:
        for line in file.readlines():
            trimmed = re.sub(r"(\s)+", "", line)
            if len(trimmed) > 0:
                lines.append(trimmed)
            line = file.readline()

    # Remove duplicates while preserving order
    uniqueSet = set()
    return [line for line in lines if line not in uniqueSet and not uniqueSet.add(line)]


def validate_arguments(arguments):
    input_file_path = os.path.realpath(arguments["input_file"])
    if not os.path.exists(input_file_path):
        logging.error(f" File not found: '{input_file_path}'")
        sys.exit(1)
    elif not os.path.isfile(input_file_path):
        logging.error(f" Input file is a directory.")
        sys.exit(1)

    output_path = os.path.realpath(arguments["output_path"])
    if not os.path.exists(output_path):
        logging.error(f" Path does not exist: '{output_path}'")
        sys.exit(1)
    elif os.path.isfile(output_path):
        logging.error(f" Output path is a file.")
        sys.exit(1)
    return True


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    arguments = parse_arguments()
    validate_arguments(arguments)
    urls = read_unique_lines(arguments["input_file"])
    executor = ThreadPoolExecutor(arguments["threads"])
    for i, url in enumerate(urls, start=1):
        output_file = os.path.join(arguments["output_path"], str(i) + ".jpg")
        executor.submit(download, url, output_file)
