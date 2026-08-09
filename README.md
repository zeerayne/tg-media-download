# Telegram media download
Downloads media of specified type from telegram entity

## Installation

This project uses uv for dependency management and virtual environments.

Requirements: Python 3.10+

Install uv if it is not already installed:

    $ curl -LsSf https://astral.sh/uv/install.sh | sh

Then install the project dependencies:

    $ uv sync

If you want to use the environment manually, activate it:

    $ source .venv/bin/activate

Now it's time to obtain Telegram API ID and hash.

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

You can run the script either with uv directly or after activating the virtual environment.

    $ uv run python dwnld.py <params>

Or:

    $ source .venv/bin/activate
    $ python dwnld.py <params>

After the script starts, you will be prompted to enter the verification code.
  
### Run script example
    
    $ python dwnld.py --id=1234567 --hash=c6405a8d35979585cfb39b7ca2dc45fc --phone=+16549871245 \
    --entity=awesome_channel --type=audio
