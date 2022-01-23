<h1 align="center">OBS Remote Controller</h1>

This program allows to remotely **change between scenes by reacting to emojis** in a [Discord](https://discord.com) text channel.

## Example

![embed](/assets/embed.png)
![example-gif](/assets/example.gif)
## Requirements
- [Python](https://www.python.org/downloads/) 3.8.x
- [Discord.py](https://github.com/Rapptz/discord.py) latest
- [OBS Studio](https://obsproject.com/) >= 27.1.3
- [obs-websocket](https://github.com/obsproject/obs-websocket/releases/tag/5.0.0-alpha3) >= 5.x.x
- [simpleobsws](https://github.com/IRLToolkit/simpleobsws/tree/master) >= 1.x.x

## Getting Started

To get everything working properly, follow these steps:
1. Install every requirement above
2. Get the Discord bot token and then replace in config.json
3. Set the OBS websocket port and password and then replace in config.json
    - Recommended to keep the default port, 4444
4. Run `connector.py` script
5. Invite the bot to your Discord server
6. Send `$setup` in any text channel
    - A channel will be created with the name in `config.json`

Obs: The IDs will be filled automatically in the step 6.

> config.json
```json
{
    "discord_token": "",
    "obs_url": "ws://localhost:4444",
    "obs_password": "123456",
    "update_time": 2,
    "channel-name": "controller",
    "guild-id": null,
    "channel-id": null,
    "msg-id": null
}
```

## Known Issues
- Discord requests are too fast and the bot is being rate limited
- OBS sometimes crashes when is closed while the controller is still running