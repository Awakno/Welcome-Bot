import discord
from discord.ext import tasks
from view.Config import ConfigView
from db.welcome import Welcome
from utils.variable import variable
from dotenv import load_dotenv
load_dotenv()
import os
bot = discord.Bot(intents=discord.Intents.all())
        
@bot.event
async def on_ready():
    print("Bot en ligne\n\n   - Serveur : {}\n   - Nom : {}\n   - ID : {}".format(len(bot.guilds),bot.user.name,bot.user.id))
    if not statut.is_running():
        statut.start()
@tasks.loop(seconds=5)
async def statut():
    statut = await Welcome().get_statut(bot.guilds[0].id)
    if statut and statut.get("text"):
        if statut.get("type"):
            if statut.get("type") == "playing":
                await bot.change_presence(activity=discord.Game(name=statut.get("text")))
            if statut.get("type") == "watching":
                await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=statut.get("text")))
            if statut.get("type") == "listening":
                await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=statut.get("text")))
            if statut.get("type") == "streaming":
                await bot.change_presence(activity=discord.Streaming(name=statut.get("text"), url="https://twitch.tv/x"))
        else:
            await bot.change_presence(activity=discord.Game(name=statut.get("text")))
        

        
@bot.slash_command(name="config",description="Configurer le bot")

async def config(ctx):
    if not ctx.author.guild_permissions.administrator:
        return await ctx.respond(embed=discord.Embed(title="Erreur",description="Vous n'avez pas la permission d'utiliser cette commande",color=discord.Color.red()))
    await ctx.respond(embed=discord.Embed(title="Configuration du bot",description="Cliquez sur le bouton pour configurer le bot",color=discord.Color.blue()),view=ConfigView(ctx.author,bot))
    
    
@bot.event
async def on_application_command_error(ctx, error):
    raise error
    

    
def convert_int(color):
    return int(color.lstrip('#'), 16)
    
async def made_embed(member):
    info = Welcome().get_embed(member.guild.id)
    
    info = info[0]
    if not info:
        return None
    embed = discord.Embed()
    embed.title = variable(info["title"],member,member.guild,bot) if info["title"] else None
    embed.set_author(name=variable(info["author"],member,member.guild,bot)) if info["author"] else None
    embed.description = variable(info["description"],member,member.guild,bot) if info["description"] else None
    embed.set_image(url=variable(info["image"],member,member.guild,bot)) if info["image"] else None
    embed.set_footer(text=variable(info["footer"],member,member.guild,bot)) if info["footer"] else None
    embed.set_thumbnail(url=variable(info["thumbnail"],member,member.guild,bot)) if info["thumbnail"] else None
    print(embed.thumbnail)
    embed.color = convert_int(info['color']) if info['color'] else convert_int("#000000")
    
    return embed
    
@bot.event
async def on_member_join(member):
    if Welcome().is_active(member.guild.id):
        embed = await made_embed(member)
        if embed:
            channel = member.guild.get_channel(await Welcome().get_channel(member.guild.id))
            if channel:
                try:
                    await channel.send(embed=embed)
                except Exception as e:
                    print(e)
                    await member.guild.system_channel.send(embed=discord.Embed(description="`❌ Un problème est survenu, contacter notre support afin d'obtenir des informations complémentaires`"))
            else:
                await member.guild.system_channel.send(embed=discord.Embed(description="`❌ Le salon de bienvenue n'est pas configuré`"))
                
        else:
            await member.guild.system_channel.send(embed=discord.Embed(description="`❌ Le message de bienvenue n'est pas bien configuré ou ne l'ai pas`"))
    
token = os.getenv("TOKEN") 
bot.run(token)