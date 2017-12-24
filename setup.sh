sudo mv boot_lightshow.sh /etc/init.d
sudo chmod +x /etc/init.d/boot_lightshow.sh
sudo chown root:root /etc/init.d/boot_lightshow.sh

sudo update-rc.d boot_lightshow.sh defaults
sudo update-rc.d boot_lightshow.sh enable

# Install pyaudio to read audio inputs from Mac devices
sudo apt-get install python-pyaudio

cd ..

sudo apt-get install libasound2-dev

# Install audio inputs to read inputs from Linux devices
git clone https://github.com/larsimmisch/pyalsaaudio.git
cd pyalsaaudio
python setup.py build
sudo python setup.py install

cd ..

pip install -r requirements.txt

# clean up
sudo rm -rf pyalsaaudio
