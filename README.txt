Before running:

run the command below to install requirements from requirements.txt in your global ENV or once a Virtual ENV is set up:

pip install -r requirements.txt

to run:

sudo ./iotfridge_sun.sh

to test:

To use the fornt end application execute index.html from your browser or
double click index.html :)

additional test:

in the testing folder I provided some testing script reading product GTIN from exel files 
They are not officially included in this application and they are not covered by the modules in requirement.txt
here's the list of neede module if willing to try testing.

matplotlib==1.4.3
openpyxl==2.2.1
parse-this==1.0.3
plotly==1.6.16
pycurl==7.19.5.1

If willing to give it a go by activating the cherrypy server script in the iotfridge_route use this command to create your certificate

openssl req -new -x509 -keyout server.pem -out server.pem -days 365 -nodes

and also the required module

CherryPy==3.7.0

this application may be also found here: https://github.com/marioviti/IOTfidge.git
I reference to the README.md file for additional infos