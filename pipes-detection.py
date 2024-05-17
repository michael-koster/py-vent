import cv2
import numpy as np

# Load the HVAC drawing image
image_path = "images/image-3.png"
#image_path = "images/hus_5-11.png"
image = cv2.imread(image_path)
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Canny edge detection
edges = cv2.Canny(gray_image, 50, 150, apertureSize=3)

# Detect lines using Hough Line Transform
lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100, minLineLength=50, maxLineGap=10)

# Draw the lines on the image
if lines is not None:
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(image, (x1, y1), (x2, y2), (0, 0, 205), 2)

# Show the output image
#cv2.imshow("Detected Pipes", image)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

cv2.imwrite('output-pipes.png', image)