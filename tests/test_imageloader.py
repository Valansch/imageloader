import os
from sys import exit

from mock import patch

from imageloader import download, read_unique_lines, validate_arguments

test_input_file_name = "test_input.txt"
test_input_file_content = (
    " https://goog le.com\nhttps://google.com\n https://example.org"
)
test_output_folder_path = "test_output"
test_file_output_file_path = "test_output.jpg"


def rm(inode_path):
    if os.path.isfile(inode_path):
        os.remove(inode_path)
    else:
        os.rmdir(inode_path)


def setup_module():
    if os.path.exists(test_file_output_file_path):
        rm(test_file_output_file_path)
    if os.path.exists(test_output_folder_path):
        rm(test_output_folder_path)
    with open(test_input_file_name, "w") as test_input_file:
        test_input_file.write(test_input_file_content)


def teardown_module():
    if os.path.exists(test_file_output_file_path):
        rm(test_file_output_file_path)
    if os.path.exists(test_input_file_name):
        rm(test_input_file_name)
    if os.path.exists(test_output_folder_path):
        rm(test_output_folder_path)


def test_download_not_found():
    assert not download("https://server.does.not.exists", test_file_output_file_path)


def test_download_url_404():
    assert not download(
        "https://google.com/path_does_not_exist", test_file_output_file_path
    )


def test_download_url_success():
    assert download("https://picsum.photos/200", test_file_output_file_path)
    assert os.path.exists(test_file_output_file_path)
    assert os.stat(test_file_output_file_path).st_size > 0


def test_read_unique_lines():
    lines = read_unique_lines(test_input_file_name)
    assert lines == ["https://google.com", "https://example.org"]


@patch("sys.exit")
def test_validate_arguments(mockExit):

    os.mkdir(test_output_folder_path)
    arguments = {
        "input_file": test_input_file_name,
        "output_path": test_output_folder_path,
    }
    assert validate_arguments(arguments)  # Everything working

    # Output folder missing
    rm(test_output_folder_path)
    validate_arguments(arguments)
    assert mockExit.call_count > 0 and mockExit.call_args_list[0].args[0] == -1

    # Input file missing
    os.mkdir(test_output_folder_path)
    rm(test_input_file_name)
    validate_arguments(arguments)
    assert mockExit.call_args_list[1].args[0] == -1

    # Input file is a directory
    os.mkdir(test_input_file_name)
    validate_arguments(arguments)
    assert mockExit.call_args_list[2].args[0] == -1

    # Output folder is a file
    rm(test_input_file_name)
    with open(test_input_file_name, "w") as f:
        f.write(test_input_file_content)
    rm(test_output_folder_path)
    with open(test_output_folder_path, "w") as f:
        f.write(test_output_folder_path)
    validate_arguments(arguments)
    assert mockExit.call_args_list[3].args[0] == -1
