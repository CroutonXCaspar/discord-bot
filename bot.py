import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from datetime import datetime
import random
import requests
load_dotenv()


print("Lancement du bot")
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
BOT_VERSION = "1.0.1"

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

@bot.tree.command(name="warnguy", description="Alerter une personne")
async def warnguy(interaction: discord.Interaction, member: discord.Member, reason: str):
    print(f"Commande exécutée pour {member.name} avec la raison : {reason}")
    try:
        await member.send(f"Tu as une alerte : {reason}")
        await interaction.response.send_message(f"Alerte envoyée à {member.mention}.")
    except Exception as e:
        print(f"Erreur : {e}")
        await interaction.response.send_message(f"❌ Impossible d'envoyer une alerte à {member.mention}.", ephemeral=True)

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

@bot.tree.command(name="userinfo", description="Affiche des informations sur un utilisateur")
async def userinfo(interaction: discord.Interaction, membre: discord.Member):
        embed = discord.Embed(
            title=f"Informations sur {membre.name}",
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=membre.avatar.url)
        embed.add_field(name="Nom d'utilisateur", value=membre.name, inline=True)
        embed.add_field(name="ID", value=membre.id, inline=True)
        embed.add_field(name="Créé le", value=membre.created_at.strftime("%d/%m/%Y à %H:%M:%S"), inline=False)
        embed.add_field(name="Rejoint le serveur le", value=membre.joined_at.strftime("%d/%m/%Y à %H:%M:%S"), inline=False)
        embed.set_footer(text="Commande exécutée par " + interaction.user.name)

        await interaction.response.send_message(embed=embed)

@bot.tree.command(name="clear", description="Supprime un certain nombre de messages dans le salon.")
@commands.has_permissions(manage_messages=True)
async def clear(interaction: discord.Interaction, nombre: int):
    if nombre <= 0:
        await interaction.response.send_message("❌ Le nombre de messages à supprimer doit être supérieur à 0.", ephemeral=True)
        return

    # Supprime les messages
    try:
        deleted = await interaction.channel.purge(limit=nombre)
        await interaction.response.send_message(f"✅ {len(deleted)} messages ont été supprimés.", ephemeral=True)
    except Exception as e:
        print(f"Erreur lors de la suppression des messages : {e}")
        await interaction.response.send_message("❌ Une erreur s'est produite lors de la suppression des messages.", ephemeral=True)


@bot.tree.command(name="serverinfo", description="Affiche des informations sur le serveur")
async def serverinfo(interaction: discord.Interaction):
    guild = interaction.guild  # Récupère les informations du serveur
    embed = discord.Embed(
        title=f"Informations sur le serveur : {guild.name}",
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url=guild.icon.url if guild.icon else None)  # Affiche l'icône du serveur s'il y en a une
    embed.add_field(name="Nom du serveur", value=guild.name, inline=True)
    embed.add_field(name="ID du serveur", value=guild.id, inline=True)
    embed.add_field(name="Propriétaire", value=guild.owner.mention, inline=True)
    embed.add_field(name="Nombre de membres", value=guild.member_count, inline=True)
    embed.add_field(name="Créé le", value=guild.created_at.strftime("%d/%m/%Y à %H:%M:%S"), inline=False)
    embed.set_footer(text=f"Commande exécutée par {interaction.user.name}")

    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="messagecount", description="Affiche le nombre total de messages dans le salon.")
async def messagecount(interaction: discord.Interaction):
    try:
        # Vérifie si le salon est valide
        if not interaction.channel:
            await interaction.response.send_message("❌ Impossible de récupérer les messages dans ce contexte.")
            return

        # Compte les messages dans le salon
        total_messages = 0
        async for message in interaction.channel.history(limit=None):
            total_messages += 1

        await interaction.response.send_message(f"📊 Le salon contient **{total_messages}** messages.")
    except Exception as e:
        print(f"Erreur lors de la récupération des messages : {e}")
        await interaction.response.send_message("❌ Une erreur s'est produite lors de la récupération des messages.")


@bot.tree.command(name="math", description="Effectue un calcul mathématique simple")
async def math(interaction: discord.Interaction, operation: str, a: float, b: float):
    try:
        if operation == "addition":
            result = a + b
        elif operation == "soustraction":
            result = a - b
        elif operation == "multiplication":
            result = a * b
        elif operation == "division":
            if b == 0:
                await interaction.response.send_message("❌ Division par zéro impossible.", ephemeral=True)
                return
            result = a / b
        else:
            await interaction.response.send_message("❌ Opération invalide. Choisissez entre : addition, soustraction, multiplication, division.", ephemeral=True)
            return

        await interaction.response.send_message(f"✅ Résultat de {operation} entre {a} et {b} : **{result}**")
    except Exception as e:
        print(f"Erreur lors du calcul : {e}")
        await interaction.response.send_message("❌ Une erreur s'est produite lors du calcul.", ephemeral=True)


@bot.tree.command(name="weather", description="Affiche la météo d'une ville")
async def weather(interaction: discord.Interaction, ville: str):
    try:
        # Remplacez "VOTRE_API_KEY" par votre clé API OpenWeatherMap
        api_key = "VOTRE_API_KEY"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={ville}&appid={api_key}&units=metric&lang=fr"

        response = requests.get(url)
        data = response.json()

        if data["cod"] != 200:
            await interaction.response.send_message(f"❌ Ville introuvable : {ville}.", ephemeral=True)
            return

        # Récupère les informations météo
        nom_ville = data["name"]
        temperature = data["main"]["temp"]
        description = data["weather"][0]["description"]
        humidite = data["main"]["humidity"]
        vent = data["wind"]["speed"]

        # Crée un embed pour afficher les informations
        embed = discord.Embed(
            title=f"Météo à {nom_ville}",
            color=discord.Color.blue()
        )
        embed.add_field(name="🌡️ Température", value=f"{temperature}°C", inline=True)
        embed.add_field(name="🌤️ Description", value=description.capitalize(), inline=True)
        embed.add_field(name="💧 Humidité", value=f"{humidite}%", inline=True)
        embed.add_field(name="🌬️ Vent", value=f"{vent} m/s", inline=True)
        embed.set_footer(text="Source : OpenWeatherMap")

        await interaction.response.send_message(embed=embed)
    except Exception as e:
        print(f"Erreur lors de la récupération de la météo : {e}")
        await interaction.response.send_message("❌ Une erreur s'est produite lors de la récupération de la météo.", ephemeral=True)


@bot.tree.command(name="help", description="Affiche la liste des commandes disponibles")
async def help_command(interaction: discord.Interaction):
    commandes = [
        {"nom": "credit", "description": "Voir mes créateurs."},
        {"nom": "ping", "description": "Voir le ping du bot."},
        {"nom": "support", "description": "Vous envoie au serveur support."},
        {"nom": "warnguy", "description": "Alerter une personne."},
        {"nom": "banguy", "description": "Bannir une personne."},
        {"nom": "blague", "description": "Affiche une blague aléatoire."},
        {"nom": "roll", "description": "Lance un dé à 6 faces."},
        {"nom": "citation", "description": "Affiche une citation inspirante."},
        {"nom": "avatar", "description": "Affiche l'avatar d'un utilisateur."},
        {"nom": "sondage", "description": "Crée un sondage simple."},
        {"nom": "pfc", "description": "Joue à Pierre-Feuille-Ciseaux avec le bot."},
        {"nom": "time", "description": "Affiche l'heure actuelle."},
        {"nom": "userinfo", "description": "Affiche des informations sur un utilisateur."},
        {"nom": "version", "description": "Affiche la version actuelle du bot."},
        {"nom": "clear", "description": "Supprime un certain nombre de messages dans le salon."},
        {"nom": "help", "description": "Affiche la liste des commandes disponibles."},
        {"nom": "youtube", "description": "T'emmène sur Youtube."},
        {"nom": "serverinfo", "description": "Affiche des informations sur le serveur."},
        {"nom": "messagecount", "description": "Affiche le nombre total de messages dans le salon."},
        {"nom": "math", "description": "Effectue un calcul mathématique simple (addition, soustraction, multiplication, division)."},
        {"nom": "weather", "description": "Affiche la météo d'une ville."}
    ]

    embed = discord.Embed(
        title="Liste des commandes disponibles",
        description="Voici toutes les commandes que vous pouvez utiliser avec ce bot.",
        color=discord.Color.green()
    )

    for commande in commandes:
        embed.add_field(name=f"/{commande['nom']}", value=commande['description'], inline=False)

    embed.set_footer(text=f"Version du bot : {BOT_VERSION}")
    await interaction.response.send_message(embed=embed)


bot.run(os.getenv('DISCORD_TOKEN'))