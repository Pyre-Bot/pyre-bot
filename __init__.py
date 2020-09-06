"""Primary Pyre Bot package that contains all the code to control the bot.

This module is what contains the logic and functions that are used within Pyre Bot. You will find submodules
that contain required and optional files that allow the bot to use all of the commands and functions.

Examples
--------
Run the bot without creating a docker image for it:
    $ python bot.py

Run the bot with the dockerfile:
    $ docker build -t pyre-bot:latest . && docker run --name pyre-bot pyre-bot:latest

"""
