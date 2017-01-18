import discord
# from opus_loader import load_opus_lib

# Function for joining a voice channel
def JoinVoiceChannel(client):
	channel = discord.utils.get(discord.server.channels, name='General', type=ChannelType.voice)
	discord.opus.load_opus
	voice = client.join_voice_channel(channel)
	return voice
	