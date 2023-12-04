# Proyecto_Vision / Eye tracker 

Pablo García Molina y Andrés Martinez

<h2> <em> Intro </em> </h2>
<p>Image and video processing application. It runs 3 modules that consists on a calibration system, a security and a tracking system</p>
<h4>Calibration System</h4>
<p> Fits a pinhole model and obtains the intrinsic, extrinsics and other parameters of the camera. It requieres a minimum of 10 images of 
a Chessboard pattern in order to calibrate the parameters correctly. This images can be provided or taken by the user in real time.</p>
<h4>Security System</h4>
<p>It is based on image recognision of polygons and provides or denies access to the real time tracker by detecting a predifined secuence of shapes</p>
<h4> Tracker System</h4>
<p>Real time eye tracker application. It works creating a blob detector that recognises firstly faces and separates them form the rest of the image. Then
it does the same for the eyes and search for the important points on the image that resembles the ones of an eye and draws a circle over it.</p>
<h2> <em> Requirements </em> </h2>

- python 3.7
- opencv-python
- picamera2
- termcolor

<h2> <em> Guide </em> </h2>
