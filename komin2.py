import cv2
import numpy as np

cv2.samples.addSamplesDataSearchPath("C:/Users/ktosicosi/PycharmProjects/scientificProject/data/images")

img = cv2.imread(cv2.samples.findFile("komin3.jpg"))


def changeRes(img, per):
   scale_percent = per  # percent of original size
   width = int(img.shape[1] * scale_percent / 100)
   height = int(img.shape[0] * scale_percent / 100)
   dim = (width, height)
   resized = cv2.resize(img, dim)
   return resized


resized = changeRes(img, 120)
gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)


blurred = cv2.GaussianBlur(gray, (5, 5), 0)


edges = cv2.Canny(blurred, 120, 210, apertureSize=3)


lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=60, minLineLength=50, maxLineGap=10)


if lines is not None:
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(resized, (x1, y1), (x2, y2), (0, 255, 0), 2)


contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
chimney_found = False

for contour in contours:

    epsilon = 0.1 * cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, epsilon, True)

    if len(approx) == 4:
        x, y, w, h = cv2.boundingRect(approx)
        aspect_ratio = float(w) / h

        cv2.rectangle(resized, (x, y), (x+w, y+h), (0, 0, 255), 2)

        if aspect_ratio < 1.0 and h > 50:
            chimney_found = True


print("Chimney detected:" if chimney_found else "No chimney detected.")

cv2.imshow('Detected Lines and Rectangles', resized)
cv2.waitKey(0)
cv2.destroyAllWindows()

