import os


def make_dir(target):
    dir = os.path.join(os.getcwd(), target)
    if not os.path.isdir(dir):
        os.mkdir(dir)


