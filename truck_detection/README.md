# Setup Truck Detection

Run these commands in the same directory as this file on *WINDOWS*:

```shell
# git clone https://github.com/Eclipse-SDV-Hackathon-Chapter-Two/maestro
cd maestro/truck_detection
python3 -m venv venv
# on linux: 
#source venv/bin/activate
# on windows:
.\venv\Scripts\activate
pip install opencv-python torch pandas requests Pillow
python truck_detector.py
```