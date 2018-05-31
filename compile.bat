echo off
echo Compiling..
transcrypt -nab --xtrans="%APPDATA%\\npm\\babel.cmd --presets=react" --parent=.none src/index.py
