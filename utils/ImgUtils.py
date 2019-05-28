from PIL import Image
from os.path import normpath
import numpy as np

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
