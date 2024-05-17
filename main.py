import cv2
import numpy as np

# Load the image
image_path = "./images/image-2.png"
image = cv2.imread(image_path)
output_image = image.copy()

# Convert to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply binary threshold
_, thresholded_image = cv2.threshold(gray_image, 128, 255, cv2.THRESH_BINARY_INV)

# Detect circles using HoughCircles
circles = cv2.HoughCircles(thresholded_image, cv2.HOUGH_GRADIENT, dp=1.2, minDist=20, param1=50, param2=30, minRadius=10, maxRadius=30)

if circles is not None:
    circles = np.round(circles[0, :]).astype("int")
    for (x, y, r) in circles:
        # Draw the circle in the output image
        cv2.circle(output_image, (x, y), r, (0, 255, 0), 4)
        # Draw a rectangle corresponding to the cross inside
        cv2.rectangle(output_image, (x - r, y - r), (x + r, y + r), (0, 128, 255), 2)

        # Extract the region of interest
        roi = thresholded_image[y - r:y + r, x - r:x + r]

        # Apply edge detection
        edges = cv2.Canny(roi, 50, 150, apertureSize=3)

        # Detect lines using HoughLinesP
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=30, minLineLength=10, maxLineGap=5)
        if lines is not None:
            line_count = 0
            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(output_image, (x1 + x - r, y1 + y - r), (x2 + x - r, y2 + y - r), (0, 0, 255), 2)
                line_count += 1

            # If two lines are detected, it is likely an inlet symbol
            if line_count >= 2:
                cv2.putText(output_image, 'Inlet', (x - r, y - r - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# Show the output image
cv2.imshow("Detected Inlets", output_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
