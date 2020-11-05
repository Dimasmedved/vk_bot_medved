import discord
from discord.ext import commands
import os
PRIFIX="."
client=commands.Bot(command_prefix=PRIFIX)

#команды



@client.command()
async def бета(ctx,member: discord.Member,amout=1):
        await ctx.channel.purge(limit=amout)
        await ctx.author.send("Привет теперь ты попал в конкурс" + "\n" + "держи ссылку на саму игру: " + "https://yadi.sk/d/uoPHL2wck4Uc7g" + "\n" + "и удачи тебе")
        await member.add_roles(member.guild.get_role(773474507796774912))





 token=os.environ.get("TOKEN")
 client.run(str(token))
