# discord_bot

Hi, :wave: welcome to my discord bot. This is just a small project for making me learn about open source, using github actions, git version control. The bot is not currently public but you can self host it. See [how to host](#host)

## <a id="host">How to host</a>
The root dir contains a file called [ex_config.yml](./ex_config.yml), this is the default config file, for making changes to it make a new file called config.yml, and continue.
The default config uses a environment var to get token which is more secure, but you can set it to a string to. (Not recommended)
After making changes to your configuration if any you can deploy it locally, on heroku, or any other platform.
### Locally
First check that your python version is 3.9.6, and install poetry using
```
python3 -m pip install poetry
```
After poetry has been installed, run poetry install in the root dir, this will install all dependencies. Now you can run the bot using
```
poetry run task start
```
> Note: if you are using default config you need to create a env variable called BOT_TOKEN with the value of your bot's token

### On heroku
As heroku doesn't support poetry, a poetry buildpack is used ```https://github.com/moneymeets/python-poetry-buildpack.git```.
Both heroku/python and poetry buildpack are used.
Now make a new key named BOT_TOKEN with value of your bot's token. And continue.
