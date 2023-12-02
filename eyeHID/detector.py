import cv2
import configparser
import os
import matplotlib.pyplot as plt
import imageio


class PolygonDetector:

    def __init__(self) -> None:
        
        # GET CONFIG FILE
        config = configparser.ConfigParser()
        config.read(os.path.join(os.path.dirname(__file__), '../config/config.ini'))


        self.polygon_vertices = [int(value) for value in config['polygon_vertices'].values()]
        self.polygon_shapes = [value for value in config['polygon_shapes'].values()]

        self.gaussian_dimensions = list(map(int, config['polygon_detection_parameters']['gaussian_blur_dimensions'].split(',')))
        self.sigma_x = float(config['polygon_detection_parameters']['gaussian_sigma_x'])
        self.sigma_y = float(config['polygon_detection_parameters']['gaussian_sigma_y'])
        self.canny_threshold_x = float(config['polygon_detection_parameters']['canny_threshold_x'])
        self.canny_threshold_y = float(config['polygon_detection_parameters']['canny_threshold_y'])
        self.min_contour_area = float(config['polygon_detection_parameters']['min_contour_area'])
        self.min_distance_inbetween_shapes = float(config['polygon_detection_parameters']['min_distance_inbetween_shapes'])

    def find_contours(self, image: cv2.Mat) -> list[cv2.Mat]:

        # Convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply GaussianBlur to reduce noise and help with contour detection
        blurred = cv2.GaussianBlur(gray, ksize=self.gaussian_dimensions, sigmaX=self.sigma_x, sigmaY=self.sigma_y)

        # Use Canny edge detector to find edges
        edges = cv2.Canny(blurred, self.canny_threshold_x, self.canny_threshold_y)

        # Find contours in the edged image
        contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Filter contours based on their area (adjust the threshold as needed)
        min_contour_area = self.min_contour_area
        return [cnt for cnt in contours if cv2.contourArea(cnt) > min_contour_area]
    
    def detect_polygons(self, image: cv2.Mat) -> list:

        contours = self.find_contours(image)

        results = []
        last_first_vertex_in_contour = contours[0][0,0]
        j = 0
        for cnt in contours:

            approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)

            found = False
            # Check if its the same as last time
            new_vertex = cnt[0,0]
            if j >0 and cv2.norm(last_first_vertex_in_contour, new_vertex) < self.min_distance_inbetween_shapes:

                found = True
            last_first_vertex_in_contour = new_vertex

            i = 0
            while i <= len(self.polygon_vertices) and not found:
                if len(approx) <= self.polygon_vertices[i]:
                    results.append(self.polygon_shapes[i])
                    found = True
                i += 1
            j += 1

        return results


    def draw_polygons(self, image: cv2.Mat) -> cv2.Mat:

        contours = self.find_contours(image)

        result_image = image.copy()
        last_first_vertex_in_contour = contours[0][0,0]
        j = 0
        for cnt in contours:

            approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)

            found = False
            # Check if its the same shape as last time
            new_vertex = cnt[0,0]
            if j > 0 and cv2.norm(last_first_vertex_in_contour, new_vertex) < self.min_distance_inbetween_shapes:
                found = True
            last_first_vertex_in_contour = new_vertex

            i = 0
            while i <= len(self.polygon_vertices) and not found:
                if len(approx) <= self.polygon_vertices[i]:
                    cv2.drawContours(result_image, [approx], -1, (0,255,255), 3)
                    (x,y)=cnt[0,0]
                    cv2.putText(result_image, self.polygon_shapes[i], (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
                    found = True
                i += 1
            j += 1

        return result_image
    

if __name__ == '__main__':


    detector = PolygonDetector()
    image = imageio.imread('../data/captured_images/captured_image1.jpg')
    result_image = detector.draw_polygons(image)
    cv2.imshow('Image', result_image)
    cv2.waitKey(0)  # Wait until a key is pressed
    cv2.destroyAllWindows()  # Close the window

