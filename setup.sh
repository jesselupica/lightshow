sudo mv boot_lightshow.sh /etc/init.d

# Install pyaudio to read audio inputs from Mac devices
sudo apt-get install python-pyaudio

cd ..

# Install audio inputs to read inputs from Linux devices
git clone https://github.com/larsimmisch/pyalsaaudio.git
cd pyalsaaudio
python setup.py build
sudo python setup.py install

cd ..

pip install -r requirements.txt

# clean up
sudo rm -rf pyalsaaudio
