import os

from mock import patch

from imageloader import download, read_unique_lines, validate_arguments

test_input_file_name = "test_input.txt"
test_input_file_content = (
    " https://goog le.com\nhttps://google.com\n https://example.org"
)
test_output_folder_path = "test_output"
test_file_output_file_path = "test_output.jpg"
arguments = {"input_file": test_input_file_name, "output_path": test_output_folder_path}


def rm(inode_path):
    if os.path.exists(inode_path):
        if os.path.isfile(inode_path):
            os.remove(inode_path)
        else:
            os.rmdir(inode_path)


def setup_module():
    rm(test_file_output_file_path)
    rm(test_output_folder_path)
    os.mkdir(test_output_folder_path)
    with open(test_input_file_name, "w") as test_input_file:
        test_input_file.write(test_input_file_content)


def teardown_module():
    rm(test_file_output_file_path)
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


def test_validate_arguments_valid():
    assert validate_arguments(arguments)  # Everything working


@patch("sys.exit")
def test_validate_arguments_no_output_folder(mockExit):
    rm(test_output_folder_path)
    validate_arguments(arguments)
    assert mockExit.call_count > 0 and mockExit.call_args_list[0].args[0] != 0


@patch("sys.exit")
def test_validate_arguments_no_input_file(mockExit):
    rm(test_input_file_name)
    validate_arguments(arguments)
    assert mockExit.call_count > 0 and mockExit.call_args_list[0].args[0] != 0


@patch("sys.exit")
def test_validate_arguments_input_file_is_directory(mockExit):
    rm(test_input_file_name)
    os.mkdir(test_input_file_name)
    validate_arguments(arguments)
    assert mockExit.call_count > 0 and mockExit.call_args_list[0].args[0] != 0


@patch("sys.exit")
def test_validate_arguments_output_folder_is_file(mockExit):
    rm(test_output_folder_path)
    open(test_output_folder_path, "a").close()
    validate_arguments(arguments)
    assert mockExit.call_count > 0 and mockExit.call_args_list[0].args[0] != 0
