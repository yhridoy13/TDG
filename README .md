# Discord Tournament Bot

A Discord bot for managing tournaments and teams with 24/7 uptime.

## Features

- Welcome messages with personal DM notifications
- Team management (6 players per team)
- Team registration with automatic role creation
- Tournament announcements
- Match reminders via DM
- 24/7 uptime capability

## Setup Instructions

### 1. Create a Discord Bot

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application"
3. Name your application (e.g., "TournamentBot")
4. Go to the "Bot" tab
5. Click "Add Bot"
6. Enable these privileges:
   - **MESSAGE CONTENT INTENT**
   - **SERVER MEMBERS INTENT**
7. Click "Reset Token" and copy the token

### 2. Get Server and Channel IDs

1. In Discord, enable Developer Mode:
   - User Settings > Advanced > Developer Mode
2. Get Server ID:
   - Right-click your server icon > "Copy Server ID"
3. Get Channel IDs:
   - Right-click welcome channel > "Copy Channel ID"
   - Right-click tournament channel > "Copy Channel ID"

### 3. Deploy on Replit

1. Create a new Repl at [replit.com](https://replit.com)
2. Import this repository
3. Set environment variables:
   - Click the lock icon (Secrets) in the left sidebar
   - Add the following secrets:
     ```
     DISCORD_TOKEN=YourBotTokenHere
     SERVER_ID=YourServerIDHere
     WELCOME_CHANNEL_ID=YourWelcomeChannelIDHere
     TOURNAMENT_CHANNEL_ID=YourTournamentChannelIDHere
     ```
4. Click the "Run" button to start the bot

### 4. Invite Bot to Your Server

1. In Discord Developer Portal:
   - Go to "OAuth2" > "URL Generator"
   - Select scopes: `bot` and `applications.commands`
   - Under "Bot Permissions":
     - Administrator (or select specific permissions)
     - Send Messages
     - Embed Links
     - Manage Roles
   - Copy the generated URL
2. Paste URL in browser and invite bot to your server

### 5. Set Up 24/7 Uptime

1. After running, Replit will show a web server URL
2. Go to [UptimeRobot](https://uptimerobot.com/) and create a free account
3. Click "Add New Monitor"
4. Set:
   - Monitor Type: HTTP
   - URL: Your Replit URL
   - Monitoring Interval: 5 minutes
5. Click "Create Monitor"

## Commands

- `/register_team [team_name]` - Register a new team
- `/add_player [@player] [team_name]` - Add a player to your team
- `/announce_tournament [details]` - Announce a new tournament

## Important Notes

- This bot uses in-memory storage. Teams will reset when the bot restarts.
- For production use, consider adding a database for persistent storage.
- The match reminder system sends hourly test messages. Customize as needed.