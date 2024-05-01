from db.mongo import welcome


class Welcome:
    async def set_channel(self,guild,channel):
        welcome.update_one({"guild_id": guild}, {"$set": {"channel": channel}}, upsert=True)
    async def config_message(self, guild, title=None, description=None, color=None, footer=None, thumbnail=None, author=None, image=None):
        update_data = {}  # Dictionnaire pour stocker les champs à mettre à jour
        if title is not None:
            update_data["panel.title"] = title
        if description is not None:
            update_data["panel.description"] = description
        if color is not None:
            update_data["panel.color"] = color
        if footer is not None:
            update_data["panel.footer"] = footer
        if thumbnail is not None:
            update_data["panel.thumbnail"] = thumbnail
        if author is not None:
            update_data["panel.author"] = author
        if image is not None:
            update_data["panel.image"] = image
        
        # Mettre à jour le document dans la base de données avec les champs spécifiés
        welcome.update_one({"guild_id": guild}, {"$set": update_data}, upsert=True)

    def is_active(self,guild):
        find = welcome.find_one({"guild_id": guild})
        
        if find:
            if find.get("active"):
                return True
            else:
                return False
        return False
    async def set_active(self,guild):
        if self.is_active(guild):
            welcome.update_one({"guild_id": guild}, {"$set": {"active": False}}, upsert=True)
        else:
            welcome.update_one({"guild_id": guild}, {"$set": {"active": True}}, upsert=True)
    def get_embed(self, guild):
        embeds = []  # Liste pour stocker les informations de chaque panneau
        find = welcome.find_one({"guild_id": guild})
        panel_data = find.get("panel")  # Vérifier si des données sont trouvées et si la clé "panel" est présente
            
        embed_data = {
                    'title': panel_data.get("title"),
                    'description': panel_data.get("description"),
                    'color': panel_data.get("color"),
                    'footer': panel_data.get("footer"),
                    'thumbnail': panel_data.get("thumbnail"),
                    'author': panel_data.get("author"),
                    'image': panel_data.get("image")
                }
        embeds.append(embed_data)  # Ajouter les informations de ce panneau à la liste des embeds
        return embeds

        
    async def get_channel(self,guild):
        find = welcome.find_one({"guild_id": guild})
        return find.get("channel")
    async def config_bot(self,guild,text=None,type=None):
        data = {}
        if text is not None:
            data["statut.text"] = text
        if type is not None:
            data["statut.type"] = type
        welcome.update_one({"guild_id": guild}, {"$set": data}, upsert=True)
    async def get_statut(self,guild):
        find = welcome.find_one({"guild_id": guild})
        if find:
            return find.get("statut")