import a2s

servers = {}


class Server:
    def __init__(self, name, address, stage, stage_number, runtime, admin_channel, command_channel, chat_channel,
                 players, player_num, max_players):
        self.name = name
        self.address = address
        self.stage = stage
        self.stage_number = stage_number
        self.runtime = runtime
        self.admin_channel = admin_channel
        self.command_channel = command_channel
        self.chat_channel = chat_channel
        self.players = players
        self.player_num = player_num
        self.max_players = max_players

    async def info(self):
        server_info = a2s.info(self.address, 1.0)
        server_players = a2s.players(self.address)

        # Creates the string of player names used in the embed
        player_names = []
        for player in server_players:
            player_names.append(player.name)
        player_names = ("\n".join(map(str, player_names)))

        # Update server variables
        self.name = str(server_info.server_name)
        self.players = player_names
        self.player_num = server_info.player_count
        self.max_players = server_info.max_players

        return {"server_info": server_info, "server_players": server_players}
