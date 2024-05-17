import cv2
import numpy as np
import glob

# Load the HVAC drawing image
image_path = "images/image-3.png"
#image_path = "images/hus_5-11.png"
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

def match_template_with_rotation(image, templates, threshold=0.70):
    print("Matching templates with rotation...")
    boxes = []
    for template in templates:
        for angle in range(0, 360, 30):  # Rotate templates every 30 degrees
            rotated_template = rotate_image(template, angle)
            result = cv2.matchTemplate(image, rotated_template, cv2.TM_CCOEFF_NORMED)
            loc = np.where(result >= threshold)
            for pt in zip(*loc[::-1]):
                boxes.append([pt[0], pt[1], pt[0] + rotated_template.shape[1], pt[1] + rotated_template.shape[0]])
    return np.array(boxes)

def non_max_suppression_fast(boxes, overlap_thresh=0.3):
    if len(boxes) == 0:
        return []
    
    print("Applying Non-Maximum Suppression...")
    # Ensure boxes is a 2D array
    boxes = np.array(boxes)
    if boxes.ndim == 1:
        boxes = np.expand_dims(boxes, axis=0)
    
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
inlet_boxes = match_template_with_rotation(gray_image, inlet_templates, threshold=0.75)
outlet_boxes = match_template_with_rotation(gray_image, outlet_templates, threshold=0.75)
muffler_boxes = match_template_with_rotation(gray_image, muffler_templates, threshold=0.65)

# Debug print to check the shapes
print("Inlet boxes shape:", inlet_boxes.shape)
print("Outlet boxes shape:", outlet_boxes.shape)
print("Muffler boxes shape:", muffler_boxes.shape)

# Apply Non-Maximum Suppression
inlet_boxes_nms = non_max_suppression_fast(inlet_boxes)
outlet_boxes_nms = non_max_suppression_fast(outlet_boxes)
muffler_boxes_nms = non_max_suppression_fast(muffler_boxes)

# Draw rectangles for inlets
for (x1, y1, x2, y2) in inlet_boxes_nms:
    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
    cv2.putText(image, 'Inlet', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# Draw rectangles for outlets
for (x1, y1, x2, y2) in outlet_boxes_nms:
    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
    cv2.putText(image, 'Outlet', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

# Draw rectangles for mufflers
for (x1, y1, x2, y2) in muffler_boxes_nms:
    cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2)
    cv2.putText(image, 'Muffler', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)


# save imag eto disk
cv2.imwrite('output.png', image)

print("Inlets: ", len(inlet_boxes_nms))
print("Outlets: ", len(outlet_boxes_nms))
print("Mufflers: ", len(muffler_boxes_nms))


# Show the output image
#cv2.imshow("Detected Inlets and Outlets", image)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
