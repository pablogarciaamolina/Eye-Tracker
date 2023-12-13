# Proyecto_Vision / Eye tracker 

Pablo García Molina y Andrés Martinez

<h2> <em> Intro </em> </h2>
<p>Image and video processing application. It runs 3 modules that consist of a calibration system, a security system, and a tracking system</p>
<h3>Calibration System</h3>
<p>Fits a pinhole model and obtains the intrinsic, extrinsics and other parameters of the camera. It requires a minimum of 10 images of 
a Chessboard pattern to calibrate the parameters correctly. These images can be provided or taken by the user in real time.</p>
<h3>Security System</h3>
<p>It is based on image recognition of polygons and provides or denies access to the real-time tracker by detecting a predefined sequence of shapes</p>
<h3> Tracker System</h3>
<p>Real-time eye tracker application. It works by creating a blob detector that recognizes faces and separates them from the rest of the image. Then it does the same for the eyes and searches for the important points on the image that resemble the ones of an eye and draws a circle over it.</p>

<h2> <em> Guide </em> </h2>

<h3>setup.py</h3>
<p>Use the setup.py to establish the directories distribution defined in the configuration file and install the dependencies of the requirements.txt</p>
<h3>application.py</h3>
<p>Running the application.py file will start the application. The application is set to run on a RaspberryPi device. It is also suited to run on Windows, but for that, a few changes need to be done. Simply change the imported module for the camera input to the one for Windows, then change the camera in the main body of the file.</p>
  
  <p>Firstly the calibration system will be activated, and if enough images are provided, the camera will be calibrated. If not, images of the calibration pattern can be taken in real-time.</p>
<p>Then the security system will start; the user will have a limited number of attempts to provide the correct sequence of polygons. If the user runs out of attempts, access will be denied, and the application will finish.</p>
<p>Lastly, if the sequence is provided successfully, access will be granted, and the tracker application will start. The eye tracker will run until the user exits the session.</p>

<h2>Configuration</h2>
<p>
  The project allows for easy configuration of directories arrangement, camera specification, and even image and video processing parameters. This is all achieved through a `configuration.ini` file located in the `/config` directory.
</p>

### File Explanation

[directories]

- **data:** Base directory for storing data. Default: `data`
- **data_calibration:** Directory for storing calibration data. Default: `data/calibration_data`
- **data_calibration_images:** Directory for storing calibration images. Default: `data/calibration_data/calibration_images`
- **data_raw:** Directory for storing raw data. Default: `data/raw_data`
- **data_images_captured:** Directory for storing captured images. Default: `data/captured_images`
- **config:** Configuration directory. Default: `config`

[camera]

- **resolution:** Camera resolution setting. Default: `320, 240`
- **main_format:** Main image format. Default: `RGB888`

[calibration]

- **calibration_layout_pattern:** Pattern layout for camera calibration. Default: `6, 4`
- **min_number_calibration_images:** Minimum number of calibration images required. Default: `10`
- **take_picture_key:** Key to trigger capturing calibration images. Default: `x`

[polygon_shapes]

- **triangle, square, pentagon, hexagon, circle:** Various polygon shapes supported. Default: `triangle, square, pentagon, hexagon, circle`

[polygon_vertices]

- **triangle_n_vertices, square_n_vertices, pentagon_n_vertices, hexagon_n_vertices, circle_n_vertices:** Number of vertices for each polygon. Default: `3, 4, 5, 6, 10`

[polygon_detection_parameters]

- **gaussian_blur_dimensions, gaussian_sigma_x, gaussian_sigma_y, canny_threshold_x, canny_threshold_y, min_contour_area, min_distance_inbetween_shapes:** Parameters for polygon detection algorithm. Default: `5, 5, 1, 1, 110, 110, 100, 30`

[security]

- **polygon_password:** Password made up of supported polygons. Default: `triangle, square, pentagon, hexagon`
- **number_of_attempts:** Number of attempts allowed for security validation. Default: `10`
- **security_picture_key:** Key to trigger security picture capture. Default: `x`

[tracker]

- **face_cascade_classifier_detector_file, eye_cascade_classifier_detector_file:** File names for face and eye cascade classifiers. Default: `face_class.xml`, `eye_class.xml`
- **simple_blob_detector_param_filter_by_area, simple_blob_detector_param_max_area, blob_process_threshold:** Parameters for blob detection. Default: `True, 1500, 37`
- **detector_multiscaledtetector_scalefactor, detector_multiscaledtetector_min_neightbours:** Parameters for multiscale object detection. Default: `1.3, 5`
- **erosion_iterations, dilation_iterations, median_blur_size:** Parameters for image processing. Default: `2, 4, 5`
- **tracker_stop_key, tracker_start_key:** Keys to start and stop the tracker. Default: `q`, `x`

</p>

<h2> <em> Requirements </em> </h2>

- python 3.7 (or above)
- opencv-python
- picamera2 (only if running on a RaspberryPi)
- termcolor
