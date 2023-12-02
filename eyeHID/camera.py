import cv2
import configparser
import os
import matplotlib.pyplot as plt

class CameraInput:

    def __init__(self, index: int = 0) -> None:
        '''
        Initializes Camera Input

        index -> Index of device's camera. Default 0.
        '''

        # OPEN CAMERA 
        self.camera = cv2.VideoCapture(index)
        ## Check if the camera is successfully opened
        if not self.camera.isOpened():
            raise Exception("Unable to open camera")
        
        # GET CONFIG FILE
        config = configparser.ConfigParser()
        config.read(os.path.join(os.path.dirname(__file__), '../config/config.ini'))

        # SET ATRIBUTES
        ## Counter for images
        self.counter: int = 0
        ## Where to store captured images
        self.captured_images_directory: str = config['directories']['data_images_captured']

        
    def feed(self, display: bool = False) -> cv2.Mat:
        '''
        Feeds a new image
        '''

        # Read a frame from the camera
        ret, frame = self.camera.read()

        # Display the frame
        if display and ret: plt.imshow(frame)
        
        return frame if ret else -1
    
    def save_image(self, image: cv2.Mat, verbose: int = 0) -> None:
        '''
        Saves the captured image
        '''

        cv2.imwrite(f'{self.captured_images_directory}/captured_image{self.counter}.jpg', image)
        if verbose == 1: print("Image captured")
        self.counter += 1
        
    def run(self, stop_key: str = 'q', picture_key: str = ' ') -> None:
        '''
        Runs camera feed
        '''

        while True:
            
            img = self.feed(display=True)

            # Display the frame
            cv2.imshow('Live Video', img)

            # Check for key events
            key = cv2.waitKeyEx(1)

            # Break the loop if the 'q' key is pressed
            if key & 0xFF == ord(stop_key):
                break

            # Capture and save an image if the spacebar is pressed
            elif key & 0xFF == ord(picture_key):
                self.save_image(img, verbose=1)
        
        self.stop()

    def stop(self) -> None:
        '''
        Closes camera
        '''

        # Release the camera and close the window
        self.camera.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":

    c = CameraInput()
    c.run()