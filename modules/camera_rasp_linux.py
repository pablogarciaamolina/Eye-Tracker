from picamera2 import Picamera2
from configparser import ConfigParser
from numpy import ndarray

CAMERA_INI = "camera"
CAMERA_RESOLUTION_INI = "resolution"
FORMAT = 'main_format'

class CameraInput_RaspBerryPi:

    def __init__(self, config: ConfigParser) -> None:
        '''
        Initializes Camera Input
        '''

        self.resolution: list[int] = tuple(map(int, config[CAMERA_INI][CAMERA_RESOLUTION_INI].split(',')))

        self.picam = Picamera2()
        self.picam.preview_configuration.main.size = self.resolution
        self.picam.preview_configuration.main.format= config[CAMERA_INI][FORMAT]
        self.picam.preview_configuration.align()
        self.picam.configure("preview")
        self.picam.start()
     
    def feed(self) -> ndarray:
        '''
        Feeds a new image
        '''

        return self.picam.capture_array()
