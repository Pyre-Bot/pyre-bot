# Pyre Bot

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)[![DeepSource](https://static.deepsource.io/deepsource-badge-light-mini.svg)](https://deepsource.io/gh/InfernalPlacebo/pyre-bot/?ref=repository-badge)![Discord](https://img.shields.io/discord/660914305515913227?label=Discord)[![GPLv3 license](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://github.com/InfernalPlacebo/ig-bot/blob/master/LICENSE)[![Documentation Status](https://readthedocs.org/projects/pyre-bot/badge/?version=latest)](https://pyre-bot.readthedocs.io/en/latest/?badge=latest)

The Pyre Discord Bot has one main goal: Create an easy-to-use way to manage a maintain dedicated game servers from within Discord. From sending commands to the game console to allowing players to initiate a restart vote, Pyre was created to make it as easy as possible.

Feel free to join our [Discord](http://discord.pyre-bot.com) if you want to discuss the bot or hang out!

## Getting Started

These instructions will help make sure your system is ready to run the bot and help you get started using it for your needs.

### Prerequisites

The bot is built upon Python 3.8 but has been tested working with Python 3.7 without any issues. The dependencies for the usage are updated regularly in the requirements.txt file and these can be installed via:

```
pip install -r requirements.txt
```

As of writing the current requirements are:

```
boto3==1.12.37
python_a2s==1.1.4
discord.py==1.3.3
psutil==5.6.7
requests==2.22.0
python_valve==0.2.1
discord==1.0.1
valve==0.0.0
```

If you get an aiohttp error while attempting to install discord.py, run the following command:

```
pip install --no-use-pep517 discord.py
```

### Installing

Clone the repo to wherever you want the bot to reside. You can run the bot by calling **bot.py**. You will also need [SteamCMD](https://developer.valvesoftware.com/wiki/SteamCMD) installed on your machine to run the updates for the game servers. When the bot first runs it will open a setup window where it prompts you for configuration settings. The window will also allow you to install the BotCommands plugin, this is required if you want access to functions that utilize in-game commands from Discord.

#### API Tokens

##### Discord
You need to get an API token from the [Discord Developer Portal](https://discordapp.com/developers/docs/intro). The token is added to the config.ini file in the config folder.

##### AWS
Pyre Bot uses Amazon DynamoDB to store player stats from the servers and link Discord IDs to SteamIDs. You will need to setup an AWS account an add some tables to DynamoDB for this to work. Create the following tables:

* **Discord_Stats** - Primary key: DiscordID (String)
* **Players** - Primary key: DiscordID (String)
* **Stats** - Primary key: SteamID64 (String)

You also need to setup AWS credentials on your computer. You can use [AWS CLI](https://aws.amazon.com/cli/) to do this.

#### Setting variables
Some variables need to be set before using the bot to make sure it is looking in the correct place for files and information. These variables are setup when the bot first runs when it opens the setup window. In the **config/config.ini** file you will be able to config the following:

```
[API]
discord_token = token

[General]
role = privileged-server-role

[RoR2]
server_address = your-server-address
server_port = your-server-port
steamcmd = path-to-steamcmd
ror2ds = path-to-ror2ds
bepinex = path-to-bepinex
channel = enter-channel-id
auto-start-chat = true
auto-server-restart = true
hidden_mods = hidden-mods-here
```

* **discord_token**: The API key you retrieved in the earlier step
* **role**: The Discord role you want using protected commands
* **admin-channel**: The channel ID that is used to issue admin commands
* **commands-channel**: The channel ID that anyone can use to issue commands
* **server_address**: the IP/domain of your server
* **server_port**: The port configured for queries
* **steamcmd**: The path to the steamcmd folder
* **ror2ds**: Used for ror2.py, path to the Risk of Rain 2 Dedicated Server folder
* **BepInEx**: Path to the BepInEx folder
* **channel**: The Discord channel ID to output live chat
* **auto-start-chat**: Set to false to prevent the bot from outputting chat to a Discord channel when it launches
* **auto-server-restart**: Set to false to prevent the bot from restarting the server every 60 minutes in which no players join the lobby
* **hidden_mods**: Add mods that you don't want to be listed by the mods command, ships with a default list

*Never upload online or share your config file to anyone you do not trust. These API keys are private and can result in your access from the services being removed if they get out.*

#### Risk of Rain 2 requirements

The bot requires that you are using the following mods in your RoR2 server. Not having all of these mods installed and updated to their latest builds can result in certain features not working properly.

**Required Mods**
* [BepInEx](https://thunderstore.io/package/bbepis/BepInExPack/)
    * Change **redirectOutputLog** to **true** in your doorstop_config.ini to prevent double messages being sent to BepInEx terminal.
* [BotCommands](https://github.com/SuperRayss/BotCommands)
    * Used to send commands to the server from Discord
* [R2DSE](https://thunderstore.io/package/Harb/R2DSEssentials/)
    * Outputs steam player names and IDs
* [DebugToolkit (Custom Fork by Rayss)](https://github.com/SuperRayss/DebugToolkit)
    * Outputs run time and stages cleared
    * Enables additional commands to be sent to the server (i.e. give_item, give_equip)

## Running and using the bot

The bot can be used by running **bot.py** in the main directory. The bot will output a message stating that it is connected to Discord and ready to listen when it starts. Once you get the confirmation message you are able to start issuing commands to your bot using one of the command prefixes ('r!', 'ig!', '>').

## Bot Commands

### Available to everyone
* restart : Initiates a vote to restart the server
    * Requires a majority vote (at least 75% of in-game player count)
* votekick [player] : Initiates a 30-second vote to kick [player] from the Risk of Rain 2 server
    * Requires a majority vote (at least 75% of in-game player count)
* endrun : Initiates a 30-second vote to end the current run in the Risk of Rain 2 server
    * Requires a majority vote (at least 75% of in-game player count)
* status : Lists the game server status via Steamworks API
* mods : Outputs a list of mods to chat
* config : Outputs the current server config to chat
    * Coming soon!

### Admin only
* start : Starts the Risk of Rain 2 server
* stop : Stops the Risk of Rain 2 server
* update : Updates the Risk of Rain 2 server
* start_chat : Reads the Risk of Rain 2 server logs and outputs live chat from the game to a specified Discord chat channel
* stop_chat : Stops reading out Risk of Rain 2 server chat
* say {message} : Sends an in-game message from the perspective of the server
* giveitem {item} {player} {quantity (default - 1)} : Gives a player a specified quantity of an item
* giveequip {equip} {player} : Gives a player a specified equipment

## Modifying the commands

By default the bot is configured to manage a Risk of Rain 2 server. This can be changed by calling the executables for other servers and pointing the checks at their respective logs.

## Built With

* [Discord.py](https://github.com/Rapptz/discord.py) - Discord API wrapper for Python
* [Python-A2S](https://github.com/Yepoleb/python-a2s) - Steamworks API wrapper for Python

## Contributing

Please read [CONTRIBUTING.md](https://github.com/InfernalPlacebo/pyre-bot/blob/master/CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

To add functionality for other games or servers, add a new file in the **cogs** folder.

## Authors

* **Wade Fox** - *Creator* - [GitHub](https://github.com/InfernalPlacebo), [Discord](http://discord.pyre-bot.com)
* **Rayss** - *Contributor* - [GitHub](https://github.com/SuperRayss), [Discord](http://discord.pyre-bot.com)

See also the list of [contributors](https://github.com/InfernalPlacebo/ig-bot/graphs/contributors) who participated in this project.

## License

This project is licensed under the GPL-3.0 License - see the [LICENSE](LICENSE.md) file for details

## Changelog
*Complete changelog available: [CHANGELOG](CHANGELOG.md)*

### 0.8.0
* Moved all stat tracking to Amazon DynamoDB for a better experience
* Custom version of the Pygtail module is now packaged with the bot
* Fixed an exception that occurred when the bot reconnected to Discord servers.
* Complete rewrite of setup.py
* Updated all requirements to newest versions
* Various fixes, improvements, and optimizations that makes everyone's lives better

### 0.7.0
* Added player stat tracking
* Improved integration with DebugToolkit
* Gets run time and stage number from the server log output directly
* Other things I've likely just forgotten about ... it's been a while

### 0.6.0
* Added configuration options for admin and command channels
    * This allows running multiple bot instances to manage more than one server
    * New global check makes sure the bot only listens to commands in these channels
* Added dictionaries for items, equipment, and stages
* Commands check dictionaries for values before issuing to the server
* Added basic logging
    * Log can be found in the **bot.log** file in the bot's directory.
* New *delete* command allows simpler delete or testing messages
* Improved error handling
* Steam query is now used to check if the server is running

### 0.5.1
* **Name changed to Pyre Bot**
* Added *giveequip* command
* *status* command now shows current stage name

### 0.5.0
* Added *say*, *endrun*, *giveitem*, and *votekick* commands
    * Requires [BotCommands](https://github.com/SuperRayss/BotCommands)
* Added a setup script to create config.ini on first launch
* Added option to output game chat to Discord channel
    * Enabled by default, change in config.ini
* Added automatic server restarts
    * Enabled by default, change in config.ini
* Using new Steamworks API
