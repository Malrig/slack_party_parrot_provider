# Slack Party Parrot Provider
[![Build Status](https://travis-ci.org/Malrig/slack_party_parrot_provider.svg?branch=master)](https://travis-ci.org/Malrig/slack_party_parrot_provider)
[![Coverage Status](https://coveralls.io/repos/github/Malrig/slack_party_parrot_provider/badge.svg?branch=master)](https://coveralls.io/github/Malrig/slack_party_parrot_provider?branch=master)

This Slack App allows users to effortlessly add new party parrots from existing emojis using the slash command `/produce_party_parrot {emoji_name}`.

## Available Slash Commands / API Endpoints

This App currently implements the following slash commands / API endpoints:
* `/hello_world` - This simple endpoint just returns `Hello World!`, it is useful for verifying the apps connectivity.
* `/produce_party_parrot` - The meat of the app, as a Slack command it accepts an emoji and will create a party parrot using [Party Parrot as a Service](https://parrotify.github.io/) and then upload it to the Slack team as an available emoji.

## Setup
The app is currently a work in progress and so is not available through the Slack app directory. Instead to add this to your team you are required to host a copy of this repository and point a custom Slack app to the endpoints there.

Note that you are required to host at a `https` end point otherwise Slack will refuse to send/receive any messages with the backend.

### Running Locally
To run locally clone the master branch of this repository using Git. Then create a Python virtual environment:
```
pip install virtualenv
python -m venv venv
```
activate it, either `venv\Scripts\activate` on Windows or `. ./venv/bin/activate` on Linux. Then install the requirements:
```
pip install -r requirements.txt
```
Then start the app using `python run.py` which should start it at `http://localhost:5000`, you should be able to test that it is up and running by visiting `http://localhost:5000/hello_world`.

### Running unit tests
You can run the unit tests using any test runner you wish. To use the inbuilt runner use `python -m unittest discover`.

### Configuration required
For the backend to work correctly it needs several bits of information to be provided in a `.env` file. This should look something like;
```
WEB_ROUTE="[Web Base Path]"
VERIFICATION_TOKEN="[Slack App Verification Token]"
OAUTH_ACCESS_TOKEN="xoxp-[Access Token]"
TEAM_COOKIE="[Very Long Cookie]"
```
and it should be saved in the root directory of your app (alongside the `index.py` file).

This configuration is:
* `WEB_ROUTE` - This is the base web path for your application and can make hosting behind a reverse proxy easier.
Example: if `WEB_ROUTE="/party_parrot_url"` then your app would be hosted at `http://localhost:5000/party_parrot_url`.
* `VERIFICATION_TOKEN` - This is the old way by which Slack app backends verify that they have received a message for the actual app. Details of how to retrieve this are [here](#Creating-your-Slack-App).
* `OAUTH_ACCESS_TOKEN` - This is required so that the backend can retrieve the list of custom emoji's available to your team. Details of how to retrieve this are [here](#Creating-your-Slack-App).
* `TEAM_COOKIE` - This is used to actually upload the new emoji's into Slack (unfortunately there is no API for doing this currently). To find this you need to:
  1. Go to the emoji customisation page of your Slack team.
  2. Open up the developer tools for your browser (on Chrome this is `F12`).
  3. Open the Networking tab of the developer tools and refresh the page.
  4. Find the request called `emoji` (it should be one of the first there).
  5. Open up that request and copy the entire cookie on the request header, it should look something like;
  ```
  b=.6li91dh3iig18kst222y6fq95; utm=%7B%22utm_source%22%3A%22messagemenu%22%2C%22utm_medium%22%3A%22inprod%22%2C%22utm_campaign%22%3A%22inprod%22%2C%22utm_content%22%3A%22overflow-more+actions%22%7D; d=ScFjqIUIb5uqciEtKCdLcgbPFSWQL3hrf8vl6h1ulvJkUz6RrDek26fuNXZ4Bofef3HGY0uuE0TxjMVnAi0HRyhsiOYoXTmaKDF8uGlVBUhP1msWntJ91Lhryx3QoXuaeyIkt5fJ8Fic9LlsX23mSgYJkO95mPXb9W7rTbFxwr2pJdUV6xunOtUZiyOaMAJ1260AJr3aMCU79YYxtlFt4n3W3UVicGeqnlQn5ujo8lxIBhzA84xFuR%3D%3D; d-s=1714128213; lc=1714128213
  ```

### Creating your Slack App
1. Go [here](https://api.slack.com/apps?new_app=1) to create your Slack App, give it a name and assign your Slack team as the Development workspace.
2. Note down teh verification token under "App Credentials" and copy it into your `.env` file.
3. Create your slash commands by first clicking the "Slash Commands", "Create New Command" and then enter the required information for each slash command that you want to implement.
3. Go to the "OAuth & Permissions" tab and scroll down to "Scopes". Add the `emoji:read` permission to your app. (You should now have two permissions; one for emojis, and one for slash commands).
4. Install the app to your Slack team using the button at the top of the page. Note down the OAuth access token given and add to your `.env` file.

Once you have completed the above instructions you should be able to issue slash commands from Slack and have them received at your backend and handled.