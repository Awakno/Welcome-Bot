def variable(message,user=None,guild=None,bot=None):
    if user:
        member_formatter = {
            "{user}": str(user),
            "{user.mention}": user.mention,
            "{user.display_name}": user.display_name,
            "{user.id}": str(user.id),
            "{user.name}": user.name,
            "{user.avatar}": str(user.display_avatar.url)
        }
    if guild:
        guild_formatter = {
            
            "{guild.name}": str(guild.name),
            "{guild.id}": str(guild.id),
            "{guild.member_count}": str(guild.member_count),
            "{guild.icon}": str(guild.icon.url) if guild.icon else None 
        }
    if bot:
        bot_formatter = {
            "{bot}": str(bot.user),
            "{bot.mention}": str(bot.user.mention),
            "{bot.name}": str(bot.user.name),
            "{bot.id}": str(bot.user.id),
            "{bot.avatar}": str(bot.user.display_avatar.url)
        }
    end = message
    if user:
        for key,value in member_formatter.items():
            
            end = end.replace(key,value)
    if guild:
        for key,value in guild_formatter.items():
            end = end.replace(key,value)
    if bot:
        for key,value in bot_formatter.items():
            end = end.replace(key,value)
    
    return end
        
