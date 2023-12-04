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
<h2> <em> Requirements </em> </h2>

- python 3.7
- opencv-python
- picamera2
- termcolor

<h2> <em> Guide </em> </h2>

<h3>Setup.py</h3>
<p>Use the setup.py to establish the directories distribution defined on the configiration file and install the dependencies of the requirements.txt</p>
<h3>Application.py</h3>
<p>Running the application.py file will start the application, firstly the calibration system will be activated and if enough images are provided the camera will be calibrated, if not images of the calibration pattern can be taken in real time.</p>
<p>Then the security system will start, the user will have a limited number of attempts to provide the correct secuence of polygons. If te user runs out odf attempts acces will be denied and the application will finish.</p>
<p>Lastly if the secuence is procided sucessfully, access will be granted and the tracker application will start. The eye tracker ill run until the user exits the session.</p>

<h2>Configuration</h2>
<p></p>
