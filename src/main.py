# 11-23-2023 (MM/DD/YY)
# Arjun Sharda
# This file is under the MIT license.
# ©️ Arjun Sharda 2023-present.

from nextcord.ext import commands, application_checks
import nextcord
import json
import random
import os
import keep_alive
from typing import Optional
from nextcord import Interaction
from datetime import datetime
from nextcord.abc import *
intents = nextcord.Intents.all()
keep_alive.keep_alive()
client = nextcord.Client(intents=intents)

intents = nextcord.Intents.all()

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

@application_checks.has_role(1115660863324565636)
@client.slash_command(description="Check the amount of members in this server!")
async def membercount(interaction: Interaction):
  embed = nextcord.Embed(title="Member Count", description=f"There are {len(interaction.guild.members)} members in this server!", color=nextcord.Color.green())
  await interaction.response.send_message(embed=embed)

@client.slash_command(description="Ask the magical 8ball a question!")
async def eightball(interaction: Interaction, *, question: str):
  embed = nextcord.Embed(title="8ball Verdict", description=f"Question: {question}\n \n Answer: {random.choice(['Yes', 'Definitely So', 'Definitely Not', 'No', 'Maybe', 'Ask again later', 'I do not know know', 'I do not think so', 'I think so', 'I think not'])}", color=nextcord.Color.random())
  await interaction.send(embed=embed)



@application_checks.has_role(1115662802082861139)
@client.slash_command(description="[MOD] Say something!")
async def say(interaction: Interaction, title: str, description: str, user: Optional[nextcord.User], channel: Optional[nextcord.TextChannel]):
  embed = nextcord.Embed(title=title, description=description, color=nextcord.Color.random())
  if user:
    await user.send(embed=embed)

  if channel:
    await channel.send(embed=embed)

@application_checks.has_role(1115660863324565636)
@client.slash_command(description="File a report against someone, anonymously!")
async def report(interaction: Interaction, user: nextcord.Member, *, reason: str, proof: Optional[str]):
  class ReportButtons(nextcord.ui.View):
    def __init__(self):
      super().__init__()
      self.value = None


    @nextcord.ui.button(label="Confirm Report", style=nextcord.ButtonStyle.green)
    async def confirm(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
      embed = nextcord.Embed(title="Report Confirmed", description=f"Your report has been confirmed! It has successfully been sent to Geography Hub's staff team. Your report is 100% anonymous. Please note that, false reports may lead to disciplinary action against you in the server. \n \n Reported user: {user} \n \n Reason: {reason} \n \n Proof: {proof}", color=nextcord.Color.green(), timestamp=datetime.now())
      await interaction.response.send_message(embed=embed, ephemeral=True)
      reportchannel = await client.fetch_channel(1177368202527903824)
      reportembed = nextcord.Embed(title="Report", description=f"{interaction.user.mention} has filed a report against {user.mention} for {reason}. NOTE: False reports may lead to disciplinary action in the server. \n \n Reason: {reason} \n \n Proof: {proof}", color=nextcord.Color.green(), timestamp=datetime.now())
      await reportchannel.send(embed=reportembed)
      self.value = True
      self.stop()

    @nextcord.ui.button(label="Cancel Report", style=nextcord.ButtonStyle.red)
    async def cancel(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
      embed = nextcord.Embed(title="Report Cancelled", description=f"You have cancelled your report against {user.mention}. \n \n Reported User: {user.mention} \n \n Reason: {reason} \n \n Proof: {proof}", color=nextcord.Color.red(), timestamp=datetime.now())
      await interaction.send(embed=embed, ephemeral=True)
      self.value = False
      self.stop()

  embed = nextcord.Embed(title="Report Confirmation", description=f"Are you sure you want to report {user.mention} for {reason}? Please carefully review your report before submitting, as false reports may result in disciplinary action. \n \n Reported user: {user.mention} \n \n Reason: {reason} \n \n Proof: {proof}", color=nextcord.Color.green(), timestamp=datetime.now())
  view = ReportButtons()
  await interaction.send(embed=embed, view=view, ephemeral=True)
  await view.wait()


@application_checks.has_role(1115662802082861139)
@client.slash_command(description="[MOD] Send a moderator message to someone. (WARN/BAN/KICK)")
async def sendmodmsg(interaction: Interaction, title: str, description: str, person: nextcord.User, remove_roles: Optional[nextcord.Role], add_roles: Optional[nextcord.Role], kick: Optional[bool], ban: Optional[bool]):
  embed = nextcord.Embed(title=title, description=description, color=nextcord.Color.red(), timestamp=datetime.now())
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
      verifychannel = await client.fetch_channel(1177339493632708628)
      chatchannel = await client.fetch_channel(1115650597237039104)
      logchannel = await client.fetch_channel(1177329725136441364)
      embed = nextcord.Embed(title=f"Verified {interaction.user}", description=f"Geography Hub AI has officially verified {interaction.user.mention}!", color=nextcord.Color.green(), timestamp=datetime.now())
      role = interaction.user.get_role(1115660863324565636)
      rrole = interaction.user.get_role(1115660806743412829)
      member = interaction.user
      embed_chat = nextcord.Embed(title="👋 New Verified Person", description=f"{interaction.user.mention} has officially verified by Geography Hub AI! Please welcome them to the discord server community. \n {interaction.user.mention}'s introduction message: \n \n {introductionmsg}", color=nextcord.Color.green(), timestamp=datetime.now())
      reason = "Geography Hub AI: Automated Verification"
      thankyouembed = nextcord.Embed(title="Verification Complete", description="Thank you for completing the verification procedure! You should be given the `Member` role shortly.", color=nextcord.Color.green(), timestamp=datetime.now())
      Interested_geo_log = nextcord.Embed(title="New Verified Person", description=f"{interaction.user.mention} has officially verified by Geography Hub AI, and **have joined via interest for geography (Interested Geographist)**. Please welcome them to the discord server community. \n {interaction.user.mention}'s introduction message: \n \n {introductionmsg}", color=nextcord.Color.green(), timestamp=datetime.now())

      Referred_log = nextcord.Embed(title="New Verified Person", description=f"{interaction.user.mention} has officially verified by Geography Hub AI, and **have joined via referral (Referred by Friend)**. Please welcome them to the discord server community. \n {interaction.user.mention}'s introduction message: \n \n {introductionmsg}", color=nextcord.Color.green(), timestamp=datetime.now())


      Other_log = nextcord.Embed(title="New Verified Person", description=f"{interaction.user.mention} has officially verified by Geography Hub AI, and **have joined via other (Other)**. Please welcome them to the discord server community. \n {interaction.user.mention}'s introduction message: \n \n {introductionmsg}", color=nextcord.Color.green(), timestamp=datetime.now())


      if self.values[0] == "Interested Geographist":
        await interaction.send(embed=thankyouembed, ephemeral=True)
        await member.add_roles(role, reason=reason)
        await member.remove_roles(rrole, reason=reason)
        await verifychannel.send(embed=embed)
        await chatchannel.send(embed=embed_chat)
        await logchannel.send(embed=Interested_geo_log)

      if self.values[0] == "Referred by friend":
        await interaction.send(embed=thankyouembed, ephemeral=True)
        await member.add_roles(role, reason=reason)
        await verifychannel.send(embed=embed)
        await chatchannel.send(embed=embed_chat)
        await logchannel.send(embed=Referred_log)

      if self.values[0] == "Other":
        await interaction.send(embed=thankyouembed, ephemeral=True)
        await member.add_roles(role, reason=reason)
        await verifychannel.send(embed=embed)
        await logchannel.send(embed=Other_log)
        await chatchannel.send(embed=Other_log)

  class VerifyView(nextcord.ui.View):
    def __init__(self):
      super().__init__()
      self.add_item(VerifySelect())
  view = VerifyView() 
  embed = nextcord.Embed(title="Welcome to Geography Hub!", description="Thanks for starting the verification procedure for joining the Geography Hub discord server. \n \n Please answer this question: \n \n What best describes you?", color=nextcord.Color.green(), timestamp=datetime.now())
  await interaction.send(embed=embed, view=view, ephemeral=True)    



client.run(os.environ['TOKEN'])

