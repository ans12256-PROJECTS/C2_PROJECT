# perform reads and local saves for image files
# file image URLs are stored in *.txt files in
# subdirectory img/test and img/train

# REFERENCES
# https: // sites.google.com/view/yoga-82/home  # h.101pn8sbpigo
# https: // docs.google.com/document/d/19u2VzvK7ql8EPohz_Kfre2SaezqdC-0WBv56pGQ-C-M/edit

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from PIL import Image, ImageOps   # pillow module ImageOps to convert to gray
import requests   # to handle URL objects (Timeout and ConnectionError are used explicitly:
# except requests.exceptions.Timeout:  # 5 seconds no response
from io import BytesIO

# importing os module to check for existence/creation of directories
import os

# location variables
# debugging mode
DEBUG = True

# SOUND EFFECTS
# https://anaconda.org/skmad/simpleaudio
# conda install -c skmad simpleaudio
# https://pypi.org/project/beepy/
# pip install beepy
#
# Following are the mappings for the numbers: 1 : 'coin', 2 : 'robot_error', 3 : 'error', 4 : 'ping', 5 : 'ready', 6 : 'success', 7 : 'wilhelm'
import beepy
# beepy.beep(sound=1) # 1 : 'coin'
# beepy.beep(sound=2) # 2 : 'robot_error'
# beepy.beep(sound=3) # 3 : 'error'
# beepy.beep(sound=4) # 4 : 'ping'
# beepy.beep(sound=5) # 5 : 'ready'
# beepy.beep(sound=6) # 6 : 'success'
# beepy.beep(sound=7) # 7 : 'wilhelm'

def log(s):
    '''
    https://stackoverflow.com/questions/6579496/using-print-statements-only-to-debug
    '''
    if DEBUG:
        print(s)

# https://pythonexamples.org/python-logging-debug/
#  
import logging

class MyFilter(object):
    def __init__(self, level):
        self.__level = level

    def filter(self, logRecord):
        return logRecord.levelno <= self.__level

#create a logger
logger = logging.getLogger('mylogger')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('mylog.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
#set filter to log only DEBUG lines
handler.addFilter(MyFilter(logging.DEBUG))
logger.addHandler(handler)

#write a debug line to log file
logger.debug('This is a DEBUG message')
logger.info('This is a INFO message')
logger.warning('This is a WARNING message')
logger.error('This is an ERROR message')
logger.critical('This is a CRITICAL message')





def File_of_82(file_name_2_process: str, path_2_dump: str, img_display=False):
    '''
    Part of the Yoga-82 workflow
    given a file in the directory with structure
    directory_name/file_name--(tab)-->URL
    1) perform existence of the directory_name, create if needed
    2) loop through file lines by calling img_URL_Read_Display_Write
    3) return updated log in case there were unsuccessful read/writes
    4) path_2_dump is a string to front concatenate to the directory_name_n_file
    '''

    logger.debug(f'Received parameter file_name_2_process: {file_name_2_process}')
    logger.debug(f"pwd={os.getcwd()}")

    # check if passed file parameter exists
    if os.path.isfile(file_name_2_process):  # file exists, open
        file = open(file_name_2_process, 'r')
        beepy.beep(sound=5) # 5 : 'ready'
        log(f'Opened file {file} for processing ===============')
        logger.debug(f'Opened file {file} for processing ===============')
    else:
        log(f'File does not exists: {file_name_2_process}')
        logger.debug(f'File does not exists: {file_name_2_process}')
        return
        
    line_count = 1
        
    for line in file:  
        logger.debug(f'File {file_name_2_process}. Processing line {line_count}: \n {line}')

        # parse the line for URL, remove \n
        # https://www.w3schools.com/tags/ref_urlencode.asp?_sm_au_=iVVDMg0TSmrMV6Dm
        img_url = line.split('\t')[1].rstrip("\n")  #\n becomes %0A when passed to requests.get()
        logger.debug(f'img_url = {img_url}')

        directory_name_n_file = path_2_dump + line.split('\t')[0]  # Camel_Pose_or_Ustrasana_/99.jpg
        directory_name = path_2_dump + line.split('\t')[0].split('/')[0]  # Camel_Pose_or_Ustrasana_

        # check if directory_name exists, create one if does not
        if os.path.isdir(directory_name):
            # directory exists in !pwd
            logger.debug(f'Directory {directory_name} exists')
        else:
            os.mkdir(directory_name)
            logger.debug(f'Directory {directory_name} was CREATED!')

        # process the line to feed img_URL_Read_Display_Write
        if os.path.isfile(directory_name_n_file):  # file exists, skip
            logger.debug(f'File {directory_name_n_file} exists, skipping read/write!')

        else:  # call file read/write subroutine
            img_URL_Read_Display_Write(img_url,
                                       save_location=directory_name_n_file,
                                       img_display=img_display)
        line_count += 1


    file.close()  # very important AFTER successful completion.
    log(f'Closed {file}  #####################')
    logger.debug(f'Closed {file}  #####################')
    beepy.beep(sound=6) # 6 : 'success'
    return


def img_URL_Read_Display_Write(img_url: str, save_location: str, img_display=False, verbose=False):
    '''
    given image URL, load image into memory
    display,
    save locally at save_location
    provide progress feedback if verbose=True
    type hints: https://docs.python.org/3/library/typing.html

    One of 82 txt files in directory "yoga_dataset_links" for example
    Akarna_Dhanurasana.txt with structure
        Akarna_Dhanurasana/680.jpg	http://allyogapositions.com/ ... /archer-pose-yoga-_13.jpg
        Akarna_Dhanurasana/478.jpg	http://nicholchaseyoga.com/.../IMG_2857.jpg
    here
        save_location = 'Akarna_Dhanurasana/680.jpg'  (check/create directory Akarna_Dhanurasana)
        img_url = 'http://allyogapositions.com/ ... /archer-pose-yoga-_13.jpg'
    '''

    # check if file has already been downloaded
    # separate name of the file from the

    # beepy.beep(sound=1) # 1 : 'coin'
    # beepy.beep(sound=2) # 2 : 'robot_error'
    # beepy.beep(sound=3) # 3 : 'error'
    # beepy.beep(sound=4) # 4 : 'ping'
    # beepy.beep(sound=5) # 5 : 'ready'
    # beepy.beep(sound=6) # 6 : 'success'
    # beepy.beep(sound=7) # 7 : 'wilhelm'

    # reading block:
    # turns out timeout was needed, refer
    # https://docs.python-requests.org/en/master/user/quickstart/
    # https://docs.python-requests.org/en/master/user/advanced/#advanced
    # Without a timeout, your code may hang for minutes or more.
    try:
        logger.debug(f'img_url = {img_url}')
        response = requests.get(img_url, timeout=(5,5))  # timeout for connect and read
        img_PIL = Image.open(BytesIO(response.content))
#        img_np = np.array(Image.open(BytesIO(response.content)))
        read_error = False  # assign reading result

    except requests.exceptions.Timeout:  # 5 seconds no response
        read_error = True  # assign reading result
        beepy.beep(sound=3) # 3 : 'error'
        logger.debug(f'Attempt to open image file failed due to 5 sec TIMEOUT: \n {img_url}')

    except requests.exceptions.ConnectionError:  # 5 seconds no connection
        read_error = True  # assign reading result
        beepy.beep(sound=2) # 2 : 'robot_error'
        logger.debug(f'Attempt to open image file failed due to 5 sec CONNECTION_ERROR: \n {img_url}')
        
    except:  # No need to be specific about the error: Name is not defined  InvalidSchema
        read_error = True  # assign reading result
        beepy.beep(sound=7) # 7 : 'wilhelm'
        logger.debug(f'Attempt to open image file failed for UNKNOWN REASON: \n {img_url}')
        # log message

    # display block
    if not read_error and img_display:   # if read and display are both True
        # display block
        # applying grayscale method
        gray_image = ImageOps.grayscale(img_PIL)
        img_np_gr = np.array(gray_image)

        fig, ax = plt.subplots(1, 2, figsize=(15, 10))  # , figsize=(15, 20)
        ax[0].imshow(img_np)
        ax[1].imshow(img_np_gr, cmap='gray')
        plt.draw()
        plt.show(block=False)  # needed for python in Code

    # save locally block
    if not read_error:   # if read and display are both True
        gray_image = ImageOps.grayscale(img_PIL)
#         img_np_gr = np.array(gray_image)

        gray_image.save(save_location)  # directory_name_n_file variable
        logger.debug(f'Saved gray version of the file at {save_location}')


    return


# File_of_82('../data/TEST/Akarna_Dhanurasana_2_files.txt', path_2_dump='../img/test/', img_display=True)
