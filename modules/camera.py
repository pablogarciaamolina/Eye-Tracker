import cv2
from configparser import ConfigParser

class CameraInput_Windows:

    def __init__(self, config: ConfigParser, index: int = 0) -> None:
        '''
        Initializes Camera Input

        index -> Index of device's camera. Default 0.
        '''

        # OPEN CAMERA 
        self.camera = cv2.VideoCapture(index)
        ## Check if the camera is successfully opened
        if not self.camera.isOpened():
            raise Exception("Unable to open camera")
        
        # SET ATRIBUTES
        ## Counter for images
        self.counter: int = 0
        ## Where to store captured images
        self.captured_images_directory: str = config['directories']['data_images_captured']
     
    def feed(self) -> cv2.Mat:
        '''
        Feeds a new image
        '''

        # Read a frame from the camera
        ret, frame = self.camera.read()
        
        if ret:
            return frame
        
        return None
    
    def save_image(self, image: cv2.Mat, verbose: int = 0) -> None:
        '''
        Saves the captured image
        '''

        cv2.imwrite(f'{self.captured_images_directory}/captured_image{self.counter}.jpg', image)
        if verbose == 1: print("Image captured")
        self.counter += 1  

    def stop(self) -> None:
        '''
        Closes camera
        '''

        # Release the camera and close the window
        self.camera.release()
        cv2.destroyAllWindows()

    def destroy_windows(self) -> None:

        cv2.destroyAllWindows()