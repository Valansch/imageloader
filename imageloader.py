import requests
import argparse


def download_url(url, dest):
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException:
        print("Could not connect to server.")
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
    parser.add_argument('-o', '--output_path', metavar='<Output folder>', type=str, help='Where the images will be stored.')
    return vars(parser.parse_args())
