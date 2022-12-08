# VO2Max Tracker

Garmin (devices and connect app/website) does not show your VO2Max as a floating point number. Instead it shows it as an integer number, so it can be difficult to see your training progress regarding to this metric.

The purpose of this small utility is to track your VO2Max as a floating point number.

## Features

- Chart of your VO2Max gropped by sport
- Support any sport where VO2Max is calculated (walking, running, cycling)
- Activities: Support for .fit files (activities stored in your device) as well as .zip files (activities exported from [Garmin Connect](https://connect.garmin.com/)

## Requirements

- Python 3.9 or newer (it could be run on oldest versions, but it was not tested)
  - [Installation](https://www.python.org/getit/)
- Poetry Package Manager. 
  - [Installation](https://python-poetry.org/docs/#installation)

## Setup

1. Install Python and Poetry as noted in previous section
2. Download this project from git (...), decompress the .zip file wherever you want in your PC.
3. Connect your device, copy the folder "activity" into "activities"
