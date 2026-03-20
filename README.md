# JagoBD Auto-Updating M3U8 Playlist 📺

![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/tahsinulmohsin/jagobd-m3u8-scraper/update_m3u8.yml?branch=master&label=Auto-Updater&style=flat-square)
![License](https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square)

This repository contains an automated Python scraper that dynamically extracts live streaming M3U8 links for all Bangladeshi TV channels from JagoBD.com. It bypasses JagoBD's stream obfuscation and HTTP Referer protections to generate a fully working, continuously updated IPTV playlist.

Because JagoBD's authentication tokens expire frequently, this repository uses **GitHub Actions** to automatically run the scraper every 20 minutes and commit the fresh `playlist.m3u8` back to this repository!

## ✨ Features
- **Auto-Updating:** Generates a fresh playlist bypassing token short-livings.
- **TV Logos:** Automatically parses `tvg-logo` metadata tags directly from JagoBD for crystal clear channel icons in your TV Guide.
- **VLC Metadata Fixes:** Forwards HTTP Referer tags to bypass firewall IP bans on JagoBD's CDNs.
- **Docker Support:** Continuously packages a lightweight Docker image pushed directly to GitHub Packages for home-server isolation.

## 🔗 Your Playlist URL
To watch the channels, simply add the following raw URL to your favorite IPTV player:

```text
https://raw.githubusercontent.com/tahsinulmohsin/jagobd-m3u8-scraper/master/playlist.m3u8
```

## 📱 Supported Players
JagoBD strictly blocks streaming requests that do not contain their exact HTTP `Referer` header. This playlist includes the special metadata tags (`#EXTVLCOPT` and `|Referer=`) to automatically append those headers on supported players.

For a flawless, plug-and-play experience, we highly recommend using a modern IPTV player on your Android/Google TV or smartphone:
- **TiviMate** (Highly Recommended)
- **Televizo**
- **OTT Navigator** 
- **Kodi** (with PVR IPTV Simple Client)

### ⚠️ A Note on VLC Media Player
If you try to load this playlist into **VLC** normally, it will throw an error (`unable to open the MRL`). This is because VLC intentionally ignores HTTP Referer metadata inside local/remote M3U files for security reasons (CVE-2013-6903).

If you absolutely must use VLC on your PC, you must launch it via your command line (or edit your Windows Shortcut Target) to include this special flag:
```bash
vlc.exe --m3u-extvlcopt
```

## ⚙️ How It Works
1. `main.py` is a Python script that impersonates a real browser to load JagoBD category headers.
2. It parses the DOM for the `embed.php` iframe sources across all active broadcast channels.
3. It reverse-engineers the inline javascript string arrays (`["h","t","t"...].join("")`) to reconstruct the base `.m3u8` URLs without needing a heavy headless browser block.
4. `.github/workflows/update_m3u8.yml` runs a cron job on `ubuntu-latest` every 20 minutes (`*/20 * * * *`), spinning up Python, fetching the new stream endpoints, and pushing `playlist.m3u8` back here!

## 🐳 Docker Deployment (Optional)
If you prefer running the script on your own Raspberry Pi or Home Server instead of relying on GitHub Actions, you can pull the automated Docker Image from GitHub Packages:
```bash
docker run -v $(pwd):/app ghcr.io/tahsinulmohsin/jagobd-m3u8-scraper:latest
```
This will silently run the scraper and drop `playlist.m3u8` right into your current directory.

## 📜 Disclaimer
This script is provided for educational purposes only. All streams belong to their respective copyright owners (JagoBD/Broadcasters).
