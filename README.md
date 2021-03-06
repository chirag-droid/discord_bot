# discord_bot

[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/chirag-droid/discord_bot/main.svg)](https://results.pre-commit.ci/latest/github/chirag-droid/discord_bot/main)

Hi, :wave: welcome to my discord bot. This is just a small project for making me learn about open source, using github actions, git version control. The bot is not currently public but you can self host it. See [how to host](#host)

## <a id="contribute">How to contribute</a>

Although this is just a small personal project, it is open to contributions. The code follows flake8, black, isort for liniting. Please make sure your code follows these guidelines before contributing. You dont need to install these manually. After seting up a poetry env, these tools should be installed. The project has a pre-commit hook which will lint your code automatically before committing. You can maually lint the code using

```sh
poetry run task lint
```

> Note make sure your pre-commit is setup, to set it up for first time do

```sh
poetry run task precommit
```

## <a id="host">How to host</a>

The root dir contains a file called [ex_config.yml](./ex_config.yml), this is the default config file, for making changes to it make a new file called config.yml, and continue.
The default config uses a environment var to get token which is more secure, but you can set it to a string to. (Not recommended)
After making changes to your configuration if any you can deploy it locally, on heroku, or any other platform.

### Locally

First check that your python version is 3.9.6, and install poetry using

```sh
python3 -m pip install poetry
```

After poetry has been installed, run poetry install in the root dir, this will install all dependencies. Now you can run the bot using

```sh
poetry run task start
```

> Note: if you are using default config you need to create a env variable called BOT_TOKEN with the value of your bot's token

### On heroku

As heroku doesn't support poetry, a poetry buildpack is used ```https://github.com/moneymeets/python-poetry-buildpack.git```.
Both heroku/python and poetry buildpack are used.
Now make a new key named BOT_TOKEN with value of your bot's token. And continue.
