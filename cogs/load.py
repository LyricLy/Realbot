import discord
import os
from discord.ext import commands

class Load:
    """Load commands."""

    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(ban_members=True)
    @commands.command(hidden=True)
    async def load(self, ctx, *, module):
        """Loads an addon."""
        try:
            if module[0:5] != "cogs.":
                module = "cogs." + module
            self.bot.load_extension(module)
            await ctx.send(':white_check_mark: Extension loaded.')
        except Exception as e:
            await ctx.send(':anger: Failed!\n```\n{}: {}\n```'.format(type(e).__name__, e))

    @commands.has_permissions(ban_members=True)
    @commands.command(hidden=True)
    async def unload(self, ctx, *, module):
        """Unloads an addon."""
        try:
            if module[0:5] != "cogs.":
                module = "cogs." + module
            if module == "cogs.load":
                await self.bot.say(":exclamation: I don't think you want to unload that!")
            else:
                self.bot.unload_extension(module)
                await ctx.send(':white_check_mark: Extension unloaded.')
        except Exception as e:
            await ctx.send(':anger: Failed!\n```\n{}: {}\n```'.format(type(e).__name__, e))

    @commands.has_permissions(ban_members=True)
    @commands.command(name='reload', hidden=True)
    async def _reload(self, ctx, *, module):
        """Reloads an addon."""
        try:
            if module[0:5] != "cogs.":
                module = "cogs." + module
            self.bot.unload_extension(module)
            self.bot.load_extension(module)
            await ctx.send(':white_check_mark: Extension reloaded.')
        except Exception as e:
            await ctx.send(':anger: Failed!\n```\n{}: {}\n```'.format(type(e).__name__, e))

    @commands.has_permissions(ban_members=True)
    @commands.command()
    async def restart(self, ctx):
        """Restart the bot."""
        await ctx.send("Restarting...")
        os.system("run.py")

def setup(bot):
    bot.add_cog(Load(bot))
