import cv2
import numpy as np
import glob

# Load the HVAC drawing image
image_path = "images/image-2.png"
image = cv2.imread(image_path)
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Load all template images for inlets and outlets
inlet_templates = [cv2.imread(file, 0) for file in glob.glob("templates/inlet/*.png")]
outlet_templates = [cv2.imread(file, 0) for file in glob.glob("templates/outlet/*.png")]
muffler_templates = [cv2.imread(file, 0) for file in glob.glob("templates/muffler/*.png")]

def rotate_image(image, angle):
    (h, w) = image.shape[:2]
    center = (w / 2, h / 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h))
    return rotated

def match_template_with_rotation(image, templates, threshold=0.8):
    locations = []
    for template in templates:
        for angle in range(0, 360, 30):  # Rotate templates every 30 degrees
            rotated_template = rotate_image(template, angle)
            result = cv2.matchTemplate(image, rotated_template, cv2.TM_CCOEFF_NORMED)
            loc = np.where(result >= threshold)
            for pt in zip(*loc[::-1]):
                locations.append((pt, rotated_template.shape[::-1]))
    return locations

# Match templates for inlets and outlets
inlet_locations = match_template_with_rotation(gray_image, inlet_templates)
outlet_locations = match_template_with_rotation(gray_image, outlet_templates)
muffler_locations = match_template_with_rotation(gray_image, muffler_templates, threshold=0.8)

# Draw rectangles for inlets
for (pt, size) in inlet_locations:
    cv2.rectangle(image, pt, (pt[0] + size[1], pt[1] + size[0]), (0, 255, 0), 2)
    cv2.putText(image, 'Inlet', (pt[0], pt[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# Draw rectangles for outlets
for (pt, size) in outlet_locations:
    cv2.rectangle(image, pt, (pt[0] + size[1], pt[1] + size[0]), (0, 0, 255), 2)
    cv2.putText(image, 'Outlet', (pt[0], pt[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

# Draw rectangles for mufflers
for (pt, size) in muffler_locations:
    cv2.rectangle(image, pt, (pt[0] + size[1], pt[1] + size[0]), (255, 0, 255), 2)
    cv2.putText(image, 'Muffler', (pt[0], pt[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 255), 2)

# Show the output image
cv2.imshow("Detected Inlets and Outlets", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
