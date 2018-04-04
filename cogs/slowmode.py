import discord
from discord.ext import commands
import time
import asyncio

class Slowmode:
    """A cog for slowmode."""

    def __init__(self, bot):
        self.bot = bot
        self.targets = {}

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def add_slowmode(self, ctx, *, args):
        members = []
        for arg in args.split():
            member = ctx.guild.get_member(int(arg))
            self.targets[member] = [0, 0.0]
            members.append(str(member))
        await ctx.send("Successfully added {} to the list of slowmoded members.".format(", ".join(members)))

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def remove_slowmode(self, ctx, *, args):
        members = []
        for arg in args.split():
            member = ctx.guild.get_member(int(arg))
            self.targets.pop(member)
            members.append(str(member))
        await ctx.send("Successfully removed {} from the list of slowmoded members.".format(", ".join(members)))

    async def on_message(self, message):
        if message.author in self.targets:
            self.targets[message.author][0] += len(message.content) * self.targets[message.author][1]
            self.targets[message.author][1] += 0.25
            if self.targets[message.author][0]:
                await message.author.add_roles(self.bot.muted_role)

    async def loop(self):
        while True:
            for target in self.targets:
                if self.targets[target][0]:
                    self.targets[target][0] -= 1
                if self.targets[target][1]:
                    self.targets[target][1] -= 0.01
                if self.targets[target][1] < 0:
                    self.targets[target][1] = 0
                if self.targets[target][0] < 0:
                    self.targets[target][0] = 0
                if self.bot.muted_role in target.roles and not self.targets[target][0]:
                    await target.remove_roles(self.bot.muted_role)
            await asyncio.sleep(1) 

def setup(bot):
    t = Slowmode(bot)
    loop = asyncio.get_event_loop()
    loop.create_task(t.loop())
    bot.add_cog(t)
