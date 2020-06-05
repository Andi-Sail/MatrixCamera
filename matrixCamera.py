import cv2 as cv
import numpy as np
import _thread
import random
import string


cap = cv.VideoCapture(0)
width = int(cap.get(3))
height = int(cap.get(4))


Symbols = string.ascii_letters + string.digits + string.punctuation*10 + 100*' '
fontScale = 0.25
fontThickness = 1
ColPadding = 10
maxSymbolWidth = 0
maxLineLen = 1000
maxNbrLines = 300

matrixLines = list()

def createNewMatrixLine():
    global matrixLines, Symbols, maxLineLen
    newLine = (random.choices(Symbols, k=maxLineLen))
    if (len(matrixLines) >= 1):
        lastLine = matrixLines[-1]
        spaceIndex=np.where(np.array(list(lastLine))==' ')[0]
        for i in spaceIndex:
            if (random.random() > 0.5):
                newLine[i] = ' '

    newLine = ''.join(newLine)
    matrixLines.append(newLine)


for i in range(maxNbrLines):
    createNewMatrixLine()


while (True):
    ret, frame = cap.read()
    frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    cv.imshow('frame',frame)

    th, frameBw = cv.threshold(frame, 0, 200, cv.THRESH_OTSU)
    cv.imshow('frameBw',frameBw)

    frameEdges = cv.Canny(frameBw, th, 2*th)
    cv.imshow('frameEdges',frameEdges)

    frameMatrix = np.zeros((height,width,3), np.uint8)
    

    widthCovered = 0
    heightCovered = 0

    lineIndex = 0
    while heightCovered < height:
        colIndex = 0
        while widthCovered < width:
            matrixChar = matrixLines[maxNbrLines -1 - lineIndex][colIndex]
            ((textW, textH), baseline) = cv.getTextSize(matrixChar, cv.FONT_HERSHEY_SIMPLEX, fontScale, fontThickness)
            maxSymbolWidth = textW if (textW > maxSymbolWidth) else maxSymbolWidth

            if (random.random() < 0.8):
                if (frameBw[heightCovered:heightCovered+textH,widthCovered:widthCovered+maxSymbolWidth].mean() > 0.7):
                    cv.putText(frameMatrix, matrixChar, (widthCovered+int((maxSymbolWidth-textW)/2),heightCovered + textH), cv.FONT_HERSHEY_SIMPLEX, fontScale, (0, 255, 0), fontThickness)
                if (frameEdges[heightCovered:heightCovered+textH,widthCovered:widthCovered+textW].mean() > 0.3):
                    cv.putText(frameMatrix, matrixChar, (widthCovered,heightCovered + textH), cv.FONT_HERSHEY_SIMPLEX, fontScale, (180, 255, 180), fontThickness)
            widthCovered += maxSymbolWidth + ColPadding
            colIndex += 1

        lineIndex += 1
        heightCovered += textH
        widthCovered = 0
    
    
    matrixLines.pop(0)
    createNewMatrixLine()
    cv.imshow('frameMatrix',frameMatrix)


    if cv.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv.destroyAllWindows()
