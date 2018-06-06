echo off
echo Compiling..
transcrypt -nab --xtrans="%APPDATA%\\npm\\babel.cmd --presets=react --plugins=emotion" --parent=.none src/index.py
