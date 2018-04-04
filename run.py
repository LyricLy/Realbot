import discord
from discord.ext import commands
import traceback

bot = commands.Bot(command_prefix=",", description="It's a real bot.")

@bot.event
async def on_ready():
    print("Realbot active.")
    print("{}#{}".format(bot.user.name, bot.user.discriminator))
    print("------------------------")
    for guild in bot.guilds:
        bot.mod_role = discord.utils.get(guild.roles, name="Mods")
        bot.muted_role = discord.utils.get(guild.roles, name="No-Speak")

        bot.update_channel = discord.utils.get(guild.channels, name="bot_updates")
        bot.err_logs_channel = discord.utils.get(guild.channels, name="error_logs")

bot.escape_trans = str.maketrans({
    "*": "\*",
    "_": "\_",
    "~": "\~",
    "`": "\`",
    "\\": "\\\\"
})

# mostly taken from https://github.com/Rapptz/discord.py/blob/async/discord/ext/commands/bot.py
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        pass  # ...don't need to know if commands don't exist
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
        embed = discord.Embed(description=error_trace.translate(bot.escape_trans))
        await bot.err_logs_channel.send("An error occurred while processing the `{}` command in channel `{}`.".format(ctx.command.name, ctx.message.channel), embed=embed)


@bot.event
async def on_error(event_method, *args, **kwargs):
    if isinstance(args[0], commands.errors.CommandNotFound):
        return
    print("Ignoring exception in {}".format(event_method))
    tb = traceback.format_exc()
    error_trace = "".join(tb)
    print(error_trace)
    embed = discord.Embed(description=error_trace.translate(bot.escape_trans))
    await bot.err_logs_channel.send("An error occurred while processing `{}`.".format(event_method), embed=embed)

addons = [
    'cogs.slowmode',
]

failed_addons = []

for extension in addons:
    try:
        bot.load_extension(extension)
    except Exception as e:
        print('{} failed to load.\n{}: {}'.format(extension, type(e).__name__, e))
        failed_addons.append([extension, type(e).__name__, e])

with open("token.txt") as f:
    token = f.read()

bot.run(token)
