<<<<<<< HEAD
from PIL import Image
from os.path import normpath
import numpy as np

import imageio

def save2stack(arrList, saveDir, verb=True):
    saveDir = normpath(saveDir)
    if verb:
        print('Saving image stack at {0}'.format(saveDir))
    imgList = []
    for arr in arrList:
        imgList.append(Image.fromarray(arr))
    imgList[0].save(saveDir, save_all=True, append_images=imgList[1:], compression = 'tiff_deflate')

def loadstack(stackFile, verb=True):
    stackFile = normpath(stackFile)
    if verb:
        print('Loading image stack at {0}'.format(stackFile))
    stack = Image.open(stackFile)

    arrList = []
    for idx in range(stack.n_frames):
        stack.seek(idx)
        arrList.append(np.array(stack))
    
    return arrList

def binImages(imgDir, binSize, outDir, prefix=''):
    img = imageio.imread(imgDir)
    arrImg = np.array(img)
    imgShape = (np.array(arrImg.shape) / binSize).astype(np.int)
    arrImg = arrImg.sum(2)[0: binSize*imgShape[0], 0:binSize*imgShape[1]]
    binedImg = arrImg.reshape(imgShape[0], binSize, imgShape[1], binSize).sum(3).sum(1)

    imageio.imwrite('{0}/{1}{2}_bin{3}.tiff'.format(outDir, prefix, imgDir[-7:-4], binSize), binedImg.astype(np.uint16))
=======
from PIL import Image
from os.path import normpath
import numpy as np

import imageio

def save2stack(arrList, saveDir, verb=True):
    saveDir = normpath(saveDir)
    if verb:
        print('Saving image stack at {0}'.format(saveDir))
    imgList = []
    for arr in arrList:
        imgList.append(Image.fromarray(arr))
    imgList[0].save(saveDir, save_all=True, append_images=imgList[1:], compression = 'tiff_deflate')

def loadstack(stackFile, verb=True):
    stackFile = normpath(stackFile)
    if verb:
        print('Loading image stack at {0}'.format(stackFile))
    stack = Image.open(stackFile)

    arrList = []
    for idx in range(stack.n_frames):
        stack.seek(idx)
        arrList.append(np.array(stack))
    
    return arrList

def binImages(imgDir, binSize, outDir, prefix=''):
    img = imageio.imread(imgDir)
    arrImg = np.array(img)
    imgShape = (np.array(arrImg.shape) / binSize).astype(np.int)
    arrImg = arrImg.sum(2)[0: binSize*imgShape[0], 0:binSize*imgShape[1]]
    binedImg = arrImg.reshape(imgShape[0], binSize, imgShape[1], binSize).sum(3).sum(1)

    imageio.imwrite('{0}/{1}{2}_bin{3}.tiff'.format(outDir, prefix, imgDir[-7:-4], binSize), binedImg.astype(np.uint16))
>>>>>>> c8474555526ef0911ae99f25cb69e593c44d1576
