import cv2
import numpy as np

# Load the HVAC drawing image
image_path = "images/image-1.png"
image = cv2.imread(image_path)
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Load the template images
inlet_template = cv2.imread("templates/inlet-1.png", 0)
outlet_template = cv2.imread("templates/outlet-1.png", 0)
muffler_template = cv2.imread("templates/muffler.png", 0)

def match_template(image, template, threshold=0.3):
    result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(result >= threshold)
    return loc

# Match templates
inlet_locations = match_template(gray_image, inlet_template)
outlet_locations = match_template(gray_image, outlet_template)
muffler_locations = match_template(gray_image, muffler_template, threshold=0.5)

# Draw rectangles for inlets
for pt in zip(*inlet_locations[::-1]):
    cv2.rectangle(image, pt, (pt[0] + inlet_template.shape[1], pt[1] + inlet_template.shape[0]), (0, 255, 0), 2)
    cv2.putText(image, 'Inlet', (pt[0], pt[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# Draw rectangles for outlets
for pt in zip(*outlet_locations[::-1]):
    cv2.rectangle(image, pt, (pt[0] + outlet_template.shape[1], pt[1] + outlet_template.shape[0]), (0, 0, 255), 2)
    cv2.putText(image, 'Outlet', (pt[0], pt[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

# Draw rectangles for mufflers
for pt in zip(*muffler_locations[::-1]):
    cv2.rectangle(image, pt, (pt[0] + muffler_template.shape[1], pt[1] + muffler_template.shape[0]), (255, 0, 0), 2)
    cv2.putText(image, 'Muffler', (pt[0], pt[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)


# Show the output image
cv2.imshow("Detected Inlets and Outlets", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
