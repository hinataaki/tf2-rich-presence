[![Github all releases](https://img.shields.io/github/downloads/Kataiser/tf2-rich-presence/total.svg)](https://www.somsubhra.com/github-release-stats/?username=Kataiser&repository=tf2-rich-presence)
[![GitHub release](https://img.shields.io/github/release/Kataiser/tf2-rich-presence.svg)](https://GitHub.com/Kataiser/tf2-rich-presence/releases/)
[![GitHub Release Date](https://img.shields.io/github/release-date/Kataiser/tf2-rich-presence.svg)](https://GitHub.com/Kataiser/tf2-rich-presence/releases/)
![Platform: Windows](https://img.shields.io/badge/platform-Windows-lightgrey?cacheSeconds=100000)
[![Kataiser on Steam](https://img.shields.io/badge/Steam-Kataiser-blue?logo=Steam)](https://steamcommunity.com/id/mechkataiser)
[![Ko-fi](https://img.shields.io/badge/Ko--fi-Kataiser-29ABE0?logo=Ko-fi)](https://ko-fi.com/kataiser)

[![GitHub commits since latest release](https://img.shields.io/github/commits-since/Kataiser/tf2-rich-presence/latest)](https://github.com/Kataiser/tf2-rich-presence/commits/master)
[![GitHub last commit](https://img.shields.io/github/last-commit/Kataiser/tf2-rich-presence.svg)](https://github.com/Kataiser/tf2-rich-presence/commits/master)
[![Updates](https://pyup.io/repos/github/Kataiser/tf2-rich-presence/shield.svg)](https://pyup.io/repos/github/Kataiser/tf2-rich-presence/)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/18a048d3a05e4815b247d886abef575f)](https://www.codacy.com/app/Kataiser/tf2-rich-presence?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Kataiser/tf2-rich-presence&amp;utm_campaign=Badge_Grade)
[![Travis tests](https://img.shields.io/travis/Kataiser/tf2-rich-presence/master?label=tests&logo=Travis)](https://travis-ci.org/Kataiser/tf2-rich-presence)
[![Help wanted tag](https://img.shields.io/github/labels/Kataiser/tf2-rich-presence/help%20wanted?cacheSeconds=100000)](https://github.com/Kataiser/tf2-rich-presence/issues?q=is%3Aissue+is%3Aopen+sort%3Aupdated-desc+label%3A%22help+wanted%22)

# TF2 Rich Presence
Discord Rich Presence for Team Fortress 2

![Preview image](preview.png)

(The actual program is nowhere near as nice looking as this)

## Download
With self-extractor: [tf2_rich_presence_{tf2rpvnum}_self_extracting.exe](https://github.com/Kataiser/tf2-rich-presence/releases/download/{tf2rpvnum}/tf2_rich_presence_{tf2rpvnum}_self_extracting.exe) ({installer_size} MB)  
Extract it yourself: [tf2_rich_presence_{tf2rpvnum}.zip](https://github.com/Kataiser/tf2-rich-presence/releases/download/{tf2rpvnum}/tf2_rich_presence_{tf2rpvnum}.zip) ({zip_size} MB)

## Installation and running
1. Extract `tf2_rich_presence_{tf2rpvnum}.zip` OR run `tf2_rich_presence_{tf2rpvnum}_self_extracting.exe`, whichever you downloaded.
2. Run `Launch TF2 with Rich Presence.exe`.
	- OR run `Launch Rich Presence alongside TF2.exe`. This one doesn't automatically start Team Fortress 2.
	- Both require Steam and Discord to be running as well.

For faster launching, you can add the first EXE to your taskbar/start menu/desktop, or to Steam as a non-Steam game.

## Changelogs
- [Changelogs.html](https://htmlpreview.github.io/?https://github.com/Kataiser/tf2-rich-presence/blob/master/Changelogs.html)
- [Releases](https://github.com/Kataiser/tf2-rich-presence/releases)

## Building from source
For making and testing changes, or simply always running the most up-to-date code. (Windows only)
1. Either clone the repo or [download the source](https://github.com/Kataiser/tf2-rich-presence/archive/master.zip).
2. Copy the entire source to another location and put the files outside of `TF2 Rich Presence` into that folder.
3. Extract `TF2 Rich Presence\python-3.7.5-embed-win32.zip`.
4. Make sure the `python` and `pip` commands point to Python >= 3.7.
4. From within `TF2 Rich Presence`, run `pip install -r requirements.txt` and `python build.py`.
