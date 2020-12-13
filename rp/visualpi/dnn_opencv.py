# Import necessary libraries
import numpy as np
import cv2

class ObjectDetectionOpenCV():
    def __init__(self, model_path='models/MobileNetSSD_deploy.caffemodel', prototxt='models/MobileNetSSD_deploy.prototxt.txt', labels='models/object_detection_classes_pascal_voc.txt'):
        # Initialize class labels of the dataset
        CLASSES = [line.strip() for line in open(labels)]
        print('[INFO]', CLASSES)
        print("[INFO] Loading model")
        self.net = cv2.dnn.readNetFromCaffe(prototxt, model_path)

    def _boxes_coordinates(self,
                            image,
                            boxes,
                            classes,
                            scores,
                            max_boxes_to_draw=20,
                            min_score_thresh=.5):

        if not max_boxes_to_draw:
            max_boxes_to_draw = boxes.shape[0]
        number_boxes = min(max_boxes_to_draw, boxes.shape[0])
        person_boxes = []
        for i in range(number_boxes):
            if scores is None or scores[i] > min_score_thresh:
                box = tuple(boxes[i].tolist())
                ymin, xmin, ymax, xmax = box
                im_height, im_width, _ = image.shape
                left, right, top, bottom = [int(z) for z in (xmin * im_width, xmax * im_width, ymin * im_height, ymax * im_height)]
                person_boxes.append([(left, top), (right, bottom), scores[i], LABELS[classes[i]]])
        return person_boxes


    def detect(self, image, threshold=0.1):
        (h, w) = image.shape[:2]
        # Resize and normalize image for network input
        blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)
        # Pass the blob through the network and obtain the detections and predictions
        self.net.setInput(blob)
        detections = self.net.forward()

        person_boxes = []
        for i in range(detections.shape[2]):
            # Extract the confidence (i.e., probability) associated with the prediction
            confidence = detections[0, 0, i, 2]

            # Filter out weak detections by ensuring the `confidence` is
            # greater than the minimum confidence
            if confidence > threshold:
                # Extract the index of the class label from the `detections`,
                # then compute the (x, y)-coordinates of the bounding box for
                # the object
                class_id = int(detections[0, 0, i, 1])
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype('int')
                person_boxes.append([(startX, startY), (endX, endY), confidence, LABELS[class_id]])

        # Find detected boxes coordinates
        return person_boxes
