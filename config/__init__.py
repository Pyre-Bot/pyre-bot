"""This submodule contains the configuration information used throughout the bot.

Configuration information is passed through as environment variables to control the bot and allow easy updating
without anything being hardcoded. The dockerfile uses config.py, if you are running the bot outside of a docker
container you need to include a ``.env`` file and use config_env.py instead.

"""
