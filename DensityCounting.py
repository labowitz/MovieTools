import numpy as np
import pickle
import argparse
import os.path as ospath

from utils.ImgUtils import loadstack
from multiprocessing import Pool
from os import listdir, mkdir


def sumStackIntensity(stackDir):
    stack = loadstack(stackDir)
    return [np.sum(img) for img in stack]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A script to process images stacks and output measurements into a pickled structure.")    
    parser.add_argument('WorkDir', help="The directory containing all the image stacks (only ends with .tiff). Should be generated from Pipeline_ProbStack.py")
    parser.add_argument('-o', "--Output",  default='./', help="The directory for pickled output")
    parser.add_argument('-t', "--MultiThread", type=int, default=1, help="Number of thread to use, default = 1")
    parser.add_argument('--keyword', type=str, help="Keyword used to filter the file names, only filenames that contains keywords will be processed")

    args = parser.parse_args()

    wDir = args.WorkDir

    oDir = ospath.normpath(args.Output)
    if not ospath.exists(oDir):
        mkdir(oDir)

    print("Output to " + oDir)

    mtNum = args.MultiThread
    if mtNum == 1:
        multiP = False
    elif mtNum < 1:
        print("Not valid thread number, now working in single thread mode")
        multiP = False
    else:
        multiP = True

    keyW = args.keyword
    if not keyW:
        keyW = ''

    # Making the list of stacks need to be processed
    stackNames = [name for name in listdir(wDir) if name.endswith('.tiff') and (keyW in name)]
    stackDirs = ['{0}/{1}'.format(wDir, name) for name in stackNames]

    # Processing the images
    if multiP:
        print("Starting {0} threads......".format(mtNum))
        with Pool(mtNum) as p:
            intensitySums = p.map(sumStackIntensity, stackDirs)
        resultDic = dict(zip(stackNames, intensitySums))
    else:
        print("Single thread mode")
        resultDic = {}
        for idx, stackDir in enumerate(stackDirs):
            resultDic[stackNames[idx]] = sumStackIntensity(stackDir)

    saveFilePath = '{0}/IntensitySum.p'.format(oDir)
    print('Finished processing, saving at {0}'.format(saveFilePath))
    with open(saveFilePath, 'wb') as f:
        pickle.dump(resultDic, f)
    print('Scripts finished successfully')


