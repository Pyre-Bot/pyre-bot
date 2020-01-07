import valve.source.a2s

SERVER_ADDRESS = ('ror2.infernal.wtf', 27016)

with valve.source.a2s.ServerQuerier(SERVER_ADDRESS) as server:
    info = server.info()
    players = server.players()
    ping = server.ping()

print("{player_count}/{max_players} {server_name}".format(**info))
for player in sorted(players["players"],
                     key=lambda p: p["score"], reverse=True):
    print("{name}".format(**player))
print("\nServer ping is {:n}.".format(ping))
