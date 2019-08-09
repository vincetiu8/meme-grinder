from instagram import Instagram_Bot
from reddit import Reddit_Bot
import multiprocessing
import time

reddit_bot = Reddit_Bot('invincbot', 'Frenchfri365', 5, 1024, 144)
insta_bot = Instagram_Bot('mustardmayonaiseketchup', 'Frenchfri365', 5, 1024, 144)

if __name__ == '__main__':
    reddit_process = multiprocessing.Process(target=reddit_bot.load_hyperlinks)
    insta_process = multiprocessing.Process(target=insta_bot.load_hyperlinks)
    reddit_process.start()
    time.sleep(1)
    print("@#@43")
    insta_process.start()
    time.sleep(3600)

    print("@#@43")
    if (reddit_process.is_alive()):
        reddit_process.terminate()
    time.sleep(1)
    if (insta_process.is_alive()):
        insta_process.terminate()
