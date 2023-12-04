import cv2
import numpy as np
from configparser import ConfigParser
from modules.config_rel import *


class Tracker:
    def __init__(self, config: ConfigParser):

        face_classifier_file = config[DIRECTORIES_MAIN][RAW_DATA] + '/' + config[TRACKER_MAIN][FACE_CASCADE_FILE]
        eye_classifier_file = config[DIRECTORIES_MAIN][RAW_DATA] + '/' + config[TRACKER_MAIN][EYE_CASCADE_FILE]
        self.face_classifier = cv2.CascadeClassifier(face_classifier_file)
        self.eye_classifier = cv2.CascadeClassifier(eye_classifier_file)


        self.detector_params = cv2.SimpleBlobDetector_Params()
        self.detector_params.filterByArea = bool(config[TRACKER_MAIN][BLOB_FILTERED_BY_AREA])
        self.detector_params.maxArea = float(config[TRACKER_MAIN][BLOB_FILTERED_MAX_AREA])
        self.detector = cv2.SimpleBlobDetector_create(self.detector_params)

        self.multiscale_factor = float(config[TRACKER_MAIN][MULTISCALE_SCALEFACTOR])
        self.multiscale_min_neightbours = int(config[TRACKER_MAIN][MULTISCALE_MIN_NEIGHTBOURS])
        self.blob_process_threshold = int(config[TRACKER_MAIN][BLOB_PROCESS_THRESHOLD])
        self.erosion_iteration = int(config[TRACKER_MAIN][EROSION_ITERATIONS])
        self.dilation_iteration = int(config[TRACKER_MAIN][DILATION_ITERATIONS])
        self.medianblur_ksize = int(config[TRACKER_MAIN][MEDIAN_BLUR_KSIZE])

        self.stop_tracking_key = config[TRACKER_MAIN][TRACKING_STOP_KEY]

    def create_gray(self,img):
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    def detect_faces(self, img):
        gray_frame = self.create_gray(img)
        classifier = self.face_classifier
        coords = classifier.detectMultiScale(gray_frame, self.multiscale_factor, self.multiscale_min_neightbours)
        if len(coords) > 0:
            biggest = (0, 0, 0, 0)
            for i in coords:
                if i[3] > biggest[3]:
                    biggest = i
            biggest = np.array([i], np.int32)
            for (x, y, w, h) in biggest:
                frame = img[y:y + h, x:x + w]
            return frame
        else:
            return None

    def detect_eyes(self,img):
        detected_eyes = []
        classifier = self.eye_classifier
        gray_frame = self.create_gray(img)
        eyes = classifier.detectMultiScale(gray_frame, self.multiscale_factor, self.multiscale_min_neightbours)
        height, width = np.size(img,0), np.size(img,1)
        
        for (x, y, w, h) in eyes:
            if y > height / 2:
                pass
            eyecenter = x + w / 2  
            if eyecenter < width * 0.5:
                detected_eyes.append(img[y:y + h, x:x + w])
            else:
                detected_eyes.append(img[y:y + h, x:x + w])
        return detected_eyes

    def blob_process(self,img, threshold):
        detector = self.detector
        gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, img = cv2.threshold(gray_frame, threshold, 255, cv2.THRESH_BINARY)
        img = cv2.erode(img, None, iterations=self.erosion_iteration)
        img = cv2.dilate(img, None, iterations=self.dilation_iteration)
        img = cv2.medianBlur(img, self.medianblur_ksize)
        keypoints = detector.detect(img)

        return keypoints


    def return_detected(self, frame: cv2.Mat):

        face_frame = self.detect_faces(frame)
        if face_frame is not None:
            eyes = self.detect_eyes(face_frame)
            for eye in eyes:
                if eye is not None:
                    keypoints = self.blob_process(eye, self.blob_process_threshold)
                    eye = cv2.drawKeypoints(eye, keypoints, eye, (0, 255, 0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

        return frame