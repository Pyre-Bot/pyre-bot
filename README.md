# InfernalGaming Discord Bot

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
python_valve==0.2.1
psutil==5.6.7
discord.py==1.2.5
pygtail==0.11.1
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
You need to get API tokens from the [Discord Developer Portal](https://discordapp.com/developers/docs/intro) to use those respective functions of the bot.

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
role = privilledged-server-role
channel = channel-id-here
```

* **discord_token**: The API key you retrieved in the earlier step
* **server_address**: the IP/domain of your server
* **server_port**: The port configed for queries
* **steamcmd**: The path to the steamcmd folder
* **ror2ds**: Used for ror2.py, path to the Risk of Rain 2 Dedicated Server folder
* **BepInEx**: Path to the BepInEx folder
* **role**: The Discord role you want using protected commands
* **channel**: The Discord channel ID to output live chat

*Never upload online or share your config file to anyone you do not trust. These API keys are private and can result in your access from the services being removed if they get out.*

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
  *Protected command*
* status : Lists the game server status via Steamworks API
* mods : Outputs a list of mods to chat
  * Coming soon!
* config : Outputs the current server config to chat
  * Coming soon!
* start_chat : Reads the server logs and outputs live chat from the game to a specified server channel
* stop_chat : Stops reading for live server chat

#### Modifying the commands

By default the bot is configured to manage a Risk of Rain 2 server. This can be changed by calling the executables for other servers and pointing the checks at their respective logs.

## Built With

* [Discord.py](https://github.com/Rapptz/discord.py) - Discord API wrapper for Python
* [Python-valve](https://github.com/serverstf/python-valve) - Steamworks API wrapper for Python

## Contributing

Please read [CONTRIBUTING.md](https://github.com/InfernalPlacebo/ig-bot) for details on our code of conduct, and the process for submitting pull requests to us.

To add functionality for other games or servers, add a new file in the **cogs** folder.

## Authors

* **Wade Fox** - *Creator* - [GitHub](https://github.com/InfernalPlacebo)

See also the list of [contributors](https://github.com/InfernalPlacebo/ig-bot/graphs/contributors) who participated in this project.

## License

This project is licensed under the GPL-3.0 License - see the [LICENSE.md](LICENSE.md) file for details

## Changelog

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
