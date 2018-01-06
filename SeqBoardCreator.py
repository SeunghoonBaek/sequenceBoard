import cv2

class SeqBoardCreator:
    def __init__(self, params):
        self.params                 = params
        defaultPaddingPixel         = int((self.params.widthPixel / self.params.numOfCols) * 0.05)
        self.paddingLeftPixel       = defaultPaddingPixel
        self.paddingRightPixel      = defaultPaddingPixel
        self.paddingTopPixel        = defaultPaddingPixel
        self.paddingBottomPixel     = defaultPaddingPixel
        self.circleWidthPixel       = int((self.params.widthPixel / self.params.numOfCols) * 0.25)
        self.circleHeightPixel      = int((self.params.heightPixel / self.params.numOfRows) * 0.25)

    def create(self):
        print("create")
        self._cretaeSequenceBoardImages()

    def _cretaeSequenceBoardImages(self):
        print("_cretaeSequenceBoardImages")
        pickedOutputImages = self._getOverlayImages(self.params.pickedImagePaths)
        notPickedOutputImages = self._getOverlayImages(self.params.originImagePaths.remove(self.params.pickedImagePaths))

        self._writeImageFiles(pickedOutputImages)
        self._writeImageFiles(notPickedOutputImages)

    def _createNumImageWithinCircle(self, circleImagePath, circleWidthPixel, circleHeightPixel, number):
        print("_createNumImageWithinCircle")
        circleImage = self._createResizedImage(circleImagePath, circleWidthPixel, circleHeightPixel)
        cv2.putText(circleImage,
                    "{}".format(number),
                    (circleWidthPixel * 0.5, circleHeightPixel * 0.5),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.0,
                    (255, 255, 255), 3)
        return circleImage

    def _createBackgroundImage(self):
        print("_createBackgroundImage")
        return self._createResizedImage(self.params.backgroundImagePath, self.params.widthPixel, self.params.heightPixel)

    def _createResizedImage(self, targetImagePath, targetWidthPixel, targetHeightPixel):
        print("_createResizedImage")
        img = cv2.imread(targetImagePath, cv2.IMREAD_UNCHANGED)

        if img.shape[2] != 4 : ## get Image channel
            img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)

        return cv2.resize(img, (targetWidthPixel, targetHeightPixel))

    def _overlayImage(self, baseImage, overlayImage, offsetX, offsetY):
        print("_overlayImage" + str(offsetX) + ", " + str(offsetY))
        baseImage[offsetY:offsetY + overlayImage.shape[0], offsetX:offsetX + overlayImage.shape[1]] = overlayImage

    def _writeImageFiles(self, outputImages):
        print("_writeImageFiles")
        for i in xrange(outputImages) :
            filename = self._getOutputFileName(self.params.outputDirPath, i)
            cv2.imwrite(filename, outputImages[i])

    def _getOutputFileName(self, outputDir, i):
        print("_getOutputFileName")
        return outputDir + "/" + str(i)

    def _getIndexOfImagePath(self, image):
        print("_getIndexOfImage")
        return self.params.originImagePaths.index(image)

    def _getOverlayImages(self, fillImagePaths):
        print("_getOverlayImages")
        overlayImages = []
        thumbnailWidth = int((self.params.widthPixel / self.params.numOfCols) - (self.paddingLeftPixel + self.paddingRightPixel))
        thumbnailHeight = int((self.params.heightPixel / self.params.numOfRows) - (self.paddingTopPixel + self.paddingBottomPixel))

        indexOfPath = 0
        while indexOfPath < len(fillImagePaths) :

            baseImage = self._createBackgroundImage()
            for row in xrange(self.params.numOfRows):
                for col in xrange(self.params.numOfCols):
                    offsetX = int((self.params.heightPixel / self.params.numOfCols) * col)
                    offsetY = int((self.params.widthPixel / self.params.numOfRows) * row)
                    notPickedImagePath = fillImagePaths[indexOfPath]
                    indexOfPath += 1

                    resizedImage = self._createResizedImage(notPickedImagePath, thumbnailWidth, thumbnailHeight)
                    self._overlayImage(baseImage,
                                       resizedImage,
                                       offsetX + self.paddingLeftPixel,
                                       offsetY + self.paddingTopPixel)

                    circleNum = self._getIndexOfImagePath(notPickedImagePath)
                    circleImage = self._createNumImageWithinCircle(self.params.circleImagePath,
                                                                   self.circleWidthPixel,
                                                                   self.circleHeightPixel,
                                                                   circleNum)
                    self._overlayImage(baseImage,
                                       circleImage,
                                       offsetX + (self.params.widthPixel / self.params.numOfCol) - self.circleWidthPixel,
                                       offsetY + (self.params.heightPixel / self.params.numOfRows) - self.circleHeightPixel)
            overlayImages.append(baseImage)
        return overlayImages