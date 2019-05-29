import argparse
import os.path as ospath
import re
import subprocess
from multiprocessing import Pool
from os import listdir, mkdir
from functools import partial

import h5py
import numpy as np
from numba import jit
from PIL import Image

from utils.ImgUtils import loadstack, save2stack

ilastik = r'C:\Program Files\ilastik-1.3.2post1\ilastik.exe'
 
def generatStackList(wDic):
    stackRe = re.compile(r'(w\d[^ _]+)_(s\d+).tiff')
    stackPairDict = dict()

    for name in listdir(wDic):
        if stackRe.match(name):
            stackMatch = stackRe.search(name)
            YFPpath = ospath.normpath('{0}/w1YFP-YM_{1}.tiff'.format(wDic, stackMatch.group(2)))
            RFPpath = ospath.normpath('{0}/w2RFP-YM_{1}.tiff'.format(wDic, stackMatch.group(2)))
            stackPairDict[stackMatch.group(2)] = (YFPpath, RFPpath)

    return stackPairDict


def unpackStack(stackFile, output):
    arrList = loadstack(stackFile)
    filePaths = []
    for idx, arr in enumerate(arrList):
        savePath = output + '/{0}_frame{1:04}.Tiff'.format(ospath.splitext(ospath.basename(stackFile))[0], idx)
        filePaths.append(savePath)
        Image.fromarray(arr).save(savePath, compression = 'tiff_deflate')
    return filePaths


def runIlastik(ilastikProject, files, tempDir, posID):
    print('running ilastik for {0}'.format(posID))
    cmd = ' '.join([ilastik, '--headless', '--project={0}'.format(ilastikProject), ' '.join(files)])
    with open(r'{0}\ilastik_log_{1}.log'.format(tempDir, posID), 'w+') as logf:
        subprocess.run(cmd, stdout=logf, stderr=logf)


def stackProb(dic, posID, output):
    probRe = re.compile(r'(w\d[^ _]+_{0})_frame(\d+)_\w+.h5'.format(posID))
    probList = []
    for name in listdir(dic):
        if probRe.match(name):
            probList.append(name)

    probList.sort(key=(lambda name : probRe.search(name).group(2)))
    arrList = []
    for maskName in probList:
        h5file = h5py.File('{0}/{1}'.format(dic, maskName))
        probMask = np.array(h5file['exported_data'])[:, :, 0]
        arrList.append((probMask * 255).astype('uint8'))

    save2stack(arrList, '{0}/{1}_prob.tiff'.format(output, posID))

def mainPipe(posID, stackDict, ilastikProj, tempDir, oDir):
    print('Processing position {0}...'.format(posID))
    splitImgs = unpackStack(stackDict[posID][0], tempDir)
    runIlastik(ilastikProj, splitImgs, tempDir, posID)
    stackProb(tempDir, posID, oDir)




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="A script to run trained ilastik project on image stacks.\
        For perfusion movie with YFP nuclei label and cytoplasmic RFP. \
        Will get probablity labels from ilastik and thresholding for segmentaion and quantify RFP with dialtion.")    
    parser.add_argument("WorkDic", help="The directory containing all the image stacks (only ends with .tiff). Should be generated from MovieStackCreator.py")
    parser.add_argument("-p", "--Project", help="trained ilastik project")
    parser.add_argument("-o", "--Output", help="The directory for csv output")
    parser.add_argument("-t", "--MultiThread", type=int, default=1, help="Number of thread to use, default = 1, this program is highly paralled because of ilastik \
        so it's a better idea to put a quater of total thread number")
    parser.add_argument("--temp", default='./pipeline_temp', help="The directory for temp files")

    args = parser.parse_args()

    wDic = args.WorkDic
    ilastikProject = ospath.normpath(args.Project)
    print(ilastikProject)

    if args.Output:
        oDir = ospath.normpath(args.Output)
    else:
        oDir = ospath.normpath('./pipeline_probStack_output')
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
    
    tempPath = args.temp
    if not ospath.exists(tempPath):
        mkdir(tempPath)

    stackPairDict = generatStackList(wDic)
    if multiP:
        print("Starting {0} threads......".format(mtNum))
        mainPipeParal = partial(mainPipe, stackDict=stackPairDict, ilastikProj=ilastikProject, tempDir=tempPath, oDir=oDir)
        # mainPipeParal(stackPairDict['s1'][0], 's1')
        with Pool(mtNum) as p:
            p.map(mainPipeParal, [posID for posID in stackPairDict])
    else:
        for posID in stackPairDict:
            mainPipe(stackPairDict[posID][0], posID, ilastikProject, tempPath, oDir)
             

    # splitImgs = unpackStack('./TestData/w1YFP-YM_s1.tiff', tempPath)
    # runIlastik('./TestData/pixelClass.ilp', splitImgs)
    # stackProb('./pepeline_temp', 's1', oDir)
    # print(splitImgs)
