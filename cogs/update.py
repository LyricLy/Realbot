import discord
import git

class Update:
    """Update the bot when there is a new push to it."""

    def __init__(self, bot):
        self.bot = bot
        self.git = git.cmd.Git(".")

    async def on_message(self, message):
        if message.channel == self.bot.update_channel:
            print("Pulling changes!")
            self.git.pull()
            print("Changes pulled!")

def setup(bot):
    bot.add_cog(Update(bot))
