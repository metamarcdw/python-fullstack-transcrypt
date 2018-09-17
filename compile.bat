echo off
echo Compiling..
transcrypt -nab --xtrans="node_modules\.bin\babel.cmd --presets=react --plugins=emotion" --parent=.none src/index.py
