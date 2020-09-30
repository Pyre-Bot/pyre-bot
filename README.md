# Pyre Bot

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Discord](https://img.shields.io/discord/660914305515913227?label=Discord)](http://discord.pyre-bot.com)
[![GPLv3 license](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://github.com/Pyre-Bot/pyre-bot/blob/cloud/LICENSE)
[![Donate](https://liberapay.com/assets/widgets/donate.svg)](https://liberapay.com/PyreBot/donate)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](https://github.com/Pyre-Bot/pyre-bot/pulls)
[![Open Source Love svg3](https://badges.frapsoft.com/os/v3/open-source.svg?v=103)](https://github.com/Pyre-Bot)
[![ForTheBadge built-with-love](http://ForTheBadge.com/images/badges/built-with-love.svg)](https://github.com/Pyre-Bot)
![Docker Pulls](https://img.shields.io/docker/pulls/infernalplacebo/pyre-bot)

Pyre Bot has one main goal: Create an easy-to-use way to manage a maintain dedicated game servers from within Discord. From sending commands to the game console to allowing players to initiate a restart vote, Pyre was created to make it as easy as possible.

Feel free to join our [Discord](http://discord.pyre-bot.com) if you want to discuss the bot or hang out!

## Getting Started

These instructions will help make sure your system is ready to run the bot and help you get started using it for your needs.

### Prerequisites

The bot can be ran without everything listed below, but this is what we recommend:
* [Python 3.8.5](https://www.python.org/)
* [Docker](https://www.docker.com/)
* [Seq](https://datalust.co/seq)
* [DynamoDB](https://aws.amazon.com/dynamodb/)
* [BotCommands](https://github.com/Pyre-Bot)

### Installing

Pyre Bot is meant to be ran within Docker; we use [AWS ECS](https://aws.amazon.com/ecs/?nc2=h_ql_prod_ct_ecs) but you can use whatever container service you like. If you prefer not to use containers, install the requirements and it can be ran locally.

The latest pre-built Docker images can be found [here](https://hub.docker.com/repository/docker/infernalplacebo/pyre-bot/general).

##### Discord
You need to get an API token from the [Discord Developer Portal](https://discordapp.com/developers/docs/intro). The token will be used later in the environment variables. Invite the bot you create on the developer portal to your server and create the following for each RoR2 server you plan on running:

* Admin commands channel
* Public commands channel
* In-game chat channel
* Role for linked members

Also create a channel for all servers to post updates to.

##### Seq
Set up a Seq server to ingest the logs from the game, we use [Twiner's GotSeq](https://thunderstore.io/package/Twiner/GotSeq/) plugin to send our logs there. Seq needs te be set up with an API key for each server you plan to host.

##### AWS
Pyre Bot uses Amazon DynamoDB to store player stats from the servers and link Discord IDs to SteamIDs. You will need to setup an AWS account an add some tables to DynamoDB for this to work. Create the following tables:

* **BotCommands_Stats** - Primary key: DiscordID (String)
* **Players** - Primary key: DiscordID (String)

###### EFS
Since we host our Seq server in AWS as well as the bot, it is recommended to use EFS to enable your files to be shared between these services.

#### Environment Variables
Several variables need to be configured in the environment to make the bot run correctly, without these it will fail to run:

* ADMIN_CHANNELS
* ADMIN_ROLE
* AWS_ACCESS_KEY_ID
* AWS_SECRET_KEY_ID
* CHAT_CHANNELS
* COMMANDS_CHANNELS
* DISCORD_TOKEN
* LINKED_ID
* LOG_LEVEL
* LOG_PATH
* PLAYERS_TABLE
* SEQ_API
* SERVER_ADDRESSES
* SERVER_CHANNEL
* STATS_ENDPOINT
* STATS_REGION
* STATS_TABLE
* TRACK_STATS

*Never upload online or share your configuration to anyone you do not trust. These API keys are private and can result in your access from the services being removed if they get out.*

#### Risk of Rain 2 requirements

The bot requires that you are using the following mods in your RoR2 server. Not having all of these mods installed and updated to their latest builds can result in certain features not working properly.

**Required Mods**
* [BepInEx](https://thunderstore.io/package/bbepis/BepInExPack/)
  * Change **redirectOutputLog** to **true** in your doorstop_config.ini to prevent double messages being sent to BepInEx terminal.
* [BotCommands](https://github.com/Pyre-Bot)
  * Used to send commands to the server from Discord
* [R2DSE](https://thunderstore.io/package/Harb/R2DSEssentials/)
  * Outputs steam player names and IDs
* [DebugToolkit](https://thunderstore.io/package/Harb/DebugToolkit/)
  * Outputs run time and stages cleared
  * Enables additional commands to be sent to the server (i.e. give_item, give_equip)

## Running and using the bot

If running in Docker, launch the bot using the following example command; consult your hosting server if using another container platform.

```shell script
docker build -f Dockerfile -t pyre-bot:latest . 
&& docker run
-v path/to/your/log/folder:/data
--env ADMIN_CHANNELS=list,of,channels
--env ADMIN_ROLE=Admin
--env AWS_ACCESS_KEY_ID=
--env AWS_SECRET_ACCESS_KEY=
--env CHAT_CHANNELS=list,of,channels
--env COMMANDS_CHANNELS=list,of,channels
--env DISCORD_TOKEN=
--env LINKED_ID=
--env LOG_PATH=/data/
--env SEQ_API=
--env SERVER_ADDRESSES=list_of_server_address:with_ports
--env SERVER_CHANNEL=
--env STATS_ENDPOINT=https://dynamodb.us-east-2.amazonaws.com
--env STATS_REGION=us-east-2
--env STATS_TABLE=BotCommands_Stats
--env TRACK_STATS=yes
--env LOG_LEVEL=info
--name pyre-bot
--rm
pyre-bot:latest
```

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
* help : Displays all commands

### Admin only
* start : Starts the Risk of Rain 2 server
* stop : Stops the Risk of Rain 2 server
* delete {number} : Deletes the given amount of messages in the channel
* say {message} : Sends an in-game message from the perspective of the server
* cmd {command with args} : Passes on a command to execute by the server
  * Very experimental as of now, only use when you are sure of the results, as passing commands in certain contexts can cause unhandled exceptions with BotCommands
* giveitem {player} {item} {quantity (default - 1)} : Gives a player a specified quantity of an item
* giveequip {player} {equip} : Gives a player a specified equipment
* restart_admin : Restarts the server without votes
* help_admin : Displays information on how to use admin commands

## Modifying the commands

By default the bot is configured to manage a Risk of Rain 2 server. This can be changed by calling the executables for other servers and pointing the checks at their respective logs.

## Built With

* [Discord.py](https://github.com/Rapptz/discord.py) - Discord API wrapper for Python
* [Python-A2S](https://github.com/Yepoleb/python-a2s) - Steamworks API wrapper for Python

## Contributing

Please read [CONTRIBUTING.md](https://github.com/Pyre-bot/pyre-bot/blob/cloud/CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

To add functionality for other games or servers, add a new file in the **cogs** folder.

## Authors

* **Wade Fox** - [GitHub](https://github.com/InfernalPlacebo), [Discord](http://discord.pyre-bot.com)
* **Rayss** - [GitHub](https://github.com/SuperRayss), [Discord](http://discord.pyre-bot.com)

See also the list of [contributors](https://github.com/Pyre-bot/pyre-bot/graphs/contributors) who participated in this project.

## License

This project is licensed under the GPL-3.0 License - see the [LICENSE](LICENSE) file for details

## Changelog

### 0.10.0
* Moved chat to its on cog
* Server now posts updates to server update channel
* Created Server class
* **Finally** updated the README?

### 0.9.0
* These updates got lost somewhere :)

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
