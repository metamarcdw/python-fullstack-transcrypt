### Example of React and Redux with Python using Transcrypt and Component.py
This project is adapted to Python from the "React from the Ground Up" course created by Tim Knight

First install Python>=3.6/pip, NodeJS/npm>=5.2, and Git:  
`sudo pacman -S python-pip npm git`  
Next, clone the repo  
`git clone https://github.com/metamarcdw/react-redux-transcrypt`  
Set up your React/Transcrypt environment:  
(Use of a virtual environment is recommended but not required)  
```
mkvirtualenv transcrypt
pip install git+https://github.com/qquick/transcrypt@master#egg=transcrypt
pip install git+https://github.com/metamarcdw/Component.py@master#egg=Component_py

cd react-redux-transcrypt/
npm install
npm install -g babel-cli  # If running Windows
```
We can now compile with Transcrypt and run our Webpack server  
```
make compile  
npm start  
```
OR (If running Windows)  
```
compile  
npm run win  
```
Open up a browser and connect to http://localhost:3000
