#!/bin/bash
printf "Creating directory\n"
mkdir ~/codesetup_temp
cd codesetup_temp

printf "Installing Polygon library\n"
wget https://bitbucket.org/jraedler/polygon2/downloads/Polygon2-2.0.6.zip
unzip Polygon2-2.0.6.zip
cd Polygon2-2.0.6/
python setup.py install --user

printf "Installing ArgParse library\n"
wget http://argparse.googlecode.com/files/argparse-1.2.1.tar.gz
tar xzf argparse-1.2.1.tar.gz
cd argparse-1.2.1/
python setup.py install --user

printf "Installing serial\n"
pip install --user pyserial

printf "Downloading OpenCV 2.4.8.1; please wait\n"
wget https://github.com/Itseez/opencv/archive/2.4.8.1.zip

printf "Moving and unzipping OpenCV to /disk/scratch/sdp"
mv 2.4.8.1.zip  /disk/scratch/sdp
cd /disk/scratch/sdp
unzip 2.4.8.1.zip
rm 2.4.8.1.zip

printf "Installing OpenCV; grab some coffee, this will take time\n"
cd opencv-2.4.8.1/

printf "Replacing cl2cpp.cmake file\n"
#TODO Currently using dropbox, could be more sophisticated here
wget https://www.dropbox.com/s/qbyln23smdr81vr/cl2cpp.cmake
mv cl2cpp.cmake cmake/

printf "Running cmake\n"
mkdir build
cd build
cmake -D CMAKE_INSTALL_PREFIX=~/.local ..

printf "Running make; this will take a while...\n"
make

printf "Running make install; almost there...\n"
make install

printf "Dependencies are done. Clone the repository and you should be set\n"

printf "Cleaning up\n"
rm -rf ~/codesetup_temp
