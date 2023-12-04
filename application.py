import os, sys, time
import cv2
import configparser
from modules.calibration import Calibration
# from modules.camera import CameraInput_Windows
from modules.camera_rasp_linux import CameraInput_RaspBerryPi
from modules.polygon_detector import Polygon_Detector
from modules.console_interface import Console_Interface
from modules.tracker import Tracker

interface = Console_Interface()

def calibrate_camera(camera, calibrator: Calibration, min_calibration_images: int, take_picture_key: str):
    '''
    Runs calibration for the camera
    '''

    interface.title('calibration system:')
    interface.start_load('Calibrating camera')
    code = calibrator.calibrate()
    while code == -1:

        interface.finish_load(text='ERROR')
        interface.message(f'· Unable to calibrate, not at lest {min_calibration_images} pattern images provided')
        try_again = interface.text_input("Take pictures for calibration? (Y/N)", expected_answer='Y')

        if try_again:

            # START GATHERING IMAGES FOR CALIBRATION
            take = True
            counter = 0
            interface.message(f'Press {take_picture_key} to take a picture', underlined=True)
            while take:

                frame = camera.feed()
                key = cv2.waitKey(1)
                cv2.imshow('Taking pictures for calibration', frame)

                if key & 0xFF == ord(take_picture_key):
                    interface.message(f'Image nº{counter+1} taken')
                    cv2.imwrite( os.path.join(calibrator.calibration_images_directory, f'calibration_image{counter}.jpg'), frame)
                    counter += 1
                    if counter >= min_calibration_images:
                        take = False

            # CALIBRATE AGAIN
            interface.start_load('Calibrating camera')
            code = calibrator.calibrate()

        else:
            code = 0

    if code == 1: interface.finish_load()
    camera.destroy_windows()

def security(camera, polygon_detector: Polygon_Detector, pattern: list[str], n_trys: int, picture_key: str):
    '''
    Runs security system. Based on polygon recognition

    RETURN CODE

    1: All good, passed
    -1: Wrong pattern denied
    '''

    interface.title('security system:')

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
            interface.message(f"· Image taken, detected: {detected}")
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
    
    camera.destroy_windows()

    if trys_left <= 0:

        interface.colored_message('NO ATTEMPTS LEFT, ACCESS DENIED', color='red')
        return -1
    
    else:

        interface.colored_message('ACCESS GRANTED', color='green')
        return 1

def run_tracker(camera, tracker: Tracker, start_key: str, exit_key: str):

    interface.title('Tracking system:')
    start = interface.text_input(f'Enter {start_key} to start tracking: ', expected_answer=start_key, next_line=False)
    if start:
        interface.message(f'Press {exit_key} to end tracking', underlined=True)

        run = True
        while run:

            frame = camera.feed()

            frame = tracker.return_detected(frame)

            cv2.imshow('Eye Tracking', frame)

            key = cv2.waitKey(1)

            if key & 0xFF == ord(exit_key):
                run = False

        camera.destroy_windows()

def main():

    configuration = configparser.ConfigParser()
    configuration.read(os.path.join(os.path.dirname(__file__), './config/config.ini'))

    # IMAGE INPUT
    camera = CameraInput_RaspBerryPi(configuration)
    # CALIBRATOR
    calibration = Calibration(configuration)
    min_calibration_images = int(configuration['calibration']['min_number_calibration_images'])
    take_picture_calibration_key = configuration['calibration']['take_picture_key']
    # DETECTOR
    polygon_detector = Polygon_Detector(configuration)
    security_pattern = list(map(str, configuration['security']['polygon_password'].split(',')))
    security_max_trys = int(configuration['security']['number_of_attempts'])
    security_key: str = configuration['security']['security_picture_key']
    # EYE TRACKER
    tracker = Tracker(configuration)
    stop_tracking_key = configuration['tracker']['tracker_stop_key']
    start_tracking_key = configuration['tracker']['tracker_start_key']
    

    interface.special_intro()
    calibrate_camera(camera, calibration, min_calibration_images, take_picture_calibration_key)
    passed = security(camera, polygon_detector, security_pattern, security_max_trys, security_key)
    if passed == 1: run_tracker(camera, tracker, start_tracking_key, stop_tracking_key)

    camera.stop()


if __name__ == '__main__':

    main()
