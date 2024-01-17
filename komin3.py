import cv2
import numpy as np

def changeRes(img, per):
   scale_percent = per  # percent of original size
   width = int(img.shape[1] * scale_percent / 100)
   height = int(img.shape[0] * scale_percent / 100)
   dim = (width, height)
   resized = cv2.resize(img, dim)
   return resized

def count_vertical_lines(image, edge_threshold1, edge_threshold2, hough_threshold, min_line_length, max_line_gap):
    print("Counting...")
    image = image
    resized = changeRes(image, 30)
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

    # Edge detection
    edges = cv2.Canny(gray, edge_threshold1, edge_threshold2)

    # Hough Line Transform
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, hough_threshold, minLineLength=min_line_length, maxLineGap=max_line_gap)

    vertical_line_count = 0

    # Filter vertical lines and count them
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            if x1 == x2:  # This is a vertical line
                vertical_line_count += 1
                # Draw the vertical line on the original image for visualization
                cv2.line(resized, (x1, y1), (x2, y2), (0, 255, 0), 2)

    print("Number of vertical lines:")
    print(vertical_line_count)
    # Show the result
    cv2.imshow('Vertical Lines', resized)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


    return vertical_line_count


edge_threshold1 = 30
edge_threshold2 = 100
hough_threshold = 15  # The minimum number of intersections to detect a line
min_line_length = 30  # The minimum number of points that can form a line
max_line_gap = 20     # The maximum gap between two points to be considered in the same line

cv2.samples.addSamplesDataSearchPath("C:/Users/ktosicosi/PycharmProjects/scientificProject/data/images")
img = cv2.imread(cv2.samples.findFile("komin1.jpg"))

num_vertical_lines = count_vertical_lines(img, edge_threshold1, edge_threshold2, hough_threshold, min_line_length, max_line_gap)

