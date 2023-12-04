import os
import cv2
import numpy as np
import copy
from configparser import ConfigParser
from modules.config_rel import *

class Calibration():

    def __init__(self, config: ConfigParser) -> None:
        
        # SET ATRIBUTES
        self.resolution: list[int] = list(map(int, config[CAMERA_INI][CAMERA_RESOLUTION_INI].split(',')))
        self.calibration_data_directory: str = config[DIRECTORIES_INI][CAMERA_CALIBRATION_DIRECTORY_INI]
        self.calibration_images_directory: str = config[DIRECTORIES_INI][CAMERA_CALIBRATION_IMAGES_DIRECTORY_INI]
        self.min_number_calibration_images: int = int(config[CALIBRATION_INI][N_CALIBRATION_IMAGES])
        self.calibration_pattern_layout: tuple[int] = tuple(map(int, config[CALIBRATION_INI][CALIBRATION_PATTERN_LAYOUT].split(',')))

    def load_calibration_images(self):
        filenames = os.listdir(self.calibration_images_directory)
        return [cv2.imread(self.calibration_images_directory + '/' + filename) for filename in filenames]
    
    def get_chessboard_points(self, chessboard_shape, dx, dy):
   
        points = np.empty([0,3])
        for i in range(chessboard_shape[1]):
            for j in range(chessboard_shape[0]):
                points = np.vstack((points, np.array([dx*i, dy*j, 0])))
    
        return points
    
    def calibrate(self) -> int:
        '''
        Calibrates camera and creates calibration files

        RETURN CODE

        1: Calibrated and files created
        -1: Unable to calibrate, not enough images to calibrate
        '''

        imgs = self.load_calibration_images()

        if len(imgs) < self.min_number_calibration_images:

            return -1
        else:

            imgs_grey = [cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) for img in imgs]
    
            corners = [cv2.findChessboardCorners(img, self.calibration_pattern_layout) for img in imgs]
            corners2 = copy.deepcopy(corners)

            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.01)
 
            cornersRefined = [cv2.cornerSubPix(i, cor[1], self.calibration_pattern_layout, (-1, -1), criteria) if cor[0] else [] for i, cor in zip(imgs_grey, corners2)]

            cb_points = self.get_chessboard_points(self.calibration_pattern_layout, 30, 30)
 
            valid_corners = [ref for cor, ref in zip(corners, cornersRefined) if cor[0]]
            num_valid_images = len(valid_corners)
            image_points = np.asarray(valid_corners, dtype=np.float32)
    
            object_points = np.asarray([cb_points for _ in range(num_valid_images)], dtype=np.float32)
    
            rms, intrinsics, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(object_points, image_points, self.resolution, None, None)
    
            extrinsics = list(map(lambda rvec, tvec: np.hstack((cv2.Rodrigues(rvec)[0], tvec)), rvecs, tvecs))

            np.save(self.calibration_data_directory + '/' + "intrinsics_" + str(self.resolution[0]) + '_' + str(self.resolution[1]), intrinsics)
            np.save(self.calibration_data_directory + '/' + "extrinsics_" + str(self.resolution[0]) + '_' + str(self.resolution[1]), extrinsics)
            np.save(self.calibration_data_directory + '/' + "rms_" + str(self.resolution[0]) + '_' + str(self.resolution[1]), rms)

            return 1

 
if __name__ == "__main__":
   

    c = Calibration()
    c.calibrate()