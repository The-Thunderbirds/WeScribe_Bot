# WeScribe Discord Bot

WeScribe Bot is a part and additional service provided by our WeScribe which helps in enhancing the participation, sharing and collaboration among students of an organization. It has many options such as sharing PDFs, useful links, images, getting auto-notifications about upcoming lectures or events, XP, levels, etc.

# Installation

1. Install pipenv
2. ```pipenv shell```
3. ```pipenv install -r requirements.txt```

# Usage

1. Create a discord application in discord developers website. Make a bot application inside it and take down its TOKEN.
2. Make a .env file in the root of the main folder
3. Fill all the necessary environment variables
   ```
    DISCORD_TOKEN=" "
    GUILD=" "
    LOG=" "
    BOT_ANNOUNCEMENTS=" "
    STUDENT=" "
    CR=" "
    CR_NAME=" "
    TZ="Asia/Kolkata"
    ```

    where LOG is log-channel id, BOT_ANNOUNCEMENTS is bot-announcements id, STUDENT is student role id, CR is cr role id in your discord server. You can use the [template](https://discord.new/ekSk9a3SsHSP) to create a WeScribe Template server.

4. Edit settings.py if required
5. RUN python3 Main.py