import os, sys, time
import cv2
import configparser
from modules.calibration import Calibration
from modules.camera_rasp_linux import CameraInput_RaspBerryPi
from modules.polygon_detector import Polygon_Detector
from modules.console_interface import Console_Interface

interface = Console_Interface()

def calibrate_camera(calibrator: Calibration):
    '''
    Runs calibration for the camera
    '''

    interface.title('camera calibration:')
    interface.start_load('Calibrating camera')
    calibrator.calibrate()
    interface.finish_load()

def security(camera: CameraInput_RaspBerryPi, polygon_detector: Polygon_Detector, pattern: list[str], n_trys: int, picture_key: str):
    '''
    Runs security system. Based on polygon recognition

    RETURN CODE

    1: All good, passed
    -1: Wrong pattern denied
    '''

    interface.title('security sistem:')
    print(pattern)

    trys_left: int = n_trys
    i = 0
    l = len(pattern)
    interface.message(f'Password contains {l} polygons, you have {n_trys} attempts', underlined=True)
    interface.message(f'-> Polygon nº{i+1}: Press "{picture_key}" for detection')
    while trys_left > 0 and  i < l:

        frame = camera.feed()
        cv2.imshow('Live video', frame)
        key = cv2.waitKey(1)

        if key & 0xFF == ord(picture_key):

            detected: list[str] = polygon_detector.detect_polygons(frame)
            interface.message(f"Image taken, detected: {detected}")
            if len(detected) == 1:

                if pattern[i] in detected:
                    interface.colored_message('Corret', color='green')
                    i += 1
                    if i < l: interface.message(f'-> Polygon nº{i+1}: Press "{picture_key}" for detection')
                else:
                    interface.colored_message('Incorrect', color='red')
                    trys_left -= 1
                    interface.message(f'{trys_left} attempts left')
                      
            elif len(detected) > 1:
                interface.message('· Too many shapes, picture is not clear, unable to detect, try again')
            elif len(detected) < 1:
                interface.message('· No shapes detected, picture is not clear, try again')

    if trys_left <= 0:

        interface.colored_message('NO ATTEMPTS LEFT, ACCESS DENIED', color='red')
        return -1
    
    else:

        interface.colored_message('ACCESS GRANTED', color='green')
        return 1



if __name__ == '__main__':

    configuration = configparser.ConfigParser()
    configuration.read(os.path.join(os.path.dirname(__file__), './config/config.ini'))

    # IMAGE INPUT
    camera = CameraInput_RaspBerryPi(configuration)
    # CALIBRATOR
    calibration = Calibration(configuration)
    # DETECTOR
    polygon_detector = Polygon_Detector(configuration)
    security_pattern = list(map(str, configuration['security']['polygon_password'].split(',')))
    security_max_trys = int(configuration['security']['number_of_attempts'])
    security_key: str = configuration['security']['security_picture_key']
    # EYE TRACKER

    calibrate_camera(calibration)
    security(camera, polygon_detector, security_pattern, security_max_trys, security_key)


    # do = True
    # while True:

    #     im = camera.feed()
    #     if do: cv2.imshow('video', im)
    #     key = cv2.waitKey(1)

    #     if key & 0xFF == ord(security_key):

    #         new = polygon_detector.draw_polygons(im)
    #         # Display the processed image
    #         cv2.imshow('Processed Image', new)
    #         do = False

    #     if key == 27:  # Check for the 'Esc' key to exit the loop
    #         break