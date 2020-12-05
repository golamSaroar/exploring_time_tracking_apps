import datetime


def write(log_text):
    with open('log.txt', 'a') as log:
        log.write(str(datetime.datetime.now()) + ": " + log_text + '\n')