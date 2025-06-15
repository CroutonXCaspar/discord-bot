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


@bot.tree.command(name="blague", description="Affiche une blague aléatoire")
async def blague(interaction: discord.Interaction):
    blagues = [
        "Pourquoi les plongeurs plongent-ils toujours en arrière et jamais en avant ? Parce que sinon ils tombent dans le bateau.",
        "Quel est le comble pour un électricien ? De ne pas être au courant.",
        "Pourquoi les canards sont-ils toujours à l'heure ? Parce qu'ils sont dans l'étang."
    ]
    await interaction.response.send_message(random.choice(blagues))

@bot.tree.command(name="roll", description="Lance un dé à 6 faces")
async def roll(interaction: discord.Interaction):
    resultat = random.randint(1, 6)
    await interaction.response.send_message(f"🎲 Vous avez obtenu : {resultat}")

@bot.tree.command(name="citation", description="Affiche une citation inspirante")
async def citation(interaction: discord.Interaction):
    citations = [
        "Le succès, c'est tomber sept fois, se relever huit. - Proverbe japonais",
        "La vie, c'est comme une bicyclette, il faut avancer pour ne pas perdre l'équilibre. - Albert Einstein",
        "Faites de votre vie un rêve, et d'un rêve, une réalité. - Antoine de Saint-Exupéry"
    ]
    await interaction.response.send_message(random.choice(citations))

@bot.tree.command(name="avatar", description="Affiche l'avatar d'un utilisateur")
async def avatar(interaction: discord.Interaction, membre: discord.Member):
    await interaction.response.send_message(f"L'avatar de {membre.mention} : {membre.avatar.url}")


@bot.tree.command(name="sondage", description="Crée un sondage simple")
async def sondage(interaction: discord.Interaction, question: str):
    # Vérifie si l'utilisateur a la permission de gérer les messages
    if not interaction.user.guild_permissions.manage_messages:
        await interaction.response.send_message(
            "❌ Vous n'avez pas la permission de créer un sondage.", ephemeral=True
        )
        return

    # Envoie le sondage
    message = await interaction.response.send_message(f"📊 **Sondage** : {question}")
    # Ajoute des réactions pour le sondage
    message = await interaction.original_response()
    await message.add_reaction("👍")
    await message.add_reaction("👎")


@bot.tree.command(name="pfc", description="Joue à Pierre-Feuille-Ciseaux avec le bot")
async def pfc(interaction: discord.Interaction, choix: str):
    options = ["pierre", "feuille", "ciseaux"]
    bot_choix = random.choice(options)
    if choix not in options:
        await interaction.response.send_message("Choisissez entre : pierre, feuille ou ciseaux.")
        return

    if choix == bot_choix:
        resultat = "Égalité !"
    elif (choix == "pierre" and bot_choix == "ciseaux") or \
         (choix == "feuille" and bot_choix == "pierre") or \
         (choix == "ciseaux" and bot_choix == "feuille"):
        resultat = "Vous avez gagné ! 🎉"
    else:
        resultat = "Le bot a gagné ! 😢"

    await interaction.response.send_message(f"Vous avez choisi : {choix}\nLe bot a choisi : {bot_choix}\n**{resultat}**")
    
    

bot.run(os.getenv('DISCORD_TOKEN'))
