import os

def create_folder_if_not_exists(directory):
    '''
    Create the folder if it doesn't exist already.
    '''
    if not os.path.exists(directory):
        os.makedirs(directory)


def get_all_filepaths(path, file_extension):
    '''
    [How can I search sub-folders using glob.glob module in Python?](https://stackoverflow.com/a/14798263/395857)
    '''
    return [os.path.join(dirpath, f) for dirpath, dirnames, files in os.walk(path) for f in files if f.endswith('.{0}'.format(file_extension))]
