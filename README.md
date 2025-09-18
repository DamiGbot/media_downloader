# 🎬 Media Downloader

Download videos from YouTube, Instagram, TikTok, Twitter, and Vimeo - all in one place, with a beautiful interface.

## Why This Exists

Tired of juggling different tools for different platforms? Want to download that YouTube playlist without ads, save TikToks before they disappear, or grab Instagram reels for offline viewing? This tool does it all, and it looks good doing it.

## What You Get

**Supported Platforms:**
- 📺 YouTube (videos, playlists, entire channels)
- 📸 Instagram (posts and reels)
- 🎵 TikTok (all those viral videos)
- 🐦 Twitter/X (video tweets)
- 🎥 Vimeo (high-quality content)

**The Experience:**
- Beautiful terminal interface that actually looks modern
- Smart error handling (no more cryptic SSL messages)
- Always downloads the best quality available
- Organizes your downloads automatically
- Works with playlists and channels, not just single videos

## Getting Started

**Step 1: Get the code**
```bash
git clone https://github.com/yourusername/media-downloader.git
cd media-downloader
```

**Step 2: Install what you need**
```bash
pip install yt-dlp rich art textual
```

**Step 3: Start downloading**
```bash
python -m media_downloader -i
```

That's it. The interactive mode will guide you through everything.

## Daily Usage

**Quick download:**
```bash
python -m media_downloader "your-video-url-here"
```

**Interactive mode (recommended):**
```bash
python -m media_downloader -i
```

**Audio only (for music):**
```bash
python -m media_downloader -a "url"
```

**Custom folder:**
```bash
python -m media_downloader -o ~/Music "url"
```

## Why It's Better

**Smart Organization:** Your downloads get sorted automatically. YouTube playlists go into folders, Instagram posts get labeled clearly, and everything has a sensible filename.

**Actually Works with Instagram:** Instagram tries really hard to block downloaders. This tool handles their anti-bot measures gracefully and tells you what's happening.

**No SSL Headaches:** Those annoying certificate errors? Fixed automatically. No more googling cryptic error messages.

**Beautiful Interface:** Choose from a simple console, rich colored output, or a full-screen interface that looks like a proper app.

**Honest Error Messages:** When something goes wrong, you get helpful suggestions instead of technical jargon.

## Common Scenarios

**Download a YouTube playlist for a flight:**
```bash
python -m media_downloader -i
# Paste playlist URL, choose video quality, done
```

**Save Instagram reels from your favorite creator:**
```bash
python -m media_downloader -i
# Paste Instagram URL, it handles the rest
```

**Extract audio from YouTube music videos:**
```bash
python -m media_downloader -a "youtube-music-url"
# Gets high-quality MP3 automatically
```

**Backup a Twitter thread with videos:**
```bash
python -m media_downloader -i
# Works with individual video tweets
```

## When Things Go Wrong

**Instagram being difficult:** This happens. Instagram blocks automated downloads randomly. Wait 30 minutes and try again, or use a VPN.

**SSL certificate errors:** The tool fixes these automatically, but if you still see them, run `pip install --upgrade yt-dlp`.

**Quality not available:** Some videos don't have the quality you want. The tool will automatically pick the best available and tell you what it chose.

**Video unavailable:** Could be private, deleted, or geo-blocked. The error messages will explain what's happening.

## For Developers

Want to add support for another platform? The code is organized to make this easy. Each platform is its own module, and adding a new one means implementing just a few methods.

The UI system is modular too - there are four different interfaces, from basic console to full-screen terminal app. Pick what works for your users.

## The Technical Bits

Built on yt-dlp (the actively maintained YouTube downloader), with Rich for beautiful terminal output and Textual for the full-screen interface. Everything is organized into clear modules so you can understand and modify the code easily.

Quality defaults to "best" because why would you want anything less? File organization follows common sense - playlists get folders, everything gets clear names, and platform prefixes help you find things later.

## Contributing

Found a bug? Want to add a platform? Pull requests welcome. The code is structured to be readable and extensible.

---

**Just want to download videos without the hassle? Run `python -m media_downloader -i` and start downloading.**