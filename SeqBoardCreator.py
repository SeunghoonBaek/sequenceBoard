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

        cv2.putText(circleImage,
                    "{}".format(number),
                    (int(circleWidthPixel * 0.5), int(circleHeightPixel * 0.5)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.0,
                    (255, 255, 255, 255),
                    4)
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

        ## baseImage[offsetY:offsetY + overlayImage.shape[0], offsetX:offsetX + overlayImage.shape[1]] = overlayImage
        ## baseImage = self.overlay_transparent(baseImage, overlayImage, offsetX, offsetY)

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

                    ## debug writing
                    # print ("[DEBUG-WRITING] " + str(self.params.outputDirPath) + "/" + str(indexOfPath) + ".jpg")
                    # cv2.imwrite(self.params.outputDirPath + "/" + str(indexOfPath) + ".jpg", baseImage)

            overlayImages.append(baseImage.copy())
        return overlayImages

    def OverlayImage(self, src, overlay, posx, posy):
        S = (0.5, 0.5, 0.5, 0.5)  # Define blending coefficients S and D
        D = (0.5, 0.5, 0.5, 0.5)

        for x in range(overlay.shape[1]):

            if x + posx < src.shape[1]:

                for y in range(overlay.shape[0]):

                    if y + posy < src.shape[1]:

                        source = cv2.Get2D(src, y + posy, x + posx)
                        over = cv2.Get2D(overlay, y, x)
                        merger = [0, 0, 0, 0]

                        for i in range(3):
                            if over[i] == 0:
                                merger[i] = source[i]
                            else:
                                merger[i] = (S[i] * source[i] + D[i] * over[i])

                        merged = tuple(merger)

                        cv2.Set2D(src, y + posy, x + posx, merged)

    def overlay_transparent(self, background_img, img_to_overlay_t, x, y, overlay_size=None):
        """
        @brief      Overlays a transparant PNG onto another image using CV2

        @param      background_img    The background image
        @param      img_to_overlay_t  The transparent image to overlay (has alpha channel)
        @param      x                 x location to place the top-left corner of our overlay
        @param      y                 y location to place the top-left corner of our overlay
        @param      overlay_size      The size to scale our overlay to (tuple), no scaling if None

        @return     Background image with overlay on top
        """

        bg_img = background_img.copy()

        if overlay_size is not None:
            img_to_overlay_t = cv2.resize(img_to_overlay_t.copy(), overlay_size)

        # Extract the alpha mask of the RGBA image, convert to RGB
        b, g, r, a = cv2.split(img_to_overlay_t)
        overlay_color = cv2.merge((b, g, r, a))

        # Apply some simple filtering to remove edge noise
        mask = cv2.medianBlur(a, 5)

        h, w, _ = overlay_color.shape
        roi = bg_img[y:y + h, x:x + w]

        # Black-out the area behind the logo in our original ROI
        img1_bg = cv2.bitwise_and(roi.copy(), roi.copy(), mask=cv2.bitwise_not(mask))

        # Mask out the logo from the logo image.
        img2_fg = cv2.bitwise_and(overlay_color, overlay_color, mask=mask)

        # Update the original image with our new ROI
        bg_img[y:y + h, x:x + w] = cv2.add(img1_bg, img2_fg)

        return bg_img