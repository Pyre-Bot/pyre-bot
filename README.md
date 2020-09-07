# Pyre Bot

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Discord](https://img.shields.io/discord/660914305515913227?label=Discord)](http://discord.pyre-bot.com)
[![GPLv3 license](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://github.com/InfernalPlacebo/ig-bot/blob/master/LICENSE)
[![Documentation Status](https://readthedocs.org/projects/pyre-bot/badge/?version=latest)](https://pyre-bot.readthedocs.io/en/latest/?badge=latest)
[![LiberPay](https://liberapay.com/assets/widgets/donate.svg)](https://liberapay.com/PyreBot/donate)

Please find complete documentation on [ReadTheDocs](https://docs.pyre-bot.com)

The Pyre Discord Bot has one main goal: Create an easy-to-use way to manage a maintain dedicated game servers from within Discord. From sending commands to the game console to allowing players to initiate a restart vote, Pyre was created to make it as easy as possible.

Feel free to join our [Discord](http://discord.pyre-bot.com) if you want to discuss the bot or hang out!

## Getting Started

These instructions will help make sure your system is ready to run the bot and help you get started using it for your needs.

### Prerequisites

The bot is built upon Python 3.8 but has been tested working with Python 3.7 without any issues. The dependencies for the usage are updated regularly in the requirements.txt file and these can be installed via:

```
pip install -r requirements.txt
```

If you get an aiohttp error while attempting to install discord.py, run the following command:

```
pip install --no-use-pep517 discord.py
```

### Usage

Clone the repo and build the docker image with `docker build -t pyre-bot .`. Run the container by passing in the environment variables listed in `config/config.py` and the AWS keys, e.g: 
```
docker run --name pyre-bot -e AWS_ACCESS_KEY_ID="awskey" -e AWS_SECRET_ACCESS_KEY="awskey" -e ADMIN_CHANNELS="channels" -e ADMIN_ROLE="role" -e CHAT_AUTOSTART="true" -e CHAT_CHANNELS="channels" -e COMMANDS_CHANNELS="channels" -e DISCORD_TABLE="Discord_Stats" -e DISCORD_TOKEN="token" -e LINKED_ID="id" -e LOG_PATH="path" -e PLAYERS_TABLE="Players" -e SEQ_API="key" -e SERVER_ADDRESSES="server:port,server:port" -e SERVER_RESTART="true" -e STATS_ENDPOINT="url" -e STATS_REGION="region" -e STATS_TABLE="BotCommands_Stats" -e TRACK_STATS="yes" pyre-bot:latest 
```

#### API Tokens

##### Discord
You need to get an API token from the [Discord Developer Portal](https://discordapp.com/developers/docs/intro). The token is added to the config.ini file in the config folder.

##### AWS
Pyre Bot uses Amazon DynamoDB to store player stats from the servers and link Discord IDs to SteamIDs. You will need to setup an AWS account an add some tables to DynamoDB for this to work. Create the following tables:

* **Discord_Stats** - Primary key: DiscordID (String)
* **Players** - Primary key: DiscordID (String)
* **BotCommands_Stats** - Primary key: SteamID64 (String)

You need to pass the AWS access credentials to the bot via environment variables.

##### Seq
We use Seq to store logs from the game servers and the bot and to pass information from them. You will need to setup a Seq server and create API keys for each game server running.

#### Risk of Rain 2 requirements

The bot requires that you are using the following mods in your RoR2 server. Not having all of these mods installed and updated to their latest builds can result in certain features not working properly.

**Required Mods**
* [BepInEx](https://thunderstore.io/package/bbepis/BepInExPack/)
  * Change **redirectOutputLog** to **true** in your doorstop_config.ini to prevent double messages being sent to BepInEx terminal.
* [BotCommands](https://github.com/SuperRayss/BotCommands)
  * Used to send commands to the server from Discord
  * Build command included in README
* [R2DSE](https://thunderstore.io/package/Harb/R2DSEssentials/)
  * Outputs steam player names and IDs
* [DebugToolkit](https://thunderstore.io/package/Harb/DebugToolkit/)
  * Outputs run time and stages cleared
  * Enables additional commands to be sent to the server (i.e. give_item, give_equip)

## Bot Commands

### Available to everyone
* restart : Initiates a vote to restart the server
  * Requires a majority vote (at least 75% of in-game player count)
* votekick {player}: Initiates a 30-second vote to kick {player} from the Risk of Rain 2 server
  * Requires a majority vote (at least 75% of in-game player count)
* endrun : Initiates a 30-second vote to end the current run in the Risk of Rain 2 server
  * Requires a majority vote (at least 75% of in-game player count)
* info : Lists the game server status via Steamworks API
  * Listed info includes server name, current stage, player count, player names, and ping
* link {SteamID} : Allows players to see their play stats for the Risk of Rain 2 server
  * Assigns the "Linked" role (NOTE: requires further config to not be hardcoded)
* stats : Outputs your player stats to chat
  * Currently supported stats are Time Played, Stages Cleared, and Runs Completed

### Admin only
* start : Starts the Risk of Rain 2 server
* stop : Stops the Risk of Rain 2 server
* delete {number} : Deletes the given amount of messages in the channel
* say {message} : Sends an in-game message from the perspective of the server
* cmd {command with args} : Passes on a command to execute by the server
  * Very experimental as of now, only use when you are sure of the results, as passing commands in certain contexts can cause unhandled exceptions with BotCommands
* giveitem {player} {item} {quantity (default - 1)} : Gives a player a specified quantity of an item
* giveequip {player} {equip} : Gives a player a specified equipment
* help_admin : Lists admin commands and usage
* restart_admin : Restarts the server
* kick {player} : Kicks the player from the server.
* endrun_admin : Ends the current run

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
* **Rayss** - *Contributor and BotCommands creator* - [GitHub](https://github.com/SuperRayss), [Discord](http://discord.pyre-bot.com)

See also the list of [contributors](https://github.com/InfernalPlacebo/pyre-bot/graphs/contributors) who participated in this project.

## License

This project is licensed under the GPL-3.0 License - see the [LICENSE](LICENSE) file for details

## Changelog

### 0.9.0
* Full docker and container support
* Configuration is handled via environment variables
* Restructuring of files
* New documentation
* Added more admin commands
* A lot more stuff I don't remember

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
