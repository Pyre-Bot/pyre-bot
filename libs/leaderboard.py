from config.config import *


leaderboards = {}
lb_stats = ['Stages Completed', 'Kills', 'Time Alive', 'Purchases', 'Deaths', 'Items Collected', 'Gold Collected']


class Leaderboard:
    """
    Object container the leaderboard information for a given category.

    Methods
    -------
    __init__(category)
        Creates the leaderboard object.
    update()
        Updates the database with the new leaderboard information.
    only10()
        Ensures only 10 items are in the leaderboard.
    check(user, amt)
        Checks if the user's stats belong in the leaderboard and updates if they do.
    results()
        Returns the information needed to display the leaderboard.
    """
    def __init__(self, category):
        self.category = category
        self.entries = leaderboard_table.scan()
        self.ranks = None
        self.ranks_readable = None

        for entry in self.entries['Items']:
            if entry['Category'] == category:
                self.ranks = entry['Ranks']
                break

    async def update(self):
        """Updates the database with the new leaderboard information. """
        leaderboard_table.put_item(Item={
            'Category': self.category,
            'Ranks': self.ranks
        })

    async def only10(self):
        """Ensures only 10 items are in the leaderboard."""
        if len(self.ranks) > 10:
            remove = len(self.ranks) - 10
            ranks_temp = sorted(self.ranks.items(), key=lambda x: int(x[1]), reverse=True)
            while remove != 0:
                ranks_temp.pop()
                remove -= 1

            self.ranks = {}
            for item in ranks_temp:
                self.ranks[item[0]] = item[1]

            await self.update()

    async def check(self, user, amt):
        """Checks if the user's stats belong in the leaderboard and updates if they do.

        Parameters
        ----------
        user : int
            User's DiscordID
        amt : int
            The score of the user in the category.
        """
        if amt > int(min(self.ranks.values())):
            if str(user) in self.ranks.keys():
                if int(amt) > int(self.ranks[str(user)]):
                    self.ranks[str(user)] = str(amt)
                    await self.update()
            else:
                self.ranks[str(user)] = str(amt)
                await self.only10()

    async def results(self):
        """Returns the information needed to display the leaderboard."""
        ranks_temp = sorted(self.ranks.items(), key=lambda x: int(x[1]), reverse=True)
        self.ranks = {}
        for item in ranks_temp:
            self.ranks[item[0]] = item[1]

        return self.ranks
