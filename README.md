# 🎶 **Discord Music Bot (Python/Discord.py)**

🚀 A powerful and simple Discord bot focused on voice playback, built with **Python** and **discord.py**. It includes basic moderation and dynamic status updates.

## 📌 Features

✅ **Voice Playback** – Streams high-quality audio from YouTube using `!play`.
✅ **Playback Controls** – Use `!pause`, `!resume`, and `!stop` to manage the audio stream.
✅ **Dynamic Status** – The bot's activity is automatically updated to show the title of the song currently playing.
✅ **Basic Moderation** – Use `!clear <number>` to delete messages (requires permissions).
✅ **Utility Commands** – `!ping` and `!echo` for simple interaction checks.

## 🛠️ Tech Stack

* **Language:** Python 3.8+

* **Primary Library:** discord.py

* **Downloader:** yt-dlp

* **Audio Processing:** FFmpeg (External Dependency)

## 🚀 Installation & Setup

### 1. Prerequisites (FFmpeg)

This bot relies on **FFmpeg** to handle audio streaming. It must be installed on your system and accessible via the **PATH** environment variable.

1. **Download FFmpeg:** Download the FFmpeg executable for your operating system.

2. **Add to PATH:** Ensure the `/bin` directory containing `ffmpeg.exe` is correctly added to your system's PATH. This is a **mandatory step**.

### 2. Install Dependencies

Clone the repo and install the required Python packages:

pip install discord.py python-dotenv yt-dlp pynacl


### 3. Set Up Environment Variables

Create a file named **`.env`** in the root directory of the project and add your Discord Bot Token:

BOT_TOKEN = "YOUR_DISCORD_BOT_TOKEN_HERE"


### 4. Permissions

Ensure your bot has the following key Discord permissions:

* **Voice Channel:** `Connect`, `Speak`.

* **Text Channel:** `Manage Messages` (for `!clear`).

### 5. Run the Bot

Execute the main Python script from your terminal:

python bot.py


## 💡 Usage

* **Joining Voice:** To invite the bot, join a voice channel and type `!join`.

* **Playing Music:** Use `!play <YouTube URL>`. The bot will stop any currently playing track and immediately start the new one.

* **Controlling Playback:** Use `!pause` or `!resume` to briefly manage the stream.

* **Ending Session:** Use `!stop` to stop playback and disconnect the bot.

## 📜 License

This project is **open source** and available under the MIT License – feel free to use, modify, and contribute!
