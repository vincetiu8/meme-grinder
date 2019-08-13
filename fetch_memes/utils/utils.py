from pathlib import PureWindowsPath, Path
from PIL import Image
import requests
import imagehash
import math
import shutil

def name_to_path(name):
    if isinstance(name, str) or isinstance(name, Path):
        path = Path(name)

        if path.exists():
            return path

    return False

def find(name, id, type):
    path = name_to_path(name)
    if path == False or len(list(path.glob('**/' + id + type))) == 0:
        return False

    return True

def make_dirs(dirs):
    for dir in dirs:
        path = Path('./' + dir)
        if not path.exists():
            path.mkdir()

def copy_files(copy_from, copy_to):
    copy_from_path = name_to_path(copy_from)
    copy_to_path = name_to_path(copy_to)

    if copy_from_path == False or copy_to_path == False:
        return False

    for file in copy_from_path.glob('**/*'):
        shutil.copyfile(file, Path(copy_to_path, file.name))

    return True

def move_files(move_from, move_to):
    if copy_files(move_from, move_to) == False:
        return False

    shutil.rmtree(Path(move_from))

    return True

def download_image(url, desired_size, name_length):
    assert(desired_size > 0)
    assert(math.sqrt(name_length).is_integer())
    response = requests.get(url, stream = True)
    img = Image.open(response.raw)

    old_size = img.size
    if old_size[0] / 2 > old_size[1] or old_size[0] < old_size[1] / 2:
        return True

    ratio = float(desired_size)/max(old_size)
    new_size = tuple([int(x*ratio) for x in old_size])
    img = img.resize(new_size, Image.ANTIALIAS)

    new_img = Image.new("RGB", (desired_size, desired_size))
    new_img.paste(img, ((desired_size - new_size[0]) // 2, (desired_size - new_size[1]) // 2))

    hash_size = int(math.sqrt(name_length) * 2)
    hash = str(imagehash.phash(new_img, hash_size))
    if find('images', hash, '.png'):
        return False
    if find('temp_images', hash, '.png'):
        return True

    new_img.save('temp_images/' + hash + '.png')
    del response
    return True

def move_memes():
    move_files('temp_images', 'images')
