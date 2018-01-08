import cv2

class SeqBoardCreator:
    def __init__(self, params):
        self.params                 = params
        defaultPaddingPixel         = int(min(self.params.widthPixel / self.params.numOfCols, self.params.heightPixel / self.params.numOfRows) * 0.05)
        self.paddingLeftPixel       = defaultPaddingPixel
        self.paddingRightPixel      = defaultPaddingPixel
        self.paddingTopPixel        = defaultPaddingPixel
        self.paddingBottomPixel     = defaultPaddingPixel
        self.circleWidthPixel       = int(min(self.params.widthPixel / self.params.numOfCols, self.params.heightPixel / self.params.numOfRows) * 0.25)
        self.circleHeightPixel      = self.circleWidthPixel

    def create(self):
        print("create")
        self._cretaeSequenceBoardImages()

    def _cretaeSequenceBoardImages(self):
        print("_cretaeSequenceBoardImages")
        pickedOutputImages = self._getOverlayImages(self.params.pickedImagePaths)

        notPickedOutputImagePaths = list(self.params.originImagePaths)
        for pickedImagePath in self.params.pickedImagePaths:
            notPickedOutputImagePaths.remove(pickedImagePath)

        notPickedOutputImages = self._getOverlayImages(notPickedOutputImagePaths)

        self._writeImageFiles(pickedOutputImages, 1)
        self._writeImageFiles(notPickedOutputImages, 2)

    def _createNumImageWithinCircle(self, circleImagePath, circleWidthPixel, circleHeightPixel, number):
        print("_createNumImageWithinCircle")
        circleImage = self._createResizedImage(circleImagePath, circleWidthPixel, circleHeightPixel)

        text = "{}".format(number)
        fontFace = cv2.FONT_HERSHEY_SIMPLEX
        fontScale = circleImage.shape[0] / 60.0     ## the scalar 60.0 is experimental value.
        thickness = int(circleImage.shape[0] / 30)  ## the scalar 30 is experimental value.

        ## refer to : https://gist.github.com/xcsrz/8938a5d4a47976c745407fe2788c813a
        (textSize, baseline) = cv2.getTextSize(text, fontFace, fontScale, thickness)
        textX = (circleImage.shape[1] - textSize[0]) / 2
        textY = (circleImage.shape[0] - textSize[1]) / 2 + (baseline * 2)

        cv2.putText(circleImage, text, (textX, textY), fontFace, fontScale, (255, 255, 255, 255), thickness)
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
        alpha_overlay = overlayImage[:, :, 3] / 255.0
        alpha_base = 1.0 - alpha_overlay

        y1, y2 = offsetY, offsetY + overlayImage.shape[0]
        x1, x2 = offsetX, offsetX + overlayImage.shape[1]

        for c in range(0, 3):
            baseImage[y1:y2, x1:x2, c] = (alpha_overlay * overlayImage[:, :, c] + alpha_base * baseImage[y1:y2, x1:x2, c])

    def _writeImageFiles(self, outputImages, temp):
        print("_writeImageFiles")
        for i in xrange(len(outputImages)) :
            filename = self._getOutputFileName(self.params.outputDirPath, temp)
            cv2.imwrite(filename, outputImages[i])

    def _getOutputFileName(self, outputDir, i):
        print("_getOutputFileName")
        return outputDir + "/" + str(i) + ".jpg"

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
                    if indexOfPath >= len(fillImagePaths):
                        break

                    offsetX = int((self.params.widthPixel / self.params.numOfCols) * col)
                    offsetY = int((self.params.heightPixel / self.params.numOfRows) * row)
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
                                       offsetX + (self.params.widthPixel / self.params.numOfCols) - self.circleWidthPixel,
                                       offsetY + (self.params.heightPixel / self.params.numOfRows) - self.circleHeightPixel)

            overlayImages.append(baseImage.copy())
        return overlayImages