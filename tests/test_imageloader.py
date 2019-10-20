import os
import pytest
from imageloader import download_url

test_file_path = "test_output.jpg"

def setup_module():
    if os.path.exists(test_file_path):
        os.remove(test_file_path)

def teardown_module():
    if os.path.exists(test_file_path):
        os.remove(test_file_path)

def test_download_not_found():
    assert not download_url("https://server.does.not.exists", test_file_path)

def test_download_url_404():
    assert not download_url("https://google.com/path_does_not_exist", test_file_path)

def test_download_url_success():
    assert download_url("https://picsum.photos/200", test_file_path)
    assert os.path.exists(test_file_path)
    assert os.stat(test_file_path).st_size > 0
