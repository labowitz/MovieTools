from scipy import ndimage
import numpy as np


def clop(imageStack):
    closed = [ndimage.binary_closing(img) for img in imageStack]
    cloped = [ndimage.binary_opening(img) for img in closed]
    
    return np.array(cloped)


def getConfl(fileDir, plate, fileRe):
        probs = np.load(fileDir).astype(np.int16)
        cellMask = (probs[:,:,0] - probs[:,:,1]) < 0
        cellMask = clop(cellMask)

        confl = (cellMask.sum() + 1) / (probs.shape[0] * probs.shape[1])
        
        pos = fileRe.match(fileDir).group(1)
        
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