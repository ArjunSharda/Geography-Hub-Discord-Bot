from nextcord.ext import commands, application_checks
import nextcord
import json
import random
import os
import keep_alive
from typing import Optional
from nextcord import Interaction
from datetime import datetime
import asyncio
from nextcord.abc import *
intents = nextcord.Intents.all()
keep_alive.keep_alive()
client = nextcord.Client(intents=intents)

intents = nextcord.Intents.all()

footertitle = "Geography Hub"
footerlogo = "https://media.discordapp.net/attachments/1115663412513488988/1177337323625656402/geo-min.jpg?ex=657223d3&is=655faed3&hm=94a2fd38cb79723233ce4f915f02567e3030a81d3ef171b9ba5912e8f761f04c&=&format=webp&width=1024&height=1024"

@client.event
async def on_ready():
  await client.change_presence(status=nextcord.Status.idle, activity=nextcord.Activity(type=nextcord.ActivityType.watching, name="Geography Hub"))
  print("=====================")
  print("Geography Hub's AI")
  print("---------------------")
  print("Status: Running")
  print("---------------------")
  print(f"Logged in as {client.user}")
  print("=====================")

@client.event
async def on_member_join(member):
  embed = nextcord.Embed(title="Welcome to Geography Hub!", description="Welcome to Geography Hub, a community hosted on Discord for people who have a interest in geography, or just to chat with other people! We hope you enjoy our community. At this time, please take a moment to check out our rules in <#1115650841303597158>. If you have any suggestions for our server, please let us know in <#1177630296334684170>. \n \n Thank you, \n Arjun Sharda \n Founder, Geography Hub", color=nextcord.Color.green(), timestamp=datetime.now())
  embed.set_author(name=f"{member}", icon_url=f"{member.display_avatar.url}")
  embed.set_footer(text=footertitle, icon_url=footerlogo)
  await member.send(embed=embed)

  joinlogs = nextcord.Embed(title="New Join", description=f"{member.mention} has joined the server!", color=nextcord.Color.green(), timestamp=datetime.now())
  embed.set_author(name=member, icon_url=member.display_avatar.url)
  embed.set_footer(text=footertitle, icon_url=footerlogo)
  joinlogchannel = client.get_channel(1177702401432625252)
  await joinlogchannel.send(embed=joinlogs)


@client.event
async def on_message_edit(before, after):
  if after.author != client.user:
    if before.content != after.content:
      embed = nextcord.Embed(title="Message Edited", description=f"User: {after.author.mention} \n \n Channel: {after.channel.mention} \n \n Before Message: {before.content} \n \n After Message: {after.content}", color=nextcord.Color.yellow(), timestamp=datetime.now())
      author = after.author
      embed.set_author(name=f"{author}", icon_url=f"{author.display_avatar.url}")
      embed.set_footer(text=footertitle, icon_url=footerlogo)
      message_log = client.get_channel(1177750576549863455)
      await message_log.send(embed=embed)

@client.event
async def on_message_delete(message):
  if message.author != client.user:
    embed = nextcord.Embed(title="Message Deleted", description=f"User: {message.author.mention} \n \n Channel: {message.channel.mention} \n \n Message: {message.content}", color=nextcord.Color.red(), timestamp=datetime.now())
    author = message.author
    embed.set_author(name=f"{author}", icon_url=f"{author.display_avatar.url}")
    embed.set_footer(text=footertitle, icon_url=footerlogo)
    message_log = client.get_channel(1177750576549863455)
    await message_log.send(embed=embed)

@application_checks.has_role(1115660863324565636)
@client.slash_command(description="Check the amount of members in this server!")
async def membercount(interaction: Interaction):
  embed = nextcord.Embed(title="Member Count", description=f"There are {len(interaction.guild.members)} members in this server!", color=nextcord.Color.green())
  embed.set_footer(text=footertitle, icon_url=footerlogo)
  await interaction.send(embed=embed)

@application_checks.has_role(1115660863324565636)
@client.slash_command(description="Suggest something!")
async def suggest(interaction: Interaction):
  class SuggestionModal(nextcord.ui.Modal):
    def __init__(self):
      super().__init__(
        "Submit a Suggestion"
      )
      self.sTitle = nextcord.ui.TextInput(label="Suggestion Title", min_length=10, max_length=1000, required=True, placeholder="Enter the title of your suggestion!")
      self.add_item(self.sTitle)

      self.sDescription = nextcord.ui.TextInput(label="Suggestion Description", min_length=10, max_length=1000, required=True, placeholder="Describe your suggestion!!", style=nextcord.TextInputStyle.paragraph)
      self.add_item(self.sDescription)

    async def callback(self, interaction: nextcord.Interaction) -> None:
      title = self.sTitle.value
      description = self.sDescription.value
      schannel = client.get_channel(1177630296334684170)
      embed = nextcord.Embed(title=f"Suggestion: {title}", description=f"Submitted by: {interaction.user.mention}. \n \n Description: {description}", color=nextcord.Color.green(), timestamp=datetime.now())
      embed.set_footer(text=footertitle, icon_url=footerlogo)
      message = await schannel.send(embed=embed)
      await message.add_reaction("👍")
      await message.add_reaction("👎")
  await interaction.response.send_modal(SuggestionModal())

      
      


@client.slash_command(description="View the avatar of another member!")
async def avatar(interaction: Interaction, user: nextcord.Member, server_avatar: Optional[bool], user_avatar: Optional[bool]):
  if server_avatar is True:
    S_Avatar = user.display_avatar
    embed = nextcord.Embed(title=f"{user}'s server avatar", color=nextcord.Color.green(), timestamp=datetime.now())
    embed.set_image(url=S_Avatar)
    embed.set_footer(text=footertitle, icon_url=footerlogo)
    await interaction.send(embed=embed)

  if user_avatar is True:
    u_avatar = user.avatar.url
    embed = nextcord.Embed(title=f"{user}'s user avatar", color=nextcord.Color.green(), timestamp=datetime.now())
    embed.set_image(url=u_avatar)
    embed.set_footer(text=footertitle, icon_url=footerlogo)
    await interaction.send(embed=embed)

  if server_avatar or user_avatar is None:
    embed = nextcord.Embed(title="An error occured", description="The user does not have a custom avatar.", color=nextcord.Color.red(), timestamp=datetime.now())
    embed.set_footer(text=footertitle, icon_url=footerlogo)
    await interaction.send(embed=embed, ephemeral=True)
    
    

@client.slash_command(description="Ask the magical 8ball a question!")
async def eightball(interaction: Interaction, *, question: str):
  embed = nextcord.Embed(title="8ball Verdict", description=f"Question: {question}\n \n Answer: {random.choice(['Yes', 'Definitely So', 'Definitely Not', 'No', 'Maybe', 'Ask again later', 'I do not know', 'I do not think so', 'I think so', 'I think not'])}", color=nextcord.Color.random())
  embed.set_footer(text=footertitle, icon_url=footerlogo)
  await interaction.send(embed=embed)



@application_checks.has_role(1115655364160016414)
@client.slash_command(description="[OWNER] Say something!")
async def say(interaction: Interaction, title: str, description: str, user: Optional[nextcord.User], channel: Optional[nextcord.TextChannel], role: Optional[nextcord.Role]):
  embed = nextcord.Embed(title=title, description=f"{description}", color=nextcord.Color.random(), timestamp=datetime.now())
  embed.set_footer(text=footertitle, icon_url=footerlogo)
  if user:
    await user.send(embed=embed)

  if channel:
    await channel.send(embed=embed)

  if role:
    members = role.members
    for member in members:
      
      await asyncio.sleep(0.1)
      try:
        await member.send(embed=embed)
      except nextcord.Forbidden:
        embed = nextcord.Embed(title="Couldn't send message", description=f"Couldn't send a message to {member}. User does not allow messages from bots.", color=nextcord.Color.red(), timestamp=datetime.now())
        embed.set_footer(text=footertitle, icon_url=footerlogo)
        await interaction.send(embed=embed, ephemeral=True)

@application_checks.has_role(1115662802082861139)
@client.slash_command(description="[MOD] Purge a specific amount of messages in a channel!")
async def purge(interaction: Interaction, amount: int, channel: Optional[nextcord.TextChannel]):
  if channel:
    await channel.purge(limit=amount)
    embed  = nextcord.Embed(title="✅ Purge Successful", description=f"Successfully purged `{amount}` messages!", color=nextcord.Color.green(), timestamp=datetime.now())
    embed.set_footer(text=footertitle, icon_url=footerlogo)
    await interaction.send(embed=embed, ephemeral=True)

  if channel is None:
    await interaction.channel.purge(limit=amount)
    embed  = nextcord.Embed(title="✅ Purge Successful", description=f"Successfully purged `{amount}` messages!", color=nextcord.Color.green(), timestamp=datetime.now())
    embed.set_footer(text=footertitle, icon_url=footerlogo)
    await interaction.send(embed=embed)

  if amount is None:
    embed  = nextcord.Embed(title="🚫 Purge Cancelled", description="The amount of messages you want to purge is not specified.", color=nextcord.Color.red(), timestamp=datetime.now())
    embed.set_footer(text=footertitle, icon_url=footerlogo)
    await interaction.send(embed=embed, ephemeral=True)

@application_checks.has_role(1115660863324565636)
@client.slash_command(description="File a report against someone, anonymously!")
async def report(interaction: Interaction, user: nextcord.Member, title: str, reason: str, proof: str):
  
  class ReportButtons(nextcord.ui.View):
    def __init__(self):
      super().__init__()
      self.value = None


    @nextcord.ui.button(label="Confirm Report", style=nextcord.ButtonStyle.green)
    async def confirm(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
      embed = nextcord.Embed(title="Report Confirmed", description=f"Your report has been confirmed! It has successfully been sent to Geography Hub's staff team. Your report is 100% anonymous. Please note that, false reports may lead to disciplinary action against you in the server. \n \n Reported user: {user} \n \n Reason: {reason} \n \n Proof: {proof}", color=nextcord.Color.green(), timestamp=datetime.now())
      embed.set_footer(text=footertitle, icon_url=footerlogo)
      await interaction.response.send_message(embed=embed, ephemeral=True)
      reportchannel = client.get_channel(1177368202527903824)
      reportembed = nextcord.Embed(title="Report", description=f"{interaction.user.mention} has filed a report against {user.mention} for {reason}. NOTE: False reports may lead to disciplinary action in the server. \n \n Reason: {reason} \n \n Proof: {proof}", color=nextcord.Color.green(), timestamp=datetime.now())
      reportembed.set_footer(text=footertitle, icon_url=footerlogo)
      await reportchannel.send(embed=reportembed)
      self.value = True
      self.stop()

    @nextcord.ui.button(label="Cancel Report", style=nextcord.ButtonStyle.red)
    async def cancel(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
      embed = nextcord.Embed(title="Report Cancelled", description=f"You have cancelled your report against {user.mention}. \n \n Reported User: {user.mention} \n \n Reason: {reason} \n \n Proof: {proof}", color=nextcord.Color.red(), timestamp=datetime.now())
      embed.set_footer(text=footertitle, icon_url=footerlogo)
      await interaction.send(embed=embed, ephemeral=True)
      self.value = False
      self.stop()

  embed = nextcord.Embed(title="Report Confirmation", description=f"Are you sure you want to report {user.mention} for {reason}? Please carefully review your report before submitting, as false reports may result in disciplinary action. \n \n Reported user: {user.mention} \n \n Reason: {reason} \n \n Proof: {proof}", color=nextcord.Color.green(), timestamp=datetime.now())
  embed.set_footer(text=footertitle, icon_url=footerlogo)
  view = ReportButtons()
  await interaction.send(embed=embed, view=view, ephemeral=True)
  await view.wait()

@application_checks.has_role(1115662802082861139)
@client.slash_command(description="[MOD] Send a moderator message to someone. (WARN/BAN/KICK)")
async def sendmodmsg(interaction: Interaction, title: str, description: str, person: nextcord.User, remove_roles: Optional[nextcord.Role], add_roles: Optional[nextcord.Role], kick: Optional[bool], ban: Optional[bool]):
  embed = nextcord.Embed(title=title, description=description, color=nextcord.Color.red(), timestamp=datetime.now())
  embed.set_footer(text=footertitle, icon_url=footerlogo)
  await person.send(embed=embed)
  if remove_roles:
    await person.remove_roles(remove_roles, reason=f"Geography Hub AI: Action taken by {interaction.user}")
  if add_roles:
    await person.add_roles(add_roles, reason=f"Geography Hub AI: Action taken by {interaction.user}")
  if kick:
    await person.kick(reason=f"Geography Hub AI: Action taken by {interaction.user}")
  if ban:
    await person.ban(reason=f"Geography Hub AI: Action taken by {interaction.user}")

@client.slash_command(description="Verify yourself!")
async def verify(interaction: Interaction, introductionmsg: str):

  class VerifySelect(nextcord.ui.Select):
    def __init__(self):
      selectOptions = [
        nextcord.SelectOption(label="Interested Geographist", description="You are a fellow geographist. Welcome home!"),
        nextcord.SelectOption(label="Referred by friend", description="You have been referred by someone in our community."),
        nextcord.SelectOption(label="Other", description="Something else, not listed here.")
      ]
      super().__init__(placeholder="Select who you are", min_values=1, max_values=1, options=selectOptions)


    async def callback(self, interaction: Interaction):
      verifychannel = client.get_channel(1177339493632708628)
      chatchannel = client.get_channel(1115650597237039104)
      logchannel = client.get_channel(1177329725136441364)
      embed = nextcord.Embed(title=f"Verified {interaction.user}", description=f"Geography Hub AI has officially verified {interaction.user.mention}!", color=nextcord.Color.green(), timestamp=datetime.now())
      embed.set_footer(text=footertitle, icon_url=footerlogo)
      role = interaction.guild.get_role(1115660863324565636)
      rrole = interaction.guild.get_role(1115660806743412829)
      member = interaction.user
      embed_chat = nextcord.Embed(title="👋 New Verified Person", description=f"{interaction.user.mention} has officially verified by Geography Hub AI! Please welcome them to the discord server community. \n {interaction.user.mention}'s introduction message: \n \n {introductionmsg}", color=nextcord.Color.green(), timestamp=datetime.now())
      embed_chat.set_footer(text=footertitle, icon_url=footerlogo)
      reason = "Geography Hub AI: Automated Verification"
      thankyouembed = nextcord.Embed(title="Verification Complete", description="Thank you for completing the verification procedure! You should be given the `Member` role shortly.", color=nextcord.Color.green(), timestamp=datetime.now())
      thankyouembed.set_footer(text=footertitle, icon_url=footerlogo)
      Interested_geo_log = nextcord.Embed(title="New Verified Person", description=f"{interaction.user.mention} has officially verified by Geography Hub AI, and **have joined via interest for geography (Interested Geographist)**. Please welcome them to the discord server community. \n {interaction.user.mention}'s introduction message: \n \n {introductionmsg}", color=nextcord.Color.green(), timestamp=datetime.now())
      Interested_geo_log.set_footer(text=footertitle, icon_url=footerlogo)

      Referred_log = nextcord.Embed(title="New Verified Person", description=f"{interaction.user.mention} has officially verified by Geography Hub AI, and **have joined via referral (Referred by Friend)**. Please welcome them to the discord server community. \n {interaction.user.mention}'s introduction message: \n \n {introductionmsg}", color=nextcord.Color.green(), timestamp=datetime.now())
      Referred_log.set_footer(text=footertitle, icon_url=footerlogo)


      Other_log = nextcord.Embed(title="New Verified Person", description=f"{interaction.user.mention} has officially verified by Geography Hub AI, and **have joined via other (Other)**. Please welcome them to the discord server community. \n {interaction.user.mention}'s introduction message: \n \n {introductionmsg}", color=nextcord.Color.green(), timestamp=datetime.now())
      Other_log.set_footer(text=footertitle, icon_url=footerlogo)


      if self.values[0] == "Interested Geographist":
        await interaction.send(embed=thankyouembed, ephemeral=True)
        await member.add_roles(role, reason=reason)
        await member.remove_roles(rrole, reason=reason)
        await verifychannel.send(embed=embed)
        await logchannel.send(embed=Interested_geo_log)
        await chatchannel.send(embed=embed_chat)


      if self.values[0] == "Referred by friend":
        await interaction.send(embed=thankyouembed, ephemeral=True)
        await member.add_roles(role, reason=reason)
        await member.remove_roles(rrole, reason=reason)
        await verifychannel.send(embed=embed)
        await logchannel.send(embed=Referred_log)
        await chatchannel.send(embed=embed_chat)

      if self.values[0] == "Other":
        await interaction.send(embed=thankyouembed, ephemeral=True)
        await member.add_roles(role, reason=reason)
        await member.remove_roles(rrole, reason=reason)
        await verifychannel.send(embed=embed)
        await logchannel.send(embed=Other_log)
        await chatchannel.send(embed=embed_chat)

  class VerifyView(nextcord.ui.View):
    def __init__(self):
      super().__init__()
      self.add_item(VerifySelect())
  view = VerifyView() 
  embed = nextcord.Embed(title="Welcome to Geography Hub!", description="Thanks for starting the verification procedure for joining the Geography Hub discord server. \n \n Please answer this question: \n \n What best describes you?", color=nextcord.Color.green(), timestamp=datetime.now())
  embed.set_footer(text=footertitle, icon_url=footerlogo)
  await interaction.send(embed=embed, view=view, ephemeral=True)    



client.run(os.environ['TOKEN'])

