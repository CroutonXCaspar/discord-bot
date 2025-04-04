import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from datetime import datetime
load_dotenv()


print("Lancement du bot")
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f"{bot.user} est prêt !")
    # Synchroniser les commandes
    try:
        #sync 
        synced = await bot.tree.sync()
        print(f"Commandes slash synchronisees : {len(synced)}")
    except Exception as e:
        print(e)

@bot.event
async def on_message(message: discord.Message):
    # empecher le bot de se declencher lui meme
    if message.author.bot:
        return

    if message.content.lower() == 'bonjour':
        channel = message.channel
        author = message.author
        await author.send("Comment tu vas ?")
    if message.content.lower() == "bienvenue":
        welcome_channel = bot.get_channel(1336073367349891174)
        await welcome_channel.send("Bienvenue")

@bot.tree.command(name="credit", description="voir mes createurs")
async def credit(interaction: discord.Interaction):
    embed = discord.Embed(
        title="developpeur",
        description="Voici mes createurs",
        color=discord.Color.blue()
    )
    embed.add_field(name="Wacky Sushi", value="Voici son discord : woah12300", inline=False)
    embed.set_footer(text="Pied de page")
    embed.set_image(url="")

    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="ping", description="voir le ping du bot")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong! {round(bot.latency * 1000)}ms")

@bot.tree.command(name="support", description="Vous envoie au serveur support")
async def support(interaction: discord.Interaction):
    await interaction.response.send_message("Voici le lien du serveur support: https://discord.gg/3Gh6wbC9zw")

@bot.tree.command(name="warnguy", description="Aleerter une personne")
async def banguy(interaction: discord.Interaction, member: discord.Member, reason: str):
    await interaction.response.send_message("Alerte envoye")
    await member.send("Tu as une alerte")

@bot.tree.command(name="banguy", description="Bannir une personne")
async def warnguy(interaction: discord.Interaction, member: discord.Member, reason: str):
    await interaction.response.send_message("Ban envoye")
    await member.ban(reason=reason)
    await member.send("Tu as ete banni")

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, raison="Aucune raison spécifiée"):
    await member.kick(reason=raison)
    await ctx.send(f"{member.mention} a été expulsé pour : {raison}")


@bot.tree.command(name="youtube", description="t'emmene sur Youtube")
async def youtube(interaction: discord.Interaction):
    await interaction.response.send_message("Voici le lien de Youtube: https://www.youtube.com/")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.lower() == "gg":
        await message.add_reaction("👍")
    await bot.process_commands(message)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.lower() == "hello":
        await message.add_reaction("👋")
    await bot.process_commands(message)

@bot.tree.command(name="time", description="pour savoir l'heure")
async def heure(interaction: discord.Interaction):
    now = datetime.now().strftime("%H:%M:%S")
    await interaction.response.send_message(f"Il est {now}")
    
    

bot.run(os.getenv('DISCORD_TOKEN'))