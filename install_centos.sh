echo ">>> 1. install Python 3.6"
sudo yum -y install epel-release
sudo yum -y install https://centos7.iuscommunity.org/ius-release.rpm
sudo yum -y install python36u
sudo yum -y install python36u-pip

python3.6 -V
pip3.6 -V

echo ">>> 2. install FFmpeg"
sudo rpm –import http://li.nux.ro/download/nux/RPM-GPG-KEY-nux.ro
sudo rpm -Uvh http://li.nux.ro/download/nux/dextop/el7/x86_64/nux-dextop-release-0-5.el7.nux.noarch.rpm
sudo yum -y install ffmpeg ffmpeg-devel

ffmpeg -version

echo ">>> 3. repository"
python3 -m venv .env
source .env/bin/activate
pip3 install -r requirements.txt

echo ">>> 4. configuration"
read -p "Input your bot token: " token
touch global_config/protected_config.py
echo "_telegrambot_token = '$token'" > global_config/protected_config.py

read -p "Input your repo absolute location: " base_dir
echo "_base_dir = '$base_dir'" > global_config/environment_config.py

read -p "Input your cache absolute location: " temp_dir
echo "_temp_dir = '$temp_dir'" >> global_config/environment_config.py

echo ">>> 5. setup entrance"
echo "On more step to done, setup your bot entrance by yourself."
