# InfernalGaming Discord Bot

This Discord bot was created primarily to be used by the InfernalGaming server to manage game servers and add other functionality to the server that wasn't available elsewhere or could be improved upon to serve the community.

## Getting Started

These instructions will help make sure your system is ready to run the bot and help you get started using it for your needs.

### Prerequisites

The bot is built upon Python 3.8 but has been tested working with Python 3.7 without any issues. The dependencies for the usage are updated regularly in the requirements.txt file and these can be installed via:

```
pip install -r requirements.txt
```

As of writing the current requirements are:

```
psutil==5.6.7
discord.py==1.2.5
cassiopeia==4.0.8
python_valve==0.2.1
discord==1.0.1
python-dotenv==0.10.3
valve==0.0.0
```

### Installing

Clone the repo to wherever you want the bot to reside. You can run the bot by calling bot.py. You will also need [SteamCMD](https://developer.valvesoftware.com/wiki/SteamCMD) installed on your machine to run the updates for the game servers.

#### API Tokens
You need to get API tokens from the [Discord Developer Portal](https://discordapp.com/developers/docs/intro) and [Riot Developer Portal](https://developer.riotgames.com/) to use those respective functions of the bot.

After cloning, create a file called ".env" in the same directory as bot.py, this will store your API tokens called by the bot. The .env file should look similar to this:

```
# .env
DISCORD_TOKEN="YOUR-DISCORD-TOKEN"
RIOT_TOKEN="YOUR-RIOT-TOKEN"
```

*Never upload online or share your .env file to anyone you do not trust. These API keys are private and can result in your access from the services being removed if they get out.*

## Running and using the bot

After adding the API keys and creating a .env file you can get started by running the bot.py file located in the main directory. The bot will output a message stating that it is connected to Discord and ready to listen when it starts. Once you get the confirmation message you are able to start issuing commands to your bot using one of the command prefixes ('r!', 'ig!', '>').

### Bot Commands

* start : Starts the specified server, by default Risk of Rain 2
* stop : Stops the specified server, by default Risk of Rain 2
* update : Updates the specified server, by default Risk of Rain 2
* status : Lists the game server status riot Steamworks API
* mods : Outputs a list of mods to chat
* link : Outputs the Steam connect link to chat
* config : Outputs the current server config to chat

#### Modifying the commands

By default the bot is configured to manage a Risk of Rain 2 server. This can be changed by calling the executables for other servers and pointing the checks at their respective logs.

## Built With

* [Discord.py](https://github.com/Rapptz/discord.py) - Discord API wrapper for Python
* [Python-valve](https://github.com/serverstf/python-valve) - Steamworks API wrapper for Python
* [Cassiopeia](https://github.com/meraki-analytics/cassiopeia) - Riot Games API wrapper for Python

## Contributing

**Coming Soon**
Please read [CONTRIBUTING.md](https://github.com/InfernalPlacebo/ig-bot) for details on our code of conduct, and the process for submitting pull requests to us.

## Authors

* **Wade Fox** - *Creator* - [GitHub](https://github.com/InfernalPlacebo)

See also the list of [contributors]https://github.com/InfernalPlacebo/ig-bot/graphs/contributors) who participated in this project.

## License

This project is licensed under the GPL-3.0 License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Everyone in the [Discord](https://discord.gg/YewZwpc) server helping test and recommend features
