import discord
from discord.ui.item import Item
from db.welcome import Welcome
import asyncio
class WelcomeConfigView(discord.ui.View):
    def __init__(self, author,bot):
        super().__init__(timeout=180)
        self.author = author
        self.bot = bot
        
        if Welcome().is_active(self.author.guild.id):
            self.btn = discord.ui.Button(label="Activer",emoji="✅",style=discord.ButtonStyle.green,custom_id="active")
        else:
            self.btn = discord.ui.Button(label="Désactiver",emoji="✖️",style=discord.ButtonStyle.red,custom_id="active")
        self.btn.callback = self.is_active_btn
        self.add_item(self.btn)
    
    async def check_interaction(self, interaction: discord.Interaction):
        if not self.author == interaction.user:
            return await interaction.response.send_message("Vous n'avez pas le droit d'effectuer cette action", ephemeral=True)
        else:
            return True
    
    async def is_active_btn(self, interaction: discord.Interaction):
        await Welcome().set_active(interaction.guild.id)
        await interaction.response.edit_message(view=WelcomeConfigView(self.author,self.bot))
    @discord.ui.button(label="Configurer le salon",emoji="📥",style=discord.ButtonStyle.green,custom_id="welcomeConfig")
    async def welcomeConfig(self, button: discord.ui.Button, interaction: discord.Interaction):
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view=self)
        await interaction.response.send_message(embed=discord.Embed().set_author(name="Mentionnez le salon"))
        message = await interaction.original_response()
        try:
            channel_response = await self.bot.wait_for("message", check=lambda m: m.author == self.author and m.channel == message.channel,timeout=30)
            if channel_response:
                id = (channel_response.content.split("#")[1]).split(">")[0]
                
                channel = self.bot.get_channel(int(id))
                
                if channel:
                    await Welcome().set_channel(interaction.guild.id, channel.id)
                    
                    await channel_response.delete()
                    for child in self.children:
                        child.disabled = False
                    await interaction.message.edit(view=self)
                    await message.edit(embed=discord.Embed(description="`✅ Le salon de bienvenue a bien été mis à jour`"))
                    await asyncio.sleep(2)
                    await message.delete()
                else:
                    await channel_response.delete()
                    await message.edit(embed=discord.Embed(description="`❌ Salon invalide, action annulée`"))
                    
                    await asyncio.sleep(2)
                    await message.delete()
                    
            else:
                await message.edit(embed=discord.Embed(description="`❌ Salon invalide, action annulée`"))
                await channel_response.delete()
                await asyncio.sleep(2)
                await message.delete()
                
        except asyncio.TimeoutError:
            
            await message.edit(embed=discord.Embed(description="`❌ Salon invalide, action annulée`"))
            await asyncio.sleep(2)
            await message.delete()
    @discord.ui.button(label="Configurer le message",emoji="📝",style=discord.ButtonStyle.green,custom_id="welcomeMessage")
    async def welcomeMessage(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.edit_message(view=ConfigMessage(self.author,self.bot))
        
class ConfigMessage(discord.ui.View):
    def __init__(self,author,bot):
        super().__init__(timeout=180)
        self.author = author
        self.bot = bot
        self.btn = [{"label": "Titre"},{"label": "Description"},{"label": "Pied de page"},{"label": "Couleur"},{"label": "Image"},{"label": "Vignette"},{"label": "Auteur"}]
        for i in self.btn:
            self.bouton = discord.ui.Button(label=i["label"],style=discord.ButtonStyle.secondary,custom_id=i["label"])
            self.bouton.callback = self.btn_callback
            self.add_item(self.bouton) 
    async def check_interaction(self, interaction: discord.Interaction):
        if not self.author == interaction.user:
            return await interaction.response.send_message("Vous n'avez pas le droit d'effectuer cette action", ephemeral=True)
        else:
            return True
    
    async def btn_callback(self, interaction: discord.Interaction):
        if interaction.data["custom_id"] == "Titre":
            for child in self.children:
                child.disabled = True
            
            await interaction.message.edit(view=self)
            await interaction.response.send_message(embed=discord.Embed().set_author(name="Configurer le titre"))
            message = await interaction.original_response()
            try:
                title = await self.bot.wait_for("message", check=lambda m: m.author == self.author and m.channel == interaction.channel,timeout=30)
                if title:
                    await Welcome().config_message(interaction.guild.id,title=title.content)
                    await title.delete()
                    await message.edit(embed=discord.Embed(description="`✅ Le titre a bien été mis à jour`"))
                    await asyncio.sleep(2)
                    await message.delete()
            except TimeoutError:
                await message.edit(embed=discord.Embed(description="`❌ Le titre n'a pas pu être mis à jour`"))
                await asyncio.sleep(2)
                await message.delete()
        if interaction.data["custom_id"] == "Description":
            for child in self.children:
                child.disabled = True
            await interaction.message.edit(view=self)
            await interaction.response.send_message(embed=discord.Embed().set_author(name="Configurer la description"))
            message = await interaction.original_response()
            try:
                description = await self.bot.wait_for("message", check=lambda m: m.author == self.author and m.channel == interaction.channel,timeout=30)
                if description:
                    await Welcome().config_message(interaction.guild.id,description=description.content)
                    await description.delete()
                    await message.edit(embed=discord.Embed(description="`✅ La description a bien été mise à jour`"))
                    await asyncio.sleep(2)
                    await message.delete()
            except TimeoutError:
                await message.edit(embed=discord.Embed(description="`❌ Le titre n'a pas pu être mis à jour`"))
                await asyncio.sleep(2)
                await message.delete()
        if interaction.data["custom_id"] == "Pied de page":
            for child in self.children:
                child.disabled = True
            
            await interaction.message.edit(view=self)
            await interaction.response.send_message(embed=discord.Embed().set_author(name="Configurer le pied de page"))
            message = await interaction.original_response()
            try:
                footer = await self.bot.wait_for("message", check=lambda m: m.author == self.author and m.channel == interaction.channel,timeout=30)
                if footer:
                    await Welcome().config_message(interaction.guild.id,footer=footer.content)
                    await footer.delete()
                    await message.edit(embed=discord.Embed(description="`✅ Le pied de page a bien été mis à jour`"))
                    await asyncio.sleep(2)
                    await message.delete()
            except TimeoutError:
                await message.edit(embed=discord.Embed(description="`❌ Le pied de page n'a pas pu être mis à jour`"))
                await asyncio.sleep(2)
                await message.delete()
        if interaction.data["custom_id"] == "Couleur":
            for child in self.children:
                child.disabled = True
            await interaction.message.edit(view=self)
            await interaction.response.send_message(embed=discord.Embed().set_author(name="Configurer la couleur"))
            message = await interaction.original_response()
            try:
                color = await self.bot.wait_for("message", check=lambda m: m.author == self.author and m.channel == interaction.channel,timeout=30)
                if color:
                    await Welcome().config_message(interaction.guild.id,color=color.content)
                    await color.delete()
                    await message.edit(embed=discord.Embed(description="`✅ La couleur a bien été mise à jour`"))
                    await asyncio.sleep(2)
                    await message.delete()
            except TimeoutError:
                await message.edit(embed=discord.Embed(description="`❌ La couleur n'a pas pu être mise à jour`"))
                await asyncio.sleep(2)
                await message.delete()
        if interaction.data["custom_id"] == "Image":
            for child in self.children:
                child.disabled = True
            await interaction.message.edit(view=self)
            await interaction.response.send_message(embed=discord.Embed().set_author(name="Configurer l'image (Format lien !)"))
            message = await interaction.original_response()
            try:
                image = await self.bot.wait_for("message", check=lambda m: m.author == self.author and m.channel == interaction.channel,timeout=30)
                if image:
                    await Welcome().config_message(interaction.guild.id,image=image.content)
                    await image.delete()
                    await message.edit(embed=discord.Embed(description="`✅ L'image a bien été mise à jour`"))
                    await asyncio.sleep(2)
                    await message.delete()
            except TimeoutError:
                await message.edit(embed=discord.Embed(description="`❌ L'image n'a pas pu être mise à jour`"))
                await asyncio.sleep(2)
                await message.delete()
                
        if interaction.data["custom_id"] == "Vignette":
            for child in self.children:
                child.disabled = True
            await interaction.message.edit(view=self)
            await interaction.response.send_message(embed=discord.Embed().set_author(name="Configurer la vignette (Format lien !)"))
            message = await interaction.original_response()
            try:
                image = await self.bot.wait_for("message", check=lambda m: m.author == self.author and m.channel == interaction.channel,timeout=30)
                if image:
                    await Welcome().config_message(interaction.guild.id,thumbnail=image.content)
                    await image.delete()
                    await message.edit(embed=discord.Embed(description="`✅ L'image a bien été mise à jour`"))
                    await asyncio.sleep(2)
                    await message.delete()
            except TimeoutError:
                await message.edit(embed=discord.Embed(description="`❌ L'image n'a pas pu être mise à jour`"))
                await asyncio.sleep(2)
                await message.delete()
        if interaction.data["custom_id"] == "Auteur":
            for child in self.children:
                child.disabled = True
            await interaction.message.edit(view=self)
            await interaction.response.send_message(embed=discord.Embed().set_author(name="Configurer l'auteur"))
            message = await interaction.original_response()
            try:
                author = await self.bot.wait_for("message", check=lambda m: m.author == self.author and m.channel == interaction.channel,timeout=30)
                if author:
                    await Welcome().config_message(interaction.guild.id,author=author.content)
                    await author.delete()
                    await message.edit(embed=discord.Embed(description="`✅ L'auteur a bien été mis à jour`"))
                    await asyncio.sleep(2)
                    await message.delete()
            except TimeoutError:
                await message.edit(embed=discord.Embed(description="`❌ L'auteur n'a pas pu être mis à jour`"))
                await asyncio.sleep(2)
                await message.delete()
        
        for child in self.children:
            child.disabled = False
        await interaction.message.edit(view=self)
            
                    
    @discord.ui.button(label="Retour",emoji="⬅",style=discord.ButtonStyle.red,custom_id="retour")
    async def retour(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.edit_message(view=WelcomeConfigView(self.author,self.bot))
    
    
class ConfigBot(discord.ui.View):
    def __init__(self,author,bot):
        self.author = author
        self.bot = bot
        super().__init__(timeout=180)
    @discord.ui.button(label="Texte du statut",emoji="📝",style=discord.ButtonStyle.gray,custom_id="Texte")
    async def Texte(self, button: discord.ui.Button, interaction: discord.Interaction):
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view=self)
        await interaction.response.send_message(embed=discord.Embed().set_author(name="Configurer le texte du statut"))
        message = await interaction.original_response()
        
        try:
            text = await self.bot.wait_for("message", check=lambda m: m.author == self.author and m.channel == interaction.channel,timeout=30)
            if text:
                await Welcome().config_bot(interaction.guild.id,text=text.content)
                await text.delete()
                await message.edit(embed=discord.Embed(description="`✅ Le texte du statut a bien été mis à jour`"))
                await asyncio.sleep(2)
                await message.delete()
        except TimeoutError:
            await message.edit(embed=discord.Embed(description="`❌ Le texte du statut n'a pas pu être mis à jour`"))
            await asyncio.sleep(2)
            await message.delete()

        for child in self.children:
            child.disabled = False
        await interaction.message.edit(view=self)
    @discord.ui.button(label="Type du statut",emoji="🕶️",style=discord.ButtonStyle.gray,custom_id="statut_type")
    async def statut_type(self, button: discord.ui.Button, interaction: discord.Interaction):  
        
        self.select = discord.ui.Select(
            placeholder="Choisissez un type",
            options=[
                discord.SelectOption(label="Jouer",emoji="🕹️"),
                discord.SelectOption(label="Regarde",emoji="👀"),
                discord.SelectOption(label="Ecoute",emoji="🎧"),
                discord.SelectOption(label="En live",emoji="🎙️"),
                
            ]
        )
        new_view = discord.ui.View()
        self.select.callback = self.callback_select
        new_view.add_item(self.select)
        # get id of message
        self.message_main = interaction.message
        for child in self.children:
            child.disabled = True
        
        
        await interaction.response.send_message(embed=discord.Embed().set_author(name="Configurer le type du statut"),view=new_view)
        
    async def callback_select(self, interaction: discord.Interaction):
        if self.select.values[0] == "Jouer":
            await Welcome().config_bot(interaction.guild.id,type="playing")
        elif self.select.values[0] == "Regarde":
            await Welcome().config_bot(interaction.guild.id,type="watching")
        elif self.select.values[0] == "Ecoute":
            await Welcome().config_bot(interaction.guild.id,type="listening")
        elif self.select.values[0] == "En live":
            await Welcome().config_bot(interaction.guild.id,type="streaming")
        
        
        
        await interaction.response.edit_message(embed=discord.Embed(description="`✅ Le type de statut a bien été mis à jour`"),view=None)
        await asyncio.sleep(2)
        await interaction.message.delete()
        for child in self.children:
            child.disabled = False
            

class ConfigView(discord.ui.View):
    def __init__(self,author,bot):
        self.author = author
        self.bot = bot
        super().__init__(timeout=180)
        self.opt = [
            discord.SelectOption(label="Configurer le plugins de bienvenue",emoji="👋",description="Configurer le plugin de bienvenue"),
            discord.SelectOption(label="Configuration du statut",emoji="📝",description="Configurer le statut du bot")
        ]

        self.select = discord.ui.Select(
            placeholder="Choisissez une option",
            options=self.opt)
        self.select.callback = self.callback
        self.add_item(self.select)
    async def check_interaction(self, interaction: discord.Interaction):
        if not self.author == interaction.user:
            return await interaction.response.send_message("Vous n'avez pas le droit d'effectuer cette action", ephemeral=True)
        else:
            return True
    async def callback(self, interaction: discord.Interaction):
        if self.select.values[0] == self.opt[0].label:
            await interaction.response.edit_message(view=WelcomeConfigView(
                author=interaction.user,
                bot=self.bot
            ))
        if self.select.values[0] == self.opt[1].label:
            await interaction.response.edit_message(view=ConfigBot(
                author=interaction.user,
                bot=self.bot   
            ))