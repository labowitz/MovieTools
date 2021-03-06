from scipy import ndimage
from os.path import basename
import numpy as np

import warnings


def clop(img):
    closed = ndimage.binary_closing(img)
    cloped = ndimage.binary_opening(closed)
    
    return np.array(cloped)

def clopStack(imgStack):
    cloped = [clop(img) for img in imgStack]
    
    return np.array(cloped)

def getConfl(fileDir):
    probs = np.load(fileDir)

    if not probs.dtype is np.uint8:
        warnings.warn('The loaded file ({0}) is not with dtype of \'uint8\', might cause problem in parsing'.format(fileDir))
    
    cellMask = (probs[... ,0] - probs[... ,1]) < 0

    if probs.shape[-1] > 2:
        validMask = (probs[..., 2] < 128)
        # print('here')
    else:
        validMask = np.ones(cellMask.shape)
    # return validMask
    cellMask = np.logical_and(cellMask, validMask)

    dim = cellMask.ndim
    if dim == 2:
        cellMask = clop(cellMask)
    elif dim == 3:
        cellMask = clopStack(cellMask)
    
    confl = (cellMask.sum(axis=(dim - 1, dim - 2)) + 1) / (validMask.sum(axis=(dim - 1, dim - 2)) + 1)

    return confl

def getConfl2plate(fileDir, plate, fileRe):
    confl = getConfl(fileDir)
    pos = fileRe.match(basename(fileDir)).group(1)    
    plate.asignData(pos, confl)


class plateData():
    
    letterMap = {
        'A' : 0,
        'B' : 1,
        'C' : 2,
        'D' : 3,
        'E' : 4,
        'F' : 5,
        'G' : 6,
        'H' : 7
    }
    
    def __init__(self):
        self.data = np.array([[np.nan] * 12] * 8)
    
    def asignData(self, pos, data):
        self.data[plateData.letterMap[pos[0]], int(pos[1:]) - 1] = data