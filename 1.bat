@echo off
pip install opencv-python pillow numpy moviepy
python %~dp0/main.py %*
pause