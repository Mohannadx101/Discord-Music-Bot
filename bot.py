import discord
import os
import yt_dlp as youtube_dl
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        initial_status_message = "!help | Clearing the way!"
        activity = discord.Activity(type=discord.ActivityType.playing, name=initial_status_message)
        
        await self.change_presence(status=discord.Status.online, activity=activity)

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')
        if message.content.lower().startswith('!ping'):
            await message.channel.send('Pong!')
        
        if message.content.lower().startswith('!echo '):
            response = message.content[6:]  # Extract the text after '!echo '
            await message.channel.send(response)
        
        if message.content.lower().startswith('!clear'):
            parts = message.content.split()
            if len(parts) < 2:
                await message.channel.send('Please specify the number of messages to delete. Usage: !clear <number>')
                return 
            try:
                amount = int(parts[1])
            except ValueError:
                await message.channel.send('Please provide a valid number of messages to delete.')
                return
                
            if amount > 100:
                amount = 100  # Discord API limit
                
            try:
                
                deleted = await message.channel.purge(limit=amount + 1)
                
                confirmation_msg = await message.channel.send(f'🧹 Cleared **{len(deleted) - 1}** messages.')
                
                await confirmation_msg.delete(delay=3)

            except discord.errors.Forbidden:
                await message.channel.send("I don't have permission to delete messages here! (Need **Manage Messages** permission).")
            except Exception as e:
                print(f"An error occurred during purge: {e}")
                await message.channel.send("An unexpected error occurred while trying to clear messages.")
        
        if message.author == self.user:
            return

        if message.content.lower() == '!join':
            # 1. Check if the user (message.author) is in a voice channel
            if message.author.voice:
                # The channel to join is the channel the author is in
                channel = message.author.voice.channel
                
                # Check if the bot is already in a voice channel in this guild
                if message.guild.voice_client:
                    # If already connected, move to the new channel
                    await message.guild.voice_client.move_to(channel)
                else:
                    # If not connected, connect to the channel
                    await channel.connect()

                await message.channel.send(f"🎙️ Joined **{channel.name}**!")
            else:
                await message.channel.send("You need to be in a voice channel for me to join!")
                
        elif message.content.lower().startswith('!play'):
            # 1. Check if bot is connected to voice
            vc = message.guild.voice_client
            if not vc:
                await message.channel.send("I need to be in a voice channel first! Use `!join`.")
                return

            # 2. Get the URL
            parts = message.content.split()
            if len(parts) < 2:
                await message.channel.send("Usage: `!play <YouTube URL>`")
                return
            
            url = parts[1]
            
            # Stop any currently playing audio before starting a new one
            if vc.is_playing():
                vc.stop()

            # 3. yt-dlp Options
            YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': True}
            FFMPEG_OPTIONS = {
                'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                'options': '-vn'
            }
            
            try:
                # Run yt-dlp to extract information
                with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                    # Setting download=False means it only fetches stream info, not the file
                    info = ydl.extract_info(url, download=False)
                    
                    # The source is the direct URL to the audio stream
                    audio_source = info['url']
                    song_title = info['title']
                    
                # 4. Create a Discord FFmpegAudio object and play it
                source = discord.FFmpegPCMAudio(audio_source, **FFMPEG_OPTIONS)
                vc.play(source)

                await message.channel.send(f"▶️ Now playing: **{song_title}**")
                
                # 5. DYNAMIC STATUS UPDATE
                # Change activity to 'Listening to [Song Title]'
                activity = discord.Activity(type=discord.ActivityType.listening, name=song_title)
                await self.change_presence(activity=activity)

            except Exception as e:
                print(f"Error during !play: {e}")
                await message.channel.send("An error occurred while trying to process the video or start playback. Check the console for FFmpeg errors.")

                
        elif message.content.lower() == '!stop':
            vc = message.guild.voice_client
            if vc:
                # Stop the currently playing stream
                if vc.is_playing():
                    vc.stop()
                    await message.channel.send("⏹️ Playback stopped.")
                
                # Disconnect the bot from the voice channel
                await vc.disconnect()
                await message.channel.send("👋 Disconnected from voice.")
            else:
                await message.channel.send("I'm not currently in a voice channel.")
                
        elif message.content.lower() == '!pause':
            vc = message.guild.voice_client
            if vc and vc.is_playing():
                vc.pause()
                await message.channel.send("⏸️ Playback paused.")
            else:
                await message.channel.send("Nothing is currently playing.")

        # Check for the !resume command
        elif message.content.lower() == '!resume':
            vc = message.guild.voice_client
            if vc and vc.is_paused():
                vc.resume()
                await message.channel.send("▶️ Playback resumed.")
            else:
                await message.channel.send("Playback is not paused.")        

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(BOT_TOKEN)
