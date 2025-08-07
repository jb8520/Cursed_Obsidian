# Cursed_Obsidian

Cursed Obsidian Bot is a specialised Discord bot built for the [Cursed Obsidian](https://discord.gg/57BurZrTYH) server, which focuses on the game Sea of Thieves. Designed to manage large-scale server coordination, player queues, in-server moderation, and security checks, the bot automates nearly every aspect of an otherwise intensive manual process — from session maintenance to queue processing, and even Xbox-integrated ban enforcement using the Xbox Web API.

Originally tailored for a close-knit, admin-run environment, the bot enables high-efficiency control of what's known as a *Sea of Thieves alliance server* — a type of setup that provides a safe, cooperative space for players to farm and explore. The introduction of this bot eliminated the need for cthe onstant staff oversight, that would come from the otherwise heavy involved managment process.

For help, support, or more information about the bot, please contact the original developer (jb8520) or refer to the command documentation below.



## Why Use Cursed Obsidian Bot?

Running an *alliance server* in *Sea of Thieves* requires coordination, queue handling, moderation, and plenty of time invested... unless you’ve got this bot.

Originally built for the [Cursed Obsidian](https://discord.gg/57BurZrTYH) server, the bot has since been designed to be easily configurable and modular — meaning any server offering similar services can set it up with minimal effort.

**Cursed Obsidian Bot** was created to eliminate the constant grind of admin tasks, automating everything from fleet creation to ship queueing, with smart logic and security checks powered by the Xbox API, integrated across a *banlist* database.

Whether you're hosting one fleet or six all at once, this bot gives your staff team the tools to manage *dozens of players in real-time* without the usual chaos. With auto-permission control, voice channel management, and crash recovery features, it transforms chaotic session management into a visually appealing, smooth experience.

Whether you are building an *alliance server* for the first time or bringing one back to life, this bot makes it not just possible - but **actually** sustainable and worthwhile.



## Features

<!-- tbd -->



## Getting Started

### Prerequisites

- Python 3.11+
- A Discord bot application created in the [Developer Portal](https://discord.com/login?redirect_to=%2Fdevelopers) (you'll need the bot token)
- MySQL Server (or compatible)
- Packages (requirements.txt):
    - discord.py==2.5.2
    - mysql-connector==2.2.9
    - python-dotenv==1.1.0
    - xbox-webapi==2.1.0


### Installation

```bash
git clone https://github.com/jb8520/cursed_obsidian.git
cd cursed_obsidian
pip install -r requirements.txt
```

Create a `.env` file (in the root) and add your Discord bot token and database credentials (mysql.connector specific in this example):
```ini
BOT_TOKEN=

DATABASE_HOST=
DATABASE_NAME=
DATABASE_PASSWORD=
DATABASE_USER=
```

Also, create a `tokens.json` file (in the root) and add the Xbox WebAPI credentials (detailed below).



## Usage

Run the bot:
```bash
python main.py
```



## Setup & Configuration

⚠️ A majority of features require proper server setup (e.g. correct channels, roles, and embeds). See the `Setup.txt` file for detailed instructions to reach the proper setup. If you need additional help please contact the original developer jb8520 either on Github or on Discord (username is the same on both).



## Commands

#### Supported Commands

**General:**


**Queue:**
<!---->

**Send Reminders/Information:**
<!---->

**Other:**
<!---->





## Contributing

Pull requests and issues are welcome! Please follow the coding style and add tests where possible.



## License

GNU AFFERO GENERAL PUBLIC LICENSE Version 3, © jb8520, James Boss