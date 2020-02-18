import re
import argparse
import os.path as ospath
import numpy as np
from PIL import Image
from os import listdir
from os import mkdir
from multiprocessing import Pool
from numba import jit



def getImageInfo(x):
    timerunRe = re.compile(r'([^ _]+)_(w\d[^ _]+_s\d+)_t(\d+).TIF')
    match = timerunRe.search(x)
    return (match.group(1), match.group(2), int(match.group(3)))

@jit
def normalizeImg(frame, maxI, perc):
    mini, maxi = np.percentile(frame, (perc, 100-perc))

    normFrame = (frame - mini) * maxI / (maxi - mini)
    normFrame[normFrame < 0] = 0
    normFrame[normFrame > maxI] = maxI

    return normFrame

def normalizeStack(imgStack):
    stackArr = np.stack([np.array(im) for im in imgStack])

    imgStack = []
    for frame in stackArr:
        normFrame = normalizeImg(frame, 65535, 1)
        imgStack.append(Image.fromarray(normFrame.astype(np.uint16)))
        # print(np.max(normFrame), np.min(normFrame))
    return imgStack

def saveEachPosWave(multiParaInput):
    pos, allImages, wDic, saveDic, compressOpt, normalize= multiParaInput
    posReg = re.compile(r'\w+_'+pos+'_')
    posImg = []
    for img in [imgName for imgName in allImages if posReg.match(imgName)]:
        posImg.append(img)

    posImg.sort(key=getImageInfo)
    print('Working on: Pos#' + pos)
    
    imageFiles = []
    for timeP in posImg:
        file = Image.open(wDic+'\\'+timeP)
        imageFiles.append(file)

    if normalize:
        imageFiles = normalizeStack(imageFiles)

    imageFiles[0].save(saveDic+pos+'.tiff', compression=compressOpt, save_all=True, append_images=imageFiles[1:])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="A script to combine seperated images from a timelapse movie taken by MetaMorph to tif image stacks. \
     Accepting file name example: MyExp1_w1YFP_s3_t15.TIF\
     Or in general, the regex r'([^ _]+)_(w\d[^ _]+_s\d+)_t(\d+).TIF'")
    parser.add_argument("WorkDic", help="The directory containing all the images (only ends with .TIF)")
    parser.add_argument("-o", "--Output", help="The directory for stack output")    
    parser.add_argument("-t", "--MultiThread", type=int, default=1, help="Number of thread to use, default = 1")
    parser.add_argument('--compressionOFF', action='store_true', help="Turn off compression if you are more CPU bound than IO bound (faster on a laptop with SSD). \
    Of course it will increase final file sizes")
    parser.add_argument('--normalize', action='store_true', help='Normalize across a each image using 1-99 percentile to 0~65535(16bit)')
    args = parser.parse_args()
    
    # Handling parameters
    wDic = args.WorkDic
    print("Start working in " + wDic)

    if args.Output:
        oDic = args.Output
    else:
        oDic = wDic
    print("Output to " + oDic)

    compressOpt = 'tiff_deflate'
    if args.compressionOFF:
        print('No copression will be applied')
        compressOpt = 'None'

    mtNum = args.MultiThread

    if mtNum == 1:
        multiP = False
    elif mtNum < 1:
        print("Not valid thread number, now working in single thread mode")
        multiP = False
    else:
        multiP = True

    normOpt = args.normalize

    # Making the list of images need to be processed
    allImages = [name for name in listdir(wDic) if name.endswith('.TIF')]

    positions = set()
    for imageName in allImages:
        pos = getImageInfo(imageName)[1]
        positions.add(pos)
    
    # Make the folder
    folderName = "NormedMovieStack" if normOpt else "RawMovieStack"
    if not ospath.isdir(oDic+'\\{0}'.format(folderName)):
        mkdir(oDic+'\\{0}'.format(folderName))

    multiPara = list(zip(list(positions), [allImages]*len(positions), [wDic]*len(positions), [oDic+'\\{0}\\'.format(folderName)]*len(positions), [compressOpt]*len(positions), [normOpt]*len(positions)))

    # Processing the images
    if multiP:
        print("Starting {0} threads......".format(mtNum))
        with Pool(mtNum) as p:
            p.map(saveEachPosWave, multiPara)
    else:
        print("Single thread mode")
        for para in multiPara:
            saveEachPosWave(para)