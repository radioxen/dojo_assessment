# dojo_assessment
Simple assessment for back-end and front-end

simple Fastapi web app to receive a csv file with home and target addresses and provide travel tiime for two means of transport, Driving and Public transit. 
It will return a chart with comparison of the mthods and time for each, along with distance of travel.

steps : 
  - git clone https://github.com/radioxen/dojo_assessment.git
  - pip install virtualenv
  - virtualenv your_venv --python=python3.8
  - source your_venv/bin/activate
  - pip install -r requirment.txt
  - uvicorn main:app --reload --port 8000 
  - navigate to the ip address provided in your terminal (by default it is http://127.0.0.1:8000/) and use the form to upload your csv
  
######
  
The CSV file should contain 2 columns, with headers (not name-sensetive). 1st column should be the home address and 2nd column should be the target address.
