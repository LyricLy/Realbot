import discord
from discord.ext import commands
import traceback

class Moderation:
    """Bot commands for moderation."""
    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(kick_members=True)    
    @commands.command()
    async def kick(self, ctx, member: discord.Member, *, reason=""):
        """Kick a member."""
        if reason:
            reason_msg = "The given reason was: {}".format(reason)
        else:
            reason_msg = "No reason was given."
        try:
            await member.send("You have been kicked by user {0.name}#{0.discriminator}.".format(ctx.author))
        except discord.errors.Forbidden:
            pass
        await member.kick(reason=reason if reason else None)
        await ctx.send("Successfully kicked user {0.name}#{0.discriminator}!".format(member))
    
    @commands.has_permissions(ban_members=True)    
    @commands.command()
    async def ban(self, ctx, member: discord.Member, *, reason=""):
        """Ban a member."""
        if reason:
            reason_msg = "The given reason was: {}".format(reason)
        else:
            reason_msg = "No reason was given."
        try:
            await member.send("You have been banned by user {0.name}#{0.discriminator}.".format(ctx.author))
        except discord.errors.Forbidden:
            pass
        await member.ban(delete_message_days=0, reason=reason if reason else None)
        await ctx.send("Successfully banned user {0.name}#{0.discriminator}!".format(member))

    async def __error(self, ctx, error):
        error = getattr(error, 'original', error)
        if isinstance(error, discord.ext.commands.errors.BadArgument):
            await ctx.send("That user could not be found.")
        elif isinstance(error, discord.ext.commands.errors.CheckFailure):
            await ctx.send("You don't have permission to use this command.")
        elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            formatter = commands.formatter.HelpFormatter()
            await ctx.send("You are missing required arguments.\n{}".format(formatter.format_help_for(ctx, ctx.command)[0]))
        else:
            if ctx.command:
                await ctx.send("An error occurred while processing the `{}` command.".format(ctx.command.name))
            print('Ignoring exception in command {0.command} in {0.message.channel}'.format(ctx))
            tb = traceback.format_exception(type(error), error, error.__traceback__)
            error_trace = "".join(tb)
            print(error_trace)
            embed = discord.Embed(description=error_trace.translate(self.bot.escape_trans))
            await self.bot.err_logs_channel.send("An error occurred while processing the `{}` command in channel `{}`.".format(ctx.command.name, ctx.message.channel), embed=embed)


def setup(bot):
    bot.add_cog(Moderation(bot))
