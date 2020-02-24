# Telegram media download
Downloads media of specified type from telegram entity

## Installation

First of all, pipenv should be installed
    
    $ pip install pipenv
    
Next, create virtualenv and install dependencies

    $ pipenv install
    
Now it's time to obtain telegram API ID and hash. 

1. [Login to your Telegram account](https://my.telegram.org/) with the phone number of the developer account to use.
1. Click under API Development tools.
1. A Create new application window will appear. Fill in your application details. There is no need to enter any URL, and only the first two fields (App title and Short name) can currently be changed later.
1. Click on Create application at the end. Remember that your API hash is secret and Telegram won’t let you revoke it. Don’t post it anywhere!

[More details](https://docs.telethon.dev/en/latest/basic/signing-in.html) in telethon docs 

    
That's all, now you are ready to use script

## Usage
Script parameters

Parameter|Parameter|Required|Value|Description
---------|---------|--------|-----|-----------
-i|--id|+| |Telegram api_id
-x|--hash|+| |Telegram api_hash
-p|--phone|+| |Phone number to authorize
-e|--entity|+| |Telegram entity (chat or channel) which media should be downloaded')
-P|--password| |If account is 2FA-enabled, password should be provided
-t|--type| |Choice: all, audio or photo. Default: all|Media type
-o|--output_dir| |Default: ./downloads|Directory to store downloaded files
-O|--overwrite| |No value, if option is submitted, files will be overwritten|Specifies whether will be files overwritten or skipped

Activate virtualenv
    
    $ pipenv shell
    
Run script example
    
    $ python dnld.py --id=1234567 --hash=c6405a8d35979585cfb39b7ca2dc45fc --phone=+16549871245 \
    --entity=awesome_channel --type=audio
    
After script start you will be promted to input verifivation code
