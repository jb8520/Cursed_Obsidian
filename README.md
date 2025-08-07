# Cursed_Obsidian

**Cursed Obsidian Bot** is a specialised Discord bot built for the [Cursed Obsidian](https://discord.gg/57BurZrTYH) server, which focuses on the game *Sea of Thieves*. Designed to manage large-scale server coordination, player queues, in-server moderation, and security checks, the bot automates nearly every aspect of an otherwise intensive manual process — from session maintenance to queue processing, and even Xbox-integrated ban enforcement using the Xbox Web API.

Originally tailored for a close-knit, admin-run environment, the bot enables high-efficiency control of what's known as a *Sea of Thieves alliance server* — a type of service that provides a safe, cooperative space for players to farm and explore. The introduction of this bot eliminated the need for constant staff oversight that would have otherwise been required due to the heavy manually intensive management process.

For help, support, or more information about the bot, please contact the original developer (jb8520) or refer to the command documentation below.



## Why Use Cursed Obsidian Bot?

Running an *alliance server* in *Sea of Thieves* requires coordination, queue handling, moderation, and plenty of time invested... unless you’ve got this bot.

Originally built for the [Cursed Obsidian](https://discord.gg/57BurZrTYH) server, the bot has since been designed to be easily configurable and modular — meaning any server offering similar services can set the bot up and use it with minimal effort.

**Cursed Obsidian Bot** was created to eliminate the constant grind of admin tasks, automating everything from fleet creation to ship queueing, with smart logic and security checks powered by the Xbox API, integrated across a *banlist* database.

Whether you are building an *alliance server* for the first time or bringing one back to life, this bot makes it not just possible - but **actually** sustainable and worthwhile. Managing **hundreds** of users in real time has never been easier.



## Features

- **Write-Ahead Logging (WAL) for State Preservation:** Ensures full in-memory state is recoverable after restarts or crashes, enabling seamless session continuity with no manual intervention.
- **Automatic Infrastructure Setup:** A setup command that can be run at any point to automatically create all necessary infrastructure (if any) required for the bot to operate.
- **Fleet & Ship Management:** Dynamically handles fleet creation + management, tracks ships in real-time, and creates a seamless graphical queueing system for players.
- **Staff Commands:**: Allows for easy control in regards to the moderation of the *alliance servers*, significantly reducing workload of staff.
- **Role-Based Staff Command Access:** Built-in tier system lets you define granular staff permissions, supporting multiple levels, ranging from member tiers up to server admins.
- **Integrated Banlist with Xbox API Support:** Optional but powerful — ties Discord users to Xbox gamertags, enforcing bans across various alt accounts, resulting in player validation using live Xbox data.
- **Fully Modular System:** Uses Cog-based architecture, with separated Views, Utils, and Config — making the codebase extendable and easy to understand/modify.
- **Customisable Text & Embeds:** Easily edit preset bot messages, embed titles, and descriptions to match your server’s theme and tone.
- **Granular Permission Control:** You decide exactly what roles can access which command tiers — all via a clean values.json config.



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

> If you wish to use the the banlist/Xbox checker system, you will also need to set this up. See the **Xbox API Setup Guide** section for this.


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



## Setup & Configuration

Add the following IDs to `Configuration/values.json` (replace the placeholder of 0):
- other
    - **`guild_id`**: the ID of your discord server
- roles
    - **`member`**: the ID of your server's generic *member role* (everyone has this role).
    - **`staff`**: the ID of your server's staff role.

> These IDs can be found by enabling Developer Mode in Discord and right-clicking the relevant role/channel/server to copy ID. See [Discord's guide](https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID) for more info.


Decide on what roles you would like to be in which permission tier:
- Tier 0 represents what everyone can do
- Tier 1 restricts *base staff commands*
- Tier 2, 3 and 4 follow in this pattern, the higher the number, the more control over the features of the bot is available.

Suggestions for both role names and tier layout is presented in `Configuration/values.json`, however this is fully customisable.
The suggested roles are:
- `admin`
- `senior_mod`
- `mod`
- `officer`

If you wish to change the roles, simply add to or delete from the roles listed above, in the file. the format should be: `"role_name": role_id,`.
To set the tiers, simply put the `role_name` in each tier's list.


If you wish to customise the text the bot uses (such as in embeds or channel names), simply customise the text in the following places:
- At the bottom of `Configuration/values.json`:
    - queue_title
    - queue_description
- `Configuration/preset_text.py`

The position of each category and its channel's permissions can also be changed. These options are also found in `Configuration/preset_text.py`.


If you are using the banlist/xbox checker integration, please also create a *linked xbox role* in your server and add its ID to the `"xbox_linked"` role in `Configuration/values.json`.


If you need additional help please contact the original developer jb8520 either on Github or on Discord (username is the same on both).



## Xbox API Setup Guide

**Step 1:**
1. Go to https://portal.azure.com/
2. Create a new Azure AD app (Search "App registrations")
3. Register it with:
    Redirect URI: https://localhost (or whatever you want)
4. Grab your Application's client_id and and client_secret

**Step 2:**
Run the provided auth script:
```bash
python Utils/xbox_auth.py
```
1. Open the printed login URL and sign in to your xbox account
2. After authenticating, you’ll be redirected to a URL similar to:
```ini
https://localhost/?code=ABC1234...&state=xyz
```
3. Paste the full redirected URL into the script prompt
4. The script will save your access and refresh tokens to a file called tokens.json
5. Ensure `tokens.json` is in the root directory (same level as `main.py`), a blank copy is included in the codebase to show where it should be located



## Usage

Run the bot:
```bash
python main.py
```



## Commands

> Format is:
> - **`/command_name`** (Permissions to use the command): description of the command.

### Slash Commands

#### General:
- **`/bot-info`**  (`Tier 0`): displays information about the bot, such as latency and uptime.
- **`/ping`**  (`Tier 0`): displays the latency of the bot.


#### Setup:
- **`/setup-all`**  (`Tier 4`): creates or recreates/fixes all the infrastructure the bot needs to function.


#### Fleet:
- **`/create`**  (`Tier 3`): creates a fleet. This includes all the required channels, roles, and control panels (ie the panels to open/close and unlock/lock the fleet vcs).
- **`/delete`**  (`Tier 3`): deletes a previously created fleet.
- **`/rename`**  (`Tier 1`): renames a specific fleet vc.
- **`/ship-size`**  (`Tier 1`): sets the vc limit of a specific fleet vc.


#### Queue:
- **`/queue-process`**  (`Tier 1`): processes the specified user onto the chosen fleet vc, when a spot has opened for them.
- **`/queue-insert`**  (`Tier 1`): inserts the specified user into the queue at a specific position.
- **`/queue-remove`**  (`Tier 1`): removes the specified user from the queue.


#### Send Reminders/Information:
- **`/start-loop`**  (`Tier 1`): starts the specified fleet's hourly information sender.
- **`/stop-loop`**  (`Tier 1`): stops the specified fleet's hourly information sender.

The following send preset information:
- **`/goldrush`**  (`Tier 0`)
- **`/spike`**  (`Tier 0`)
- **`/stacking`**  (`Tier 0`)
- **`/ritual-skulls`**  (`Tier 0`)
- **`/rogue`**  (`Tier 0`)


#### Banlist/Xbox Checker:
- **`/banlist-case`**  (`Tier 1`): displays the information for a specific ban case ID.
- **`/banlist-add`**  (`Tier 3`): adds the specified xbox and/or discord account to the banlist.
- **`/banlist-delete`**  (`Tier 3`): removes the ban associated with the specified ban case ID.

- **`/user-check`**  (`Tier 1`): runs a banlist check on both the user supplied and their xbox friends. If there are no bans, the user is given the `staff-verified` role.
- **`/lookup`**  (`Tier 1`): displays information about the specified xbox account.


### Prefix Commands
- **`.sync`**  (`bot owner only`): syncs the command tree.
- **`.shutdown`**  (`bot owner only`): induces a safe shutdown.
- **`.say`**  (`requires admin`): the bot will send a message containing the specified text.



## Contributing

Pull requests and issues are welcome! Please follow the coding style and add tests where possible.



## License

GNU AFFERO GENERAL PUBLIC LICENSE Version 3, © jb8520, James Boss