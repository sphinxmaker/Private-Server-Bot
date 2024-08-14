import nextcord
from nextcord.ext import commands
from nextcord import Interaction
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = nextcord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

whitelist_file = 'whitelist.txt'

def load_whitelist():
    if os.path.exists(whitelist_file):
        with open(whitelist_file, 'r') as file:
            return set(line.strip() for line in file.readlines())
    return set()

def save_whitelist(whitelist):
    with open(whitelist_file, 'w') as file:
        for user_id in whitelist:
            file.write(f'{user_id}\n')

whitelist = load_whitelist()

@bot.slash_command(name="whitelist", description="Whitelist a user", guild_ids=[1269703897010671626])
async def whitelist_user(interaction: Interaction, user: nextcord.User):
    if str(user.id) in whitelist:
        await interaction.response.send_message(f'{user.mention} is already whitelisted.')
    else:
        whitelist.add(str(user.id))
        save_whitelist(whitelist)
        await interaction.response.send_message(f'{user.mention} has been whitelisted!')

@bot.slash_command(name="rmwhitelist", description="Remove a user from the whitelist", guild_ids=[1269703897010671626])
async def remove_whitelist(interaction: Interaction, user: nextcord.User):
    if str(user.id) in whitelist:
        whitelist.remove(str(user.id))
        save_whitelist(whitelist)
        await interaction.response.send_message(f'{user.mention} has been removed from the whitelist.')
    else:
        await interaction.response.send_message(f'{user.mention} is not in the whitelist.')

@bot.slash_command(name="list", description="List all whitelisted users", guild_ids=[1269703897010671626])
async def list_whitelist(interaction: Interaction):
    if whitelist:
        users = [f'<@{user_id}>' for user_id in whitelist]
        await interaction.response.send_message(f'Whitelisted users: {", ".join(users)}')
    else:
        await interaction.response.send_message('No users are whitelisted.')

@bot.slash_command(name="check", description="Check if a user is whitelisted", guild_ids=[1269703897010671626])
async def check_whitelist(interaction: Interaction, user: nextcord.User = None):
    user = user or interaction.user
    if str(user.id) in whitelist:
        await interaction.response.send_message(f'{user.mention} is whitelisted.')
    else:
        await interaction.response.send_message(f'{user.mention} is not whitelisted.')

@bot.event
async def on_member_join(member):
    if str(member.id) not in whitelist:
        await member.send(
            "You are not whitelisted on our private server. You will be kicked. Purchase access by contacting <@1051935640209588294>."
        )
        await member.kick(reason="Not whitelisted")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if str(message.author.id) not in whitelist:
        await message.author.send(
            "You are not whitelisted on our private server. Purchase access by contacting <@1051935640209588294>."
        )
        await message.delete()
        return

    await bot.process_commands(message)

bot.run(TOKEN)
