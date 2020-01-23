# InfernalGaming Discord Bot

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)[![DeepSource](https://static.deepsource.io/deepsource-badge-light-mini.svg)](https://deepsource.io/gh/InfernalPlacebo/ig-bot/?ref=repository-badge)![Discord](https://img.shields.io/discord/509196313431375874)[![GPLv3 license](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://github.com/InfernalPlacebo/ig-bot/blob/master/LICENSE)

This Discord bot was created primarily to be used by the InfernalGaming server to manage game servers and add other functionality to the server that wasn't available elsewhere or could be improved upon to serve the community. Feel free to join our [Discord](https://discord.gg/YewZwpc) if you want to discuss the bot or hang out!

## Getting Started

These instructions will help make sure your system is ready to run the bot and help you get started using it for your needs.

### Prerequisites

The bot is built upon Python 3.8 but has been tested working with Python 3.7 without any issues. The dependencies for the usage are updated regularly in the requirements.txt file and these can be installed via:

```
pip install -r requirements.txt
```

As of writing the current requirements are:

```
pygtail==0.11.1
psutil==5.6.7
python_valve==0.2.1
python_a2s==1.1.1
discord.py==1.2.5
discord==1.0.1
valve==0.0.0
```

If you get an aiohttp error while attempting to install discord.py, run the following command:

```
pip install --no-use-pep517 discord.py
```

### Installing

Clone the repo to wherever you want the bot to reside. You can run the bot by calling bot.py. You will also need [SteamCMD](https://developer.valvesoftware.com/wiki/SteamCMD) installed on your machine to run the updates for the game servers.

#### API Tokens
You need to get an API token from the [Discord Developer Portal](https://discordapp.com/developers/docs/intro). The token is added to the config.ini file in the config folder.

#### Setting variables
Some variables need to be set before using the bot to make sure it is looking in the correct place for files and information. In the **config/config.ini** file you will be able to config the following:

```
[API]
discord_token = token

[RoR2]
server_address = your-server-address
server_port = your-server-port
steamcmd = path-to-steamcmd
ror2ds = path-to-ror2ds
bepinex = path-to-bepinex
botcmd = path-to-botcmd
role = privilledged-server-role
channel = channel-id-here
auto-start-chat = true
hidden_mods = hidden-mods-here
```

* **discord_token**: The API key you retrieved in the earlier step
* **server_address**: the IP/domain of your server
* **server_port**: The port configured for queries
* **steamcmd**: The path to the steamcmd folder
* **ror2ds**: Used for ror2.py, path to the Risk of Rain 2 Dedicated Server folder
* **BepInEx**: Path to the BepInEx folder
* **botcmd**: Path to the folder containing your botcmd.txt file
* **role**: The Discord role you want using protected commands
* **channel**: The Discord channel ID to output live chat
* **auto-start-chat**: Set to false to prevent the bot from outputting chat to a Discord channel when it launches
* **hidden_mods**: Add mods that you don't want to be listed by the mods command, ships with a default list

*Never upload online or share your config file to anyone you do not trust. These API keys are private and can result in your access from the services being removed if they get out.*

#### Risk of Rain 2 requirements

The bot assumes that you are using mods in your RoR2 server, or at the very least have BepInEx loaded. If you do not have BepInEx the bot will not be able to read outputs from starting or live chat.

**Recommendations**
* BepInEx
  * Change **redirectOutputLog** to **true** in your doorstop_config.ini to prevent double messages being sent to BepInEx terminal.
* R2DSE

## Running and using the bot

After adding the API keys and creating a .env file you can get started by running the bot.py file located in the main directory. The bot will output a message stating that it is connected to Discord and ready to listen when it starts. Once you get the confirmation message you are able to start issuing commands to your bot using one of the command prefixes ('r!', 'ig!', '>').

### Bot Commands

* start : Starts the specified server, by default Risk of Rain 2
  * *Protected command*
* stop : Stops the specified server, by default Risk of Rain 2
  * *Protected command*
* restart : Initiates a vote to restart the server
  * Defaults to 60 seconds, but can be changed by adding a number after the command
  * Example for 30 second timer: restart 30
* update : Updates the specified server, by default Risk of Rain 2
  * *Protected command*
* status : Lists the game server status via Steamworks API
* mods : Outputs a list of mods to chat
* config : Outputs the current server config to chat
  * Coming soon!
* start_chat : Reads the server logs and outputs live chat from the game to a specified server channel
  * *Protected command*
* stop_chat : Stops reading for live server chat
  * *Protected command*
* votekick [player] : Initiates a 60-second vote to kick [player] from the Risk of Rain 2 server
  * Requires a majority vote that at least meets 75% of the in-game player count

#### Modifying the commands

By default the bot is configured to manage a Risk of Rain 2 server. This can be changed by calling the executables for other servers and pointing the checks at their respective logs.

## Built With

* [Discord.py](https://github.com/Rapptz/discord.py) - Discord API wrapper for Python
* [Python-A2S](https://github.com/Yepoleb/python-a2s) - Steamworks API wrapper for Python

## Contributing

Please read [CONTRIBUTING.md](https://github.com/InfernalPlacebo/ig-bot) for details on our code of conduct, and the process for submitting pull requests to us.

To add functionality for other games or servers, add a new file in the **cogs** folder.

## Authors

* **Wade Fox** - *Creator* - [GitHub](https://github.com/InfernalPlacebo), [Discord](discord.infernal.wtf)
* **Rayss** - *Contributor*

See also the list of [contributors](https://github.com/InfernalPlacebo/ig-bot/graphs/contributors) who participated in this project.

## License

This project is licensed under the GPL-3.0 License - see the [LICENSE.md](LICENSE.md) file for details

## Changelog

### 0.4.1
* Able to view server mods with the >mods commands
* ror2.py outputs load AND unload to terminal
* Misc code cleanup

### 0.4.0
* We welcome **Rayss** as a contributor to the project!
* Added config.ini
* New function to allow commands to output to a specified Discord channel
  * Requires the role specified in config.ini to use these commands
  * Discord channel is specified in config.ini
* ror2.py now outputs to terminal when it is loaded
* Minor fix to update command, removes log file *before* starting the update now
* Commands no longer require proper capitalization


### 0.3.2
* Thanks to Rayss for testing the bot and providing valuable feedback!
* Added a new variable for the Risk of Rain server location
* Removed link command until I can figure out how to fix it
* Fixed the status command to show the guild name vs being hard coded
* Load, unload, and reload commands can now only be used by the bot owner
* Changed restart vote to require 75% of the server player count (via Steamworks)

### 0.3.1
* Removed League of Legends support and dependencies... for now.

### 0.3.0
* Added the restart feature
  * Allows Discord members to initiate a restart vote for the RoR2 server.
* Changed the protected features check to a configurable variable
* Lowered wait time for start and stop commands to 15 seconds

### 0.2.0
* "Overhaul"
* **Added Cogs**
  * Added cogs to the code to provide expandable in future releases and allow cleaner reading and writing of code.
  * Cogs allow development and test of features and changes without having to completely restart bot.
