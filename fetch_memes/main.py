from instagram import Instagram_Bot
from reddit import Reddit_Bot
import multiprocessing
import time
import atexit
import shutil
import os
import ctypes

reddit_bot = Reddit_Bot('invincbot', 'Frenchfri365', 5)
insta_bot = Instagram_Bot('mustardmayonaiseketchup', 'Frenchfri365', 5)

def find(id, path):
    for filename in os.listdir(path):
        if filename.startswith(id):
            return True

    return False

def move_memes():
    if find('temp_images', './'):
        for img in os.listdir('temp_images'):
            shutil.copyfile('temp_images/' + img, 'images/' + img)
        shutil.rmtree('temp_images')

atexit.register(move_memes)

if __name__ == '__main__':
    reddit_process = multiprocessing.Process(target=reddit_bot.load_hyperlinks)
    insta_process = multiprocessing.Process(target=insta_bot.load_hyperlinks)
    reddit_process.start()
    time.sleep(1)
    insta_process.start()
    time.sleep(3600)

    if (reddit_process.is_alive()):
        reddit_process.terminate()
    time.sleep(1)
    if (insta_process.is_alive()):
        insta_process.terminate()
