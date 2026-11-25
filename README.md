# heard-pota-spots
A short python script that compares the heard CW spots of a specified node on Reverse Beacon Network to the spots available on the pota.app website to find POTA activators who you can actually hear.

This script scrapes the Reverse Beacon Network (RBN) website for CW spots from a spotter station that is specified in the settings.ini file. Then it scrapes all spots from the POTA.app website, and compares them. If there are any matches, then hopefully that same activator will be heard from your QTH. 
To let you know that a spot has been heard, a discord message is sent.

### settings.ini
Upon first cloning this repo, rename "CHANGE_ME_settings.ini" to "settings.ini". Then edit the file to 
1. Customise the RBN spotter to one closest to your QTH.
2. Select whether the script should use firefox or chrome to scrape the two websites. Whichever you choose will need to be installed on the machine running the script. If trying to run on a raspberry pi, do "sudo apt-get install chromium-chromedriver" then use the "chrome" setting in settings.ini
3. Add the webhook URL for the discord channel the script should message in to. You may need to create a private discord server to host this channel if you do not already have one. Once the server is made, make a channel, then right click on the channel -> Edit Channel -> Integrations -> Webhooks -> New Webhook. Enter a name that the messages will come from, and copy the URL into this settings file.

### Python dependencies
Before running the script, you should create a virtual environment (venv), activate it, and then use pip to install the dependencies listed in the requirements.txt file. Instructions to do that are as follows:
1. Open a terminal window in this folder
2. "python -m venv ./"
3. ".venv\Scripts\activate"
4. "pip install -r requirements.txt"
The requirements includes the dependencies of the "core" dependencies. If you would prefer to just install the core ones directly, they are "selenium" and "requests". 
