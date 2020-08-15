import re
import argparse
import os.path as ospath
import numpy as np
import imageio
from os import listdir
from os import mkdir
from multiprocessing import Pool

from functools import partial

def getImageInfo(x):
    timerunRe = re.compile(r'([^ _]+)_(w\d[^ _]+_s\d+)_t(\d+).TIF')
    match = timerunRe.search(x)
    return (match.group(1), match.group(2), int(match.group(3)))


stageReg = re.compile(r'(w\d[^ _]+_s)(\d+)')

def saveEachPosWave(pos, allImages, wDir, saveDir):
    posReg = re.compile(r'\w+_'+pos+'_')
    posImg = []
    for img in [imgName for imgName in allImages if posReg.match(imgName)]:
        posImg.append(img)

    posImg.sort(key=getImageInfo)
    print('Working on: Pos#' + pos)
    
    imageFiles = []
    for timeP in posImg:
        file = imageio.imread(wDir+'/'+timeP)
        imageFiles.append(file)

    stageMatch = stageReg.search(pos)
    saveLoc = '{0}/{1}{2:03d}.tiff'.format(saveDir, stageMatch.group(1), int(stageMatch.group(2)))
    imageio.mimsave(saveLoc, imageFiles)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="A script to combine seperated images from a timelapse movie taken by MetaMorph to tif image stacks. \
     Accepting file name example: MyExp1_w1YFP_s3_t15.TIF\
     Or in general, the regex r'([^ _]+)_(w\d[^ _]+_s\d+)_t(\d+).TIF'")
    parser.add_argument("WorkDir", help="The directory containing all the images (only ends with .TIF)")
    parser.add_argument("-o", "--Output", help="The directory for stack output")    
    parser.add_argument("-t", "--MultiThread", type=int, default=1, help="Number of thread to use, default = 1")

    args = parser.parse_args()
    
    # Handling parameters
    wDir = args.WorkDir
    print("Start working in " + wDir)

    if args.Output:
        oDir = args.Output
    else:
        oDir= wDir
    print("Output to " + oDir)

    mtNum = args.MultiThread

    if mtNum == 1:
        multiP = False
    elif mtNum < 1:
        print("Not valid thread number, now working in single thread mode")
        multiP = False
    else:
        multiP = True

    # normOpt = args.normalize

    # Making the list of images need to be processed
    allImages = [name for name in listdir(wDir) if name.endswith('.TIF')]

    positions = set()
    for imageName in allImages:
        pos = getImageInfo(imageName)[1]
        positions.add(pos)
    
    # Make the folder
    folderName = "RawMovieStack"
    if not ospath.isdir(oDir+'/{0}'.format(folderName)):
        mkdir(oDir+'/{0}'.format(folderName))

    partialSaveFunc = partial(saveEachPosWave, allImages=allImages, wDir=wDir, saveDir=oDir+'/{0}'.format(folderName))

    # Processing the images
    if multiP:
        print("Starting {0} threads......".format(mtNum))
        with Pool(mtNum) as p:
            p.map(partialSaveFunc, positions)
    else:
        print("Single thread mode")
        for pos in positions:
            partialSaveFunc(pos)