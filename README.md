##Systems Design Project - Group 11##

*Amanda Tollafield-Small, Kuba Kowalski, Alex Przybylski, Giedrius Zebrauskas, Atanas Dobrev, Fotis Papadogeorgopoulos, Darin Mihov*

#####Based on Group 7 work from 2014.#####
------

###Future SDP teams
The planner and vision are very good.

The vision is very accurate with the correct calibration and achieves above 30 FPS when only tracking two robots (faster than the camera).
Planner is based on a reactive system. You can modify the strategies accordingly for you robot design keeping the same planner.

###Running the system

In the root of the project, execute `python controller.py <pitch_number> <our_side> <our_color>` where *pitch_number* is either 0 for the main pitch and 1 for the secondary pitch. Colors are regular yellow and blue. Side can be either left or right.

####Vision calibration controls
Press the following keys to switch the thresholding scheme:
*r* - red
*p* - plate
*d* - black dots

Note that the colors of the plates themselves are ignored - you don't need them.

------
###Installation

#### Linux/DICE

To install the Polygon library, download the [source](https://bitbucket.org/jraedler/polygon2/downloads/Polygon2-2.0.6.zip), navigate inside and execute `python setup.py install --user`.

To install Argparse for python, download [ArgParse](http://argparse.googlecode.com/files/argparse-1.2.1.tar.gz), extract and run `python setup.py install --user`. All done.

In addition, *serial* library is required.

------
### Vision

* At the moment OpenCV + Python are being used. A [book](http://programmingcomputervision.com/downloads/ProgrammingComputerVision_CCdraft.pdf) on Computer Vision with OpenCV in Python is a decent starting point about what OpenCV can do.
* A detailed tutorial with examples and use cases can be found [here](https://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_tutorials.html) - going through it can be handy to understand the code
* For OpenCV installation (on DICE) use the script **vision_setup.sh** provided in the root directory.
* After executing the script, run `ipython` and do `import cv2`, if all executes fine then you're set.