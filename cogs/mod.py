import discord
from discord.ext import commands

class Moderation:
    """Bot commands for moderation."""
    def __init__(self, bot):
        self.bot = bot
        
    def find_user(self, user, ctx):
        found_member = ctx.guild.get_member(user)
        if not found_member:
            found_member = ctx.guild.get_member_named(user)
        if not found_member:
            try:
                found_member = ctx.message.mentions[0]
            except IndexError:
                pass
        return found_member

    @commands.has_permissions(kick_members=True)    
    @commands.command()
    async def kick(self, ctx, member, *, reason=""):
        """Kick a member."""
        found_member = self.find_user(member, ctx)
        if not found_member:
            await self.bot.say("That user could not be found.")
        else:
            if reason:
                reason_msg = "The given reason was: {}".format(reason)
            else:
                reason_msg = "No reason was given."
            try: 
                await found_member.send("You have been kicked by user {0.name}#{0.discriminator}.".format(ctx.author))
            except discord.errors.Forbidden:
                pass
            await found_member.ban()
            await ctx.send("Successfully kicked user {0.name}#{0.discriminator}!".format(found_member))
    
    @commands.has_permissions(ban_members=True)    
    @commands.command()
    async def ban(self, ctx, member, *, reason=""):
        """Ban a member."""
        found_member = self.find_user(member, ctx)
        if not found_member:
            await self.bot.say("That user could not be found.")
        else:
            if reason:
                reason_msg = "The given reason was: {}".format(reason)
            else:
                reason_msg = "No reason was given."
            try: 
                await found_member.send("You have been banned by user {0.name}#{0.discriminator}.".format(ctx.author))
            except discord.errors.Forbidden:
                pass
            await found_member.ban()
            await ctx.send("Successfully banned user {0.name}#{0.discriminator}!".format(found_member))

def setup(bot):
    bot.add_cog(Moderation(bot))
