import argparse
import os.path as ospath
import re
import subprocess
import h5py
from multiprocessing import Pool
from os import listdir, mkdir

import numpy as np
from numba import jit
from PIL import Image

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
    stack = Image.open(stackFile)
    filePaths = []
    for idx in range(stack.n_frames):
        stack.seek(idx)
        savePath = output + '/{0}_frame{1:04}.Tiff'.format(ospath.splitext(ospath.basename(stackFile))[0], idx)
        filePaths.append(savePath)
        stack.save(savePath)
    return filePaths


def runIlastik(ilastikProject, files):
    cmd = ' '.join([ilastik, '--headless', '--project={0}'.format(ilastikProject), ' '.join(files)])
    subprocess.run(cmd)


def stackProb(dic):
    probRe = re.compile(r'(w\d[^ _]+_s\d+)_frame(\d+)_\w+.h5')
    posDict = dict()
    for name in listdir(dic):
        if probRe.match(name):
            match = probRe.search(name)

            if not match.group(1) in posDict:
                posDict[match.group(1)] = []
            
            posDict[match.group(1)].append(name)

    for pos in posDict:
        posDict[pos].sort(key=(lambda name : probRe.search(name).group(2)))
        imgList = []
        for maskName in posDict[pos]:
            h5file = h5py.File('{0}/{1}'.format(dic, maskName))
            probMask = np.array(h5file['exported_data'])[:, :, 0]
            probMask = (probMask * 255).astype('uint16')

            imgList.append(Image.fromarray(probMask))
        imgList[0].save('{0}/{1}_prob.tiff'.format(dic, pos), save_all=True, append_images=imgList[1:])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="A script to run trained ilastik project on image stacks.\
        For perfusion movie with YFP nuclei label and cytoplasmic RFP. \
        Will get probablity labels from ilastik and thresholding for segmentaion and quantify RFP with dialtion.")    
    parser.add_argument("WorkDic", help="The directory containing all the image stacks (only ends with .tiff). Should be generated from MovieStackCreator.py")
    parser.add_argument("-p", "--Project", help="trained ilastik project")
    parser.add_argument("-o", "--Output", help="The directory for csv output")
    parser.add_argument("-t", "--MultiThread", type=int, default=1, help="Number of thread to use, default = 1")
    parser.add_argument("--temp", default='./pepeline1_temp', help="The directory for temp files")

    args = parser.parse_args()

    wDic = args.WorkDic
    ilastikProject = args.Project

    if args.Output:
        oDic = args.Output
    else:
        oDic = wDic + '/pepline1Output'
    print("Output to " + oDic)

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


    # splitImgs = unpackStack('./TestData/w1YFP-YM_s1.tiff', tempPath)
    # runIlastik('./TestData/pixelClass.ilp', splitImgs)
    stackProb('./pepeline1_temp')
    # print(splitImgs)
