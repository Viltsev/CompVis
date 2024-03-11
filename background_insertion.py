import os
import random
import cv2

def background_insertion(directory='imagesWithoutBackground/', background="background.jpg", imageCount=5):
    newDirectory = 'imagesWithBackground/'
    os.makedirs(newDirectory, exist_ok=True)

    files = os.listdir(directory)
    randomImages = random.sample(files, imageCount)

    for image in randomImages:
        imagePath = os.path.join(directory, image)

        # Download foreground
        foreground = cv2.imread(imagePath)
        foregroundHeight, foregroundWidth = foreground.shape[:2]

        # Download background
        imgBackground = cv2.imread(background)
        resizedBackground = cv2.resize(imgBackground, (foregroundWidth, foregroundHeight))

        # Make pyramid of image for foreground and background
        pyramidForeground = tuple(cv2.pyrDown(foreground) for _ in range(3))
        pyramidBackground = tuple(cv2.pyrDown(resizedBackground) for _ in range(3))
        result = None

        # ROI approximation
        for i in range(3):
            backgroundHeight, backgroundWidth = pyramidBackground[i].shape[:2]
            roi = cv2.resize(pyramidForeground[i], (backgroundWidth, backgroundHeight))

            # Foreground mask
            foregroundGray = cv2.cvtColor(pyramidForeground[i], cv2.COLOR_BGR2GRAY)
            _, mask = cv2.threshold(foregroundGray, 1, 255, cv2.THRESH_BINARY)

            # Foreground to background by pyramid method
            foregroundMasked = cv2.bitwise_and(roi, roi, mask=mask)
            backgroundMasked = cv2.bitwise_and(pyramidBackground[i], pyramidBackground[i], mask=cv2.bitwise_not(mask))
            blended = cv2.addWeighted(foregroundMasked, 1, backgroundMasked, 1, 0)

            # Increase result image on the next level of the pyramid
            if i < 2:
                blended = cv2.resize(blended, (pyramidForeground[i + 1].shape[1], pyramidForeground[i + 1].shape[0]))
                blended = cv2.pyrUp(blended)

            result = blended

        # Save result
        new_image_path = os.path.join(newDirectory, image)
        cv2.imwrite(new_image_path, result)

background_insertion()