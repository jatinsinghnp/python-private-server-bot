import discord
from dotenv import load_dotenv
import os
from discord.ext import commands

#intents 
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


#.env settings 
import replicate
load_dotenv()
TOKEN=os.environ.get("TOKEN")



#active status
@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


#user message 
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(".hello"):
        await message.channel.send(f"hello {message.author}")
    if message.content[0] == "?":
        await message.channel.send(f"hi,{message.author}")


#user join 
@client.event
async def on_member_join(member):
    welcome_channel = client.get_channel(1010188442048663625)
    print(f"{member} has join ")
    await welcome_channel.send(f"{member.mention} has join server ! thank you ")
    try:
        await member.send(f"hey{member.display_name} thank you for joining the server ")
    except:
        await welcome_channel.send(f"{member.mention} I cant dm you ,but thanks for  joining")


#user remove
@client.event
async def on_member_remove(member):
    welcome_channel = client.get_channel(1010188442048663625)
    print(f"{member} has join ")
    await welcome_channel.send(f"{member.mention} has left the the server  ! sob: ")
    try:
        await member.send(f"hey{member.display_name} goobye  ")
    except:
        await welcome_channel.send(f"{member.mention} I can't dm you ,goodbye")
        
#bot command         

bot = commands.Bot(
    command_prefix="!",
    description="Runs models on Replicate!",
    intents=intents,
)

@bot.command()
async def make(ctx, *, prompt):
    """Generate an image from a text prompt using the stable-diffusion model"""
    msg = await ctx.send(f"“{prompt}”\n> Generating...")

    model = replicate.models.get("stability-ai/stable-diffusion")
    image = model.predict(prompt=prompt)[0]

    await msg.edit(content=f"“{prompt}”\n{image}")



bot.run(TOKEN)

client.run(TOKEN)
