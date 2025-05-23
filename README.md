Archived repository, new location: https://codeberg.org/jalbiero/vo2max-tracker
---

- [VO2Max Tracker](#vo2max-tracker)
  - [Features](#features)
  - [Interpreting results](#interpreting-results)
  - [Requirements](#requirements)
  - [Setup](#setup)
  - [Run](#run)
  - [Export](#export)
    - [Export to CVS](#export-to-cvs)
    - [Export to JSON](#export-to-json)
  - [Help](#help)
  - [Configuration](#configuration)
  - [Disclaimer](#disclaimer)
  - [Troubleshooting](#troubleshooting)
    - [Error when trying to execute _run_win.ps1_ on Windows](#error-when-trying-to-execute-run_winps1-on-windows)
    - [Chart is too small](#chart-is-too-small)
  - [Other related tools](#other-related-tools)
  - [For developers](#for-developers)
    - [Install full dependencies](#install-full-dependencies)
    - [Run application](#run-application)
    - [Run tests and code tools (isort, autopep and mypy)](#run-tests-and-code-tools-isort-autopep-and-mypy)
    - [Run tools without tests](#run-tools-without-tests)


# VO2Max Tracker

Garmin (devices and connect app/website) does not show your VO2Max as a floating point number. Instead it shows it as an integer value, so it can be difficult to see what your device really measures in each training session in order get a more precise feedback.

This simple application tracks the VO2Max value that your device has calculated in each training session. Be aware that the VO2Max showed by your device status (or Garmin Connect) can differ from the one that was measured (the value saved in the .FIT activity file). The watch applies a correction after the activity was finalized/saved. See [Interpreting results](#interpreting-results) later in this document for more information.

## Features

- Chart of your VO2Max grouped by sport

  ![Chart plot](doc/chat_plot.png)

- Support any sport where VO2Max is calculated (walking, running, cycling, swimming, etc)
- Activities
  - Support for raw .fit files (activities stored in your device)
  - Support for compressed fit files (.zip files) (activities exported from [Garmin Connect](https://connect.garmin.com/))
- Export your activities (only values defined in [class FitData](vo2max_tracker/fit/decoder.py) are exported)
  - Support for CVS files (easily read by Excel or any other spreedsheet)
  - Support for JSON files
- Cache of parsing results to improve execution speed

## Interpreting results

Let's see the following chart:

  ![Chart plot](doc/chart_interpreting_results.png)

- Jump in VO2Max
  - Values greater than "a value and a half" could be considered as a VO2Max improvement (does not always happen, but several values above the "half" for sure will end up in a new VO2Max).
  - Values stored in the .FIT activiy file are "corrected" by the device after the activity is finalized (in general, the device's VO2Max is one integer point above the .FIT's VO2Max). That's why the current VO2Max of 53 was upgraded to 54 when the calculated .FIT number hit the 52.6 value.
- Productive trainning status
  - When there is a breaking point in the VO2Max curve your device will show a **"productive"** status.

## Requirements

- Python 3.9 or newer (it could be run on older versions, but it was not tested)
  - [Installation](https://www.python.org/getit/)
- Poetry Package Manager.
  - [Installation](https://python-poetry.org/docs/#installation)

## Setup

1. Install Python and Poetry as noted in previous section
2. Download this project from [git](https://github.com/jalbiero/vo2max-tracker/archive/refs/heads/main.zip), decompress the .zip file wherever you want in your PC.
3. Connect your device,
4. Copy the content of the device folder _activity_ (or _ACTIVITY_) into the project folder _activities_ (you can change this default location if you want, see [Configuration](#configuration))
5. If you do not want to copy the activities from your device, you can download them from [Garmin Connect](https://connect.garmin.com/modern/) (one by one). Just select/view the activity you want to download, click on the upper right gear and select "Export Original". The zipped activity should be saved in the aforementioned _activity_ folder. It is not necessary to decompress the file.

    ![Export activity](doc/export_activity.png)

6. Execute the application using the provided script for your platform (run_linux.sh, run_mac.sh, or run_win.ps1)

## Run

In order to run the application just execute one of the provided scripts via command line or file explorer. Be aware that the first run will take some time due to the following things:

1. It is necessary to download the runtime software dependencies
2. Decoding (parsing) a FIT file is slow (at least in Python) so dependending on the number of activities you will have to wait. Don't worry, the decoding results are cached so the next time the start up will be almost instant (unless you add new activities that need to be parsed).

e.g. Run VO2Max Tracker on Linux (APP_DIRECTORY is where you downloaded the app)

```bash
$ APP_DIRECTORY/run_linux.sh
```

## Export

### Export to CVS

```bash
$ APP_DIRECTORY/run_linux.sh --csv --output my_activities.csv
```

### Export to JSON

```bash
$ APP_DIRECTORY/run_linux.sh --json --output my_activities.json
```

## Help

For a full list of options just invoke its command line help

```bash
$ APP_DIRECTORY/run_linux.sh --help

usage: app [-h] [-v] [-r] [-c] [-j] [-o OUTPUT]

optional arguments:
  -h, --help            show this help message and exit

General options:
  -v, --version         show VO2MaxReader version
  -r, --rcache          Recreate FIT cache. The application start-up will be very slow, be patience.

Export options:
  -c, --csv             Export all activities in CSV format
  -j, --json            Export all activities in JSON format
  -o OUTPUT, --output OUTPUT
                        Output file (when not specified, './export_output.txt' will be used
```

## Configuration

For a custom configuration, just edit the file [vo2max_tracker/config.py](vo2max_tracker/config.py)

## Disclaimer

VO2Max Tracker was developed and tested on Linux (openSUSE 15.4 with Anaconda3 2022-10/Python 3.9.13, bash 4.4.23, zsh 5.6 and PowerShell for Linux 7.2.3) with data from Garmin FR-945 and FR-920. Older devices like the latter currently have partial support, so it is possible that no all information will be shown on the tooltip. VO2Max Tracker was also tested on Windows 10 (Python 3.11.1). I am sorry, but I do not have a Mac, so let me know if you have any issue on macOS.

## Troubleshooting

### Error when trying to execute _run_win.ps1_ on Windows

If you get the following error:

```powershell
PS C:\Users\Javier\vo2max_tracker> .\run_win.ps1
.\run_win.ps1 : File C:\Users\Javier\vo2max_tracker\run_win.ps1 cannot be loaded because running
scripts is disabled on this system. For more information, see about_Execution_Policies at
https:/go.microsoft.com/fwlink/?LinkID=135170.
At line:1 char:1
+ .\run_win.ps1
+ ~~~~~~~~~~~~~
    + CategoryInfo          : SecurityError: (:) [], PSSecurityException
    + FullyQualifiedErrorId : UnauthorizedAccess
```

Then you need to change the execution policy. Open a PowerShell terminal and paste the following Cmdlet:

```powershell
Set-ExecutionPolicy -Scope "CurrentUser" -ExecutionPolicy "RemoteSigned"
```

If anyone know how to change the execution policy just for _run_win.ps1_ script (instead of all scripts for the current user), please let me know, thanks in advance.

### Chart is too small

It is quite possible that you have a High DPI monitor. Try increasing the value of **DPI** property in the [configuration file](vo2max_tracker/config.py). A normal value is 100, but, as a sort of compromise between high and low resolution monitors, the default one was set to 150 (1.5 x). Try setting it to 200 (2x) or greater.

## Other related tools

- [Runanalyze](https://runalyze.com)
- https://github.com/jimmykane/fit-parser
- https://github.com/CraigMohn/fitparseR
- https://github.com/bleenhou/fitparser


## For developers

If you use [VSCode](https://code.visualstudio.com/) or [VSCodium](https://vscodium.com/) for development, you must use a virtual environment inside the project (e.g. vo2max-tracker/.venv directory) as noted in this [stack overflow answer](https://stackoverflow.com/a/64434542)

The following examples assume a terminal located in *vo2max-tracker* directory (or _vo2max-tracker-main_ if you downloaded the .zip file instead of cloning the repository)

### Install full dependencies

```bash
$ poetry install
```

### Run application

```bash
$ poetry run app
```

### Run tests and code tools (isort, autopep and mypy)

```bash
$ poetry run tests [optional_arguments_for_pytest]
```

### Run tools without tests

```bash
$ poetry run tools
```
