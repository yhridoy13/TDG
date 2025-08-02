import discord
import os
import asyncio
from dotenv import load_dotenv
from keep_alive import keep_alive
from discord import app_commands

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SERVER_ID = int(os.getenv('SERVER_ID'))
WELCOME_CHANNEL_ID = int(os.getenv('WELCOME_CHANNEL_ID'))
TOURNAMENT_CHANNEL_ID = int(os.getenv('TOURNAMENT_CHANNEL_ID'))

# Bot setup
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)

# Team storage
teams = {}  # {team_name: {"captain": user_id, "players": [user_ids], "role_id": role_id}}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await tree.sync(guild=discord.Object(id=SERVER_ID))
    print("Commands synced!")

# Welcome system
@bot.event
async def on_member_join(member):
    # Server welcome
    welcome_channel = bot.get_channel(WELCOME_CHANNEL_ID)
    embed = discord.Embed(
        title=f"Welcome to {member.guild.name}!",
        description=f"Hey {member.mention}! Welcome to our server!",
        color=discord.Color.blue()
    )
    await welcome_channel.send(embed=embed)
    
    # DM notification
    try:
        await member.send(f"Welcome to {member.guild.name}! Stay tuned for tournament announcements!")
    except:
        pass

# Team registration command
@tree.command(name="register_team", description="Register a new team", guild=discord.Object(id=SERVER_ID))
@discord.app_commands.describe(team_name="Name of your team")
async def register_team(interaction: discord.Interaction, team_name: str):
    user = interaction.user
    guild = interaction.guild
    
    # Check if team exists
    if team_name in teams:
        await interaction.response.send_message("Team name already exists!", ephemeral=True)
        return
    
    # Create team role
    role = await guild.create_role(name=team_name)
    await user.add_roles(role)
    
    # Store team data
    teams[team_name] = {
        "captain": user.id,
        "players": [user.id],
        "role_id": role.id
    }
    
    await interaction.response.send_message(f"Team '{team_name}' registered successfully! You're the captain.", ephemeral=True)

# Add player command
@tree.command(name="add_player", description="Add a player to your team", guild=discord.Object(id=SERVER_ID))
@discord.app_commands.describe(player="Player to add", team_name="Your team name")
async def add_player(interaction: discord.Interaction, player: discord.Member, team_name: str):
    user = interaction.user
    
    # Check if team exists and user is captain
    if team_name not in teams or teams[team_name]["captain"] != user.id:
        await interaction.response.send_message("You're not the captain of this team!", ephemeral=True)
        return
    
    # Check team size
    if len(teams[team_name]["players"]) >= 6:
        await interaction.response.send_message("Team is full (6 players max)!", ephemeral=True)
        return
    
    # Add player to team
    guild = interaction.guild
    role = guild.get_role(teams[team_name]["role_id"])
    await player.add_roles(role)
    teams[team_name]["players"].append(player.id)
    
    await interaction.response.send_message(f"{player.mention} added to {team_name}!", ephemeral=True)

# Tournament notification
@tree.command(name="announce_tournament", description="Announce a new tournament", guild=discord.Object(id=SERVER_ID))
@discord.app_commands.describe(details="Tournament details")
async def announce_tournament(interaction: discord.Interaction, details: str):
    channel = bot.get_channel(TOURNAMENT_CHANNEL_ID)
    embed = discord.Embed(
        title="🏆 New Tournament! 🏆",
        description=details,
        color=discord.Color.gold()
    )
    await channel.send(embed=embed)
    
    # DM all team captains
    for team_name, team_data in teams.items():
        captain = bot.get_user(team_data["captain"])
        try:
            await captain.send(f"New tournament announced: {details}")
        except:
            pass
    
    await interaction.response.send_message("Tournament announced!", ephemeral=True)

# Match reminder system
async def match_reminder():
    await bot.wait_until_ready()
    while not bot.is_closed():
        # This is a placeholder - implement actual match scheduling logic
        # For demonstration, we'll send a test reminder every hour
        await asyncio.sleep(3600)  # 1 hour
        
        # Get all team captains
        for team_name, team_data in teams.items():
            captain = bot.get_user(team_data["captain"])
            try:
                await captain.send("Reminder: Your match starts in 30 minutes!")
            except:
                pass

# Start background task
@bot.event
async def on_ready():
    print("Starting match reminder task...")
    asyncio.create_task(match_reminder())

# Start bot
keep_alive()
bot.run(MTQwMTIyMjc3MzU2NDUwNjE0NQ.G1Oc_H.jHyKFG_-1ZMbtJEhakqV_y48_vGr4Nk-v9bhww)