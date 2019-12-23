# SSDC-Autobooker 
A python-selenium script built to automate the booking of practical lessons from the Singapore Safety Driving Center [website](https://ssdcl.com.sg/)

## Dependencies

This script uses Selenium with the google chrome web driver. Run `pip install selenium` to install selenium. 
If you wish to use a different web driver (eg. Firefox) visit the python selenium [documentation](https://selenium-python.readthedocs.io/installation.html#drivers) for instructions on where and how to download the web drivers and replace the current chromedriver.exe file. Remember to replace the name in `chromedriver = os.path.abspath("chromedriver.exe")` with your driver name.

## Usage

### Email Setup

This script sends automated emails through the gmail smtp to let you know when a booking has been made. To enable, type "y" when prompted by the console. For your own local use, turn on allow less secure apps for your gmail account [here](https://myaccount.google.com/lesssecureapps). 

### Running the script

Navigate to the directory where you downloaded the files and call `python script.py` and follow the command line instructions.

The script supports the option to enable a range of your desired date and 6 days ahead for autobooking. Type "y" when prompted by the command line to enable this. Otherwise a static date will be used for the search and booking.

Only practical lessons booking is supported.
