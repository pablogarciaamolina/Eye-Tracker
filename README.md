# Proyecto_Vision / Eye tracker 

Pablo García Molina y Andrés Martinez

<h2> <em> Intro </em> </h2>
<p>Image and video processing application. It runs 3 modules that consists on a calibration system, a security and a tracking system</p>
<h3>Calibration System</h3>
<p> Fits a pinhole model and obtains the intrinsic, extrinsics and other parameters of the camera. It requieres a minimum of 10 images of 
a Chessboard pattern in order to calibrate the parameters correctly. This images can be provided or taken by the user in real time.</p>
<h3>Security System</h3>
<p>It is based on image recognision of polygons and provides or denies access to the real time tracker by detecting a predifined secuence of shapes</p>
<h3> Tracker System</h3>
<p>Real time eye tracker application. It works creating a blob detector that recognises firstly faces and separates them form the rest of the image. Then
it does the same for the eyes and search for the important points on the image that resembles the ones of an eye and draws a circle over it.</p>

<h2> <em> Guide </em> </h2>

<h3>setup.py</h3>
<p>Use the setup.py to establish the directories distribution defined on the configiration file and install the dependencies of the requirements.txt</p>
<h3>application.py</h3>
<p>Running the application.py file will start the application. The application is set to run in a RaspberryPi device. It also suitted to run on windows, but for that few changes need to be done. Simply change the imported module for the camera input to the one for Windows, then change the camera in the main body of the file.</p>
  
  <p>Firstly the calibration system will be activated and if enough images are provided the camera will be calibrated, if not images of the calibration pattern can be taken in real time.</p>
<p>Then the security system will start, the user will have a limited number of attempts to provide the correct secuence of polygons. If te user runs out odf attempts acces will be denied and the application will finish.</p>
<p>Lastly if the secuence is procided sucessfully, access will be granted and the tracker application will start. The eye tracker ill run until the user exits the session.</p>

<h2>Configuration</h2>
<p>
  The project allows for easy configuration of directories arrangement, camera specification and even image and video processing parameters. This is all achieved through a configuration.ini file located on /config.
</p>


## Directories

### `data`

- **Description:** Base directory for storing data.
- **Default Value:** `data`

### `data_calibration`

- **Description:** Directory for storing calibration data.
- **Default Value:** `data/calibration_data`

### `data_calibration_images`

- **Description:** Directory for storing calibration images.
- **Default Value:** `data/calibration_data/calibration_images`

### `data_raw`

- **Description:** Directory for storing raw data.
- **Default Value:** `data/raw_data`

### `data_images_captured`

- **Description:** Directory for storing captured images.
- **Default Value:** `data/captured_images`

### `config`

- **Description:** Configuration directory.
- **Default Value:** `config`

## Camera

### `resolution`

- **Description:** Camera resolution setting.
- **Default Value:** `320, 240`

### `main_format`

- **Description:** Main image format.
- **Default Value:** `RGB888`

## Calibration

### `calibration_layout_pattern`

- **Description:** Pattern layout for camera calibration.
- **Default Value:** `6, 4`

### `min_number_calibration_images`

- **Description:** Minimum number of calibration images required.
- **Default Value:** `10`

### `take_picture_key`

- **Description:** Key to trigger capturing calibration images.
- **Default Value:** `x`

## Polygon Shapes

### `triangle`, `square`, `pentagon`, `hexagon`, `circle`

- **Description:** Various polygon shapes supported.
- **Default Values:** `triangle`, `square`, `pentagon`, `hexagon`, `circle`

## Polygon Vertices

### `triangle_n_vertices`, `square_n_vertices`, `pentagon_n_vertices`, `hexagon_n_vertices`, `circle_n_vertices`

- **Description:** Number of vertices for each polygon.
- **Default Values:** `3`, `4`, `5`, `6`, `10`

## Polygon Detection Parameters

### `gaussian_blur_dimensions`, `gaussian_sigma_x`, `gaussian_sigma_y`, `canny_threshold_x`, `canny_threshold_y`, `min_contour_area`, `min_distance_inbetween_shapes`

- **Description:** Parameters for polygon detection algorithm.
- **Default Values:** `5, 5`, `1`, `1`, `110`, `110`, `100`, `30`

## Security

### `polygon_password`

- **Description:** Password made up of supported polygons.
- **Default Value:** `triangle,square,pentagon,hexagon`

### `number_of_attempts`

- **Description:** Number of attempts allowed for security validation.
- **Default Value:** `10`

### `security_picture_key`

- **Description:** Key to trigger security picture capture.
- **Default Value:** `x`

## Tracker

### `face_cascade_classifier_detector_file`, `eye_cascade_classifier_detector_file`

- **Description:** File names for face and eye cascade classifiers.
- **Default Values:** `face_class.xml`, `eye_class.xml`

### `simple_blob_detector_param_filter_by_area`, `simple_blob_detector_param_max_area`, `blob_process_threshold`

- **Description:** Parameters for blob detection.
- **Default Values:** `True`, `1500`, `37`

### `detector_multiscaledtetector_scalefactor`, `detector_multiscaledtetector_min_neightbours`

- **Description:** Parameters for multiscale object detection.
- **Default Values:** `1.3`, `5`

### `erosion_iterations`, `dilation_iterations`, `median_blur_size`

- **Description:** Parameters for image processing.
- **Default Values:** `2`, `4`, `5`

### `tracker_stop_key`, `tracker_start_key`

- **Description:** Keys to start and stop the tracker.
- **Default Values:** `q`, `x`

<h2> <em> Requirements </em> </h2>

- python 3.7 (or above)
- opencv-python
- picamera2 (only if running on a RaspberryPi)
- termcolor
