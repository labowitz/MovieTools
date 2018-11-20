import re
import argparse
import os.path as ospath
from PIL import Image
from os import listdir
from os import mkdir
from multiprocessing import Pool


def getImageInfo(x):
    timerunRe = re.compile(r'([^ _]+)_(w\d[^ _]+_s\d+)_t(\d+).TIF')
    match = timerunRe.search(x)
    return (match.group(1), match.group(2), int(match.group(3)))

def saveEachPosWave(multiParaInput):
    pos, allImages, wDic, saveDic, compressOpt, = multiParaInput
    posReg = re.compile('\w+_'+pos+'_')
    posImg = []
    for img in [imgName for imgName in allImages if posReg.match(imgName)]:
        posImg.append(img)

    posImg.sort(key=getImageInfo)
    print(pos)
    
    imageFiles = []
    for timeP in posImg:
        file = Image.open(wDic+'\\'+timeP)
        imageFiles.append(file)
    print(compressOpt)
    imageFiles[0].save(saveDic+pos+'.tiff', compression=compressOpt, save_all=True, append_images=imageFiles[1:])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="A script to combine seperated images from a timelapse movie taken by MetaMorph to tif image stacks. \
     Accepting file name example: MyExp1_w1YFP_s3_t15.TIF\
     Or in general, the regex r'([^ _]+)_(w\d[^ _]+_s\d+)_t(\d+).TIF'")
    parser.add_argument("WorkDic", help="The directory containing all the images (only ends with .TIF)")
    parser.add_argument("-t", "--MultiThread", type=int, default=1, help="Number of thread to use, default = 1")
    parser.add_argument('--compressionOFF', action='store_true', help="Turn off compression if you are more CPU bound than IO bound (faster on a laptop with SSD). \
    Of course it will increase final file sizes")
    args = parser.parse_args()
    
    wDic = args.WorkDic
    print("Start working in " +wDic)

    compressOpt = 'tiff_deflate'
    if args.compressionOFF:
        print('none')
        compressOpt = 'None'

    mtNum = args.MultiThread

    if mtNum == 1:
        multiP = False
    elif mtNum < 1:
        print("Not valid thread number, now working in single thread mode")
        multiP = False
    else:
        multiP = True

    allImages = [name for name in listdir(wDic) if name.endswith('.TIF')]

    positions = set()
    for imageName in allImages:
        pos = getImageInfo(imageName)[1]
        positions.add(pos)
    
    if not ospath.isdir(wDic+'\\EachPosWave'):
        mkdir(wDic+'\\EachPosWave')

    multiPara = list(zip(list(positions), [allImages]*len(positions), [wDic]*len(positions), [wDic+'\\EachPosWave\\']*len(positions), [compressOpt]*len(positions)))

    if multiP:
        print("Starting {0} threads".format(mtNum))
        with Pool(mtNum) as p:
            p.map(saveEachPosWave, multiPara)
    else:
        print("Single thread mode")
        for para in multiPara:
            saveEachPosWave(para)