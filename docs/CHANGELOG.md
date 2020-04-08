## Changelog

### 0.8.0
* Moved all stat tracking to Amazon DynamoDB for a better experience
* Custom version of the Pygtail module is now packaged with the bot
* Fixed an exception that occurred when the bot reconnected to Discord servers.
* Complete rewrite of setup.py
* Updated all requirements to newest versions
* Various fixes, improvements, and optimizations that makes everyone's lives better

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
* Added Cogs
    * Added cogs to the code to provide expandable in future releases and allow cleaner reading and writing of code.
    * Cogs allow development and test of features and changes without having to completely restart bot.
