# Muscle Milk

### Description
The following is a personal project completed by myself. My sister reached out asking if I could compile a list of muscles from [here](http://www.meddean.luc.edu/lumen/MedEd/GrossAnatomy/dissector/mml/) for her upcoming medical school exam. I knew a solution was possible manually, however I wasn't sure how to do it programatically. After a good half-day of coding, it looks like I was able to compile a solution.

The code extracts the "muscle code" (as I've dubbed it) which is a short letter code, often an acronym of the muscle, that appends to the end of the URL to access that muscle's detail page. Then it looks through each page, pulls the "muscle code", "muscle", "origin", "insertion", "action", and "nerve" for each muscle in the alphabetical list. For the purposes of this task, I ran with the asusumption that the alphabetical list was the master list, and was inherently complete, more on this later. My sister then requested that the muscles be shown with its repsective region, hence the additional for look to match the "region" variable to each "muscle code". It appeared one muscle was on the alphaebtical list, but was not within a region list. As such, based on my (limited) knowledge, I added it to the head/neck region list.

The final deliverable is an excel file with a column for each variable listed in the preceding paragraph. Muscles that are in multiple regions are listed multiple times with the different region name, hence why the deliverable length is longer than the initial alphabetical master length.

### Required Packages
  `import sys
  import re
  import requests
  import pprint (this was used iteratively to view the output but wasn't used in the final code)
  import pandas as pd
  from bs4 import BeautifulSoup
  
