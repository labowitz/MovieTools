<<<<<<< HEAD
import argparse
import os.path as ospath
import re
from datetime import datetime
from functools import partial
from multiprocessing import Pool
from os import listdir, mkdir
from utils.ImgUtils import save2stack

import imageio
import numpy as np
from colorama import Back
from numba import jit

folderRe = re.compile(r'Scan \'[^\']+\' (\d\d\d\d-\d\d-\d\d \d\d.\d\d.\d\d)')
wellRe = re.compile(r'([A-Z]\d\d).png')

# Get the datetime from the folder name
def getTimeInfo(x):
    match = folderRe.search(x)
    takeDate = datetime.strptime(match.group(1), '%Y-%m-%d %H.%M.%S')
    return takeDate

# Return a 3-D stack of a specific position
def extractEachWell(pos, wDir, folderList, oDir):
    allImgs = []
    shapes = []
    for folder in folderList:
        img = imageio.imread('{0}/{1}/{2}'.format(wDir, folder, pos))
        arrImg = np.array(img.astype(np.int16))
        arrImg = arrImg.sum(2)
        shapes.append(arrImg.shape)
        allImgs.append(arrImg)
    
    shapes = np.array(shapes)
    minShape = shapes.min(axis=0)

    allImgs = [img[0:minShape[0], 0:minShape[1]] for img in allImgs]
    arrImgStack = np.array(allImgs, dtype=np.uint16)
    
    print('Finished processing position #{0}'.format(pos[0:-4]))

    save2stack(arrImgStack, '{0}/RawMovieStack/{1}.tiff'.format(oDir, pos[0:-4]))
    
    return arrImgStack


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="A script to combine seperated images from a serise of snapshots taken by EVOS, and compile each well into a stack. \n\
        Runs at the parental folder, folder for each date expample: \"Scan 'LT_ibidi24' 2020-01-23 12.34.31\" \n\
        File example: A03.png (single channel only, RGB images will be merged to single channel)\n\
        The output will be several stacks + a csv for datetimes, in the format of \'2011-11-04T00:05:23\' (ISO 8601) \n\
        WARNING: The script is extreme RAM inefficient! But should be OK for movies with relative low frame rate.") 
    parser.add_argument("WorkDir", help="The directory containing all the images (only ends with .TIF)")
    parser.add_argument("-o", "--Output", help="The directory for stack output")    
    parser.add_argument("-t", "--MultiThread", type=int, default=1, help="Number of thread to use, default = 1")
    args = parser.parse_args()
    
    # Handling parameters
    wDir = args.WorkDir
    print(Back.RED + 'WARNING: The script is extreme RAM inefficient! But should be OK for movies with relative low frame rate.')
    print("Start working in " + wDir)

    if args.Output:
        oDir = args.Output
    else:
        oDir = wDir
    print("Output to " + oDir)


    mtNum = args.MultiThread

    if mtNum == 1:
        multiP = False
    elif mtNum < 1:
        print("Not valid thread number, now working in single thread mode")
        multiP = False
    else:
        multiP = True

    # Making the list of images need to be processed
    allSubFolders = [folder for folder in listdir(wDir) if folderRe.match(folder)]
    allSubFolders.sort()
    # print(allSubFolders)
    positions = [well for well in listdir('{0}/{1}'.format(wDir, allSubFolders[0])) if wellRe.match(well)]
    positions = set(positions)
    
    # Make the folder
    if not ospath.isdir(oDir+'\\{0}'.format("RawMovieStack")):
        mkdir(oDir+'\\{0}'.format("RawMovieStack"))

    # Processing the images
    if multiP:
        print("Starting {0} threads......".format(mtNum))
        mtWorker = partial(extractEachWell, wDir=wDir, folderList=allSubFolders, oDir=oDir)
        with Pool(mtNum) as p:
            allStacks = p.map(mtWorker, positions)
    else:
        print("Single thread mode")
        allStacks = []
        for pos in positions:
            allStacks.append(extractEachWell(pos, wDir, allSubFolders, oDir))

    stackShapes = np.array([stack.shape for stack in allStacks])
    minStackShape = stackShapes.min(axis=0)
=======
import argparse
import os.path as ospath
import re
from datetime import datetime
from functools import partial
from multiprocessing import Pool
from os import listdir, mkdir
from utils.ImgUtils import save2stack

import imageio
import numpy as np
from colorama import Back
from numba import jit

folderRe = re.compile(r'Scan \'[^\']+\' (\d\d\d\d-\d\d-\d\d \d\d.\d\d.\d\d)')
wellRe = re.compile(r'([A-Z]\d\d).png')

# Get the datetime from the folder name
def getTimeInfo(x):
    match = folderRe.search(x)
    takeDate = datetime.strptime(match.group(1), '%Y-%m-%d %H.%M.%S')
    return takeDate

# Return a 3-D stack of a specific position
def extractEachWell(pos, wDir, folderList, oDir):
    allImgs = []
    shapes = []
    for folder in folderList:
        img = imageio.imread('{0}/{1}/{2}'.format(wDir, folder, pos))
        arrImg = np.array(img.astype(np.int16))
        arrImg = arrImg.sum(2)
        shapes.append(arrImg.shape)
        allImgs.append(arrImg)
    
    shapes = np.array(shapes)
    minShape = shapes.min(axis=0)

    allImgs = [img[0:minShape[0], 0:minShape[1]] for img in allImgs]
    arrImgStack = np.array(allImgs, dtype=np.uint16)
    
    print('Finished processing position #{0}'.format(pos[0:-4]))

    save2stack(arrImgStack, '{0}/RawMovieStack/{1}.tiff'.format(oDir, pos[0:-4]))
    
    return arrImgStack


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="A script to combine seperated images from a serise of snapshots taken by EVOS, and compile each well into a stack. \n\
        Runs at the parental folder, folder for each date expample: \"Scan 'LT_ibidi24' 2020-01-23 12.34.31\" \n\
        File example: A03.png (single channel only, RGB images will be merged to single channel)\n\
        The output will be several stacks + a csv for datetimes, in the format of \'2011-11-04T00:05:23\' (ISO 8601) \n\
        WARNING: The script is extreme RAM inefficient! But should be OK for movies with relative low frame rate.") 
    parser.add_argument("WorkDir", help="The directory containing all the images (only ends with .TIF)")
    parser.add_argument("-o", "--Output", help="The directory for stack output")    
    parser.add_argument("-t", "--MultiThread", type=int, default=1, help="Number of thread to use, default = 1")
    args = parser.parse_args()
    
    # Handling parameters
    wDir = args.WorkDir
    print(Back.RED + 'WARNING: The script is extreme RAM inefficient! But should be OK for movies with relative low frame rate.')
    print("Start working in " + wDir)

    if args.Output:
        oDir = args.Output
    else:
        oDir = wDir
    print("Output to " + oDir)


    mtNum = args.MultiThread

    if mtNum == 1:
        multiP = False
    elif mtNum < 1:
        print("Not valid thread number, now working in single thread mode")
        multiP = False
    else:
        multiP = True

    # Making the list of images need to be processed
    allSubFolders = [folder for folder in listdir(wDir) if folderRe.match(folder)]
    allSubFolders.sort()
    # print(allSubFolders)
    positions = [well for well in listdir('{0}/{1}'.format(wDir, allSubFolders[0])) if wellRe.match(well)]
    positions = set(positions)
    
    # Make the folder
    if not ospath.isdir(oDir+'\\{0}'.format("RawMovieStack")):
        mkdir(oDir+'\\{0}'.format("RawMovieStack"))

    # Processing the images
    if multiP:
        print("Starting {0} threads......".format(mtNum))
        mtWorker = partial(extractEachWell, wDir=wDir, folderList=allSubFolders, oDir=oDir)
        with Pool(mtNum) as p:
            allStacks = p.map(mtWorker, positions)
    else:
        print("Single thread mode")
        allStacks = []
        for pos in positions:
            allStacks.append(extractEachWell(pos, wDir, allSubFolders, oDir))

    stackShapes = np.array([stack.shape for stack in allStacks])
    minStackShape = stackShapes.min(axis=0)
>>>>>>> c8474555526ef0911ae99f25cb69e593c44d1576
