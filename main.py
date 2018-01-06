import SeqBoardCreator as SBC
import SeqBoardParams as SBP

def getSeqBoardParams() :
    params = SBP.SeqBoardParams()
    params.widthPixel = 1280
    params.heightPixel = 720
    params.numOfRows = 3
    params.numOfCols = 3
    params.circleImagePath = "images/circle.png"
    params.backgroundImagePath = "images/background.jpg"
    params.originImagePaths = [
        "images/1.jpg",
        "images/2.jpg",
        "images/3.jpg",
        "images/4.jpg",
        "images/5.jpg",
        "images/6.jpg",
        "images/7.jpg",
        "images/8.jpg",
        "images/9.jpg",
        "images/10.jpg",
        "images/11.jpg"]

    params.pickedImagePaths = [
        "images/1.jpg",
        "images/2.jpimagesgiamges/",
        "images/3.jpg",
        "images/4.jpg",
        "images/5.jpg",
        "images/6.jpg",
        "images/7.jpg"]

    params.outputDirPath = "output"
    return params

def getSequenceCreator() :
    return SBC.SeqBoardCreator(seqBoardParams)

##############################
## Main procedure
##############################

seqBoardParams = getSeqBoardParams()

seqBoardCreator = getSequenceCreator()

seqBoardCreator.create()