import cv2
import numpy as np
import glob

# Load the HVAC drawing image
#image_path = "images/hus_5-01.png"
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

def match_template_with_rotation(image, templates, threshold=0.6):
    locations = []
    for template in templates:
        for angle in range(0, 360, 30):  # Rotate templates every 30 degrees
            rotated_template = rotate_image(template, angle)
            result = cv2.matchTemplate(image, rotated_template, cv2.TM_CCOEFF_NORMED)
            loc = np.where(result >= threshold)
            for pt in zip(*loc[::-1]):
                locations.append((pt, rotated_template.shape[::-1]))
    return locations

def match_template_with_rotation_v2(image, templates, threshold=0.8):
    boxes = []
    for template in templates:
        for angle in range(0, 360, 30):  # Rotate templates every 30 degrees
            rotated_template = rotate_image(template, angle)
            result = cv2.matchTemplate(image, rotated_template, cv2.TM_CCOEFF_NORMED)
            loc = np.where(result >= threshold)
            for pt in zip(*loc[::-1]):
                boxes.append([pt[0], pt[1], pt[0] + rotated_template.shape[1], pt[1] + rotated_template.shape[0]])
    return np.array(boxes)

def match_template(image, templates, threshold=0.8):
    locations = []
    for template in templates:
        result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(result >= threshold)
        for pt in zip(*loc[::-1]):
                    locations.append((pt, template.shape[::-1]))
    return locations

def non_max_suppression_fast(boxes, overlap_thresh=0.3):
    if len(boxes) == 0:
        return []
    
    boxes = np.array(boxes)
    pick = []
    
    x1 = boxes[:, 0]
    y1 = boxes[:, 1]
    x2 = boxes[:, 2]
    y2 = boxes[:, 3]

    area = (x2 - x1 + 1) * (y2 - y1 + 1)
    idxs = np.argsort(y2)
    
    while len(idxs) > 0:
        last = len(idxs) - 1
        i = idxs[last]
        pick.append(i)
        
        xx1 = np.maximum(x1[i], x1[idxs[:last]])
        yy1 = np.maximum(y1[i], y1[idxs[:last]])
        xx2 = np.minimum(x2[i], x2[idxs[:last]])
        yy2 = np.minimum(y2[i], y2[idxs[:last]])
        
        w = np.maximum(0, xx2 - xx1 + 1)
        h = np.maximum(0, yy2 - yy1 + 1)
        
        overlap = (w * h) / area[idxs[:last]]
        
        idxs = np.delete(idxs, np.concatenate(([last], np.where(overlap > overlap_thresh)[0])))
    
    return boxes[pick].astype("int")

# Match templates for inlets and outlets
inlet_locations =   match_template_with_rotation_v2(gray_image, inlet_templates)
outlet_locations =  match_template_with_rotation_v2(gray_image, outlet_templates)
muffler_locations = match_template_with_rotation_v2(gray_image, muffler_templates, threshold=0.8)

# Apply non-maximum suppression to remove overlapping bounding boxes
inlet_locations = non_max_suppression_fast(inlet_locations)
outlet_locations = non_max_suppression_fast(outlet_locations)
#muffler_locations = non_max_suppression_fast(muffler_locations)


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

# save imag eto disk
cv2.imwrite('output.png', image)

print("Inlets: ", len(inlet_locations))
print("Outlets: ", len(outlet_locations))
print("Mufflers: ", len(muffler_locations))

# Show the output image
#cv2.imshow("Detected Inlets and Outlets", image)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
