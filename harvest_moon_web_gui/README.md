# HarvestMoon Web GUI
THIS WORK IS STILL UNDER CONSTRUCTION  
For up-to-date version, visit:
https://harvestmoon.appspot.com/

## Overview
This web gui is hosted on _Google Cloud Platform (GCP)_

## Dependencies
Install dependencies by running:
```
pip install -r requirements.txt 
```

## Local Testing Deployment
Run `main.py` python script under `harvest_moon_web_gui directory`:
```
python main.py
``` 
Open a browser and enter `localhost:8080` for local development.


### GCP App Deployment
To deploy app to _GCP_ (remember to update **requirement.txt**), simply run:
```
gcp app deploy
```