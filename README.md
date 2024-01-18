# NOTE: This project has been deprecated due to a change in the Riot Games API :(
# Gromp Bot Backend
This repository holds the backend application for the discord bot that goes by the name "Gromp Bot".

Gromp Bot is a discord bot which provides easy accessibility to build, and rune information for the playable champions in League of Legends. This information makes sure that you are getting the most out of the champion you pick to play.

## What is League of Legends?

[League of Legends](https://www.leagueoflegends.com/en-us/) is a online multiplayer video game. Playing the game consists of participating in a 5v5 match that lasts ~30-45min. A game is won when one team destroys the other team's home base. 

During each match players play as one of 140+ characters which are referred to as "champions". Each champion has a different set of abilities and a different role to play in the team. Players will also accumulate gold throughout a match, which can be spent on different items which make that player stronger during the match. 

### What is Gromp Bot's role?
There are over 200 items a player can buy throughout a match, but only 6 can be held at a time. This leaves over 80 billion different possibilities for what set of items can be chosen! This is where the Gromp Bot can help. Gromp Bot will display an infographic to the player depending on the champion they are playing. This infograpic will tell the player the best combination of items and runes that they can use to maximize their chances of success on a given champion.



## Try it out in Discord!
Gromp Bot has a dedicated testing ground where you can try out the bots functions for yourself!

Join the testing discord: https://discord.gg/vNqKQZwQ

Try using the command: 
```
#champ <champion_name>
```
Some champion names can include Annie, Aatrox, and Camille.

Click [here](https://www.leagueoflegends.com/en-us/champions/) for a full list of champion names.

## Running it locally
Getting the Gromp Bot backend up and running locally requires the following steps:

1. Cloning from the local_dev branch! The dev and main branches of this project are both setup with production database settings. Technically you can clone from those and then just swap the database, but its much simpler to simply clone the local_dev branch and save yourself the trouble. 

2. Running inside Docker. This project comes with a docker-compose file I used for local development. To start playing with it yourself, simply run the following inside the project directory:
```
docker-compose build
docker-compose up -d
docker exec -it league_app_container /bin/bash
```

From here you can start playing with the management commands available in the project. To view your local database, visit pgadmin at localhost:5050 and login with:

- user: admin@admin.com
- pw: root


## A High-level View of the Architecture

<img src="https://league-bot-image-bucket.s3.amazonaws.com/readme_pictures/Highest_Level.png"/>


Above you can see a high level view of how the bot presents data to the user. 
The backend will ingest and transform data every 24 hours in the following manner:

1. An API request for data on a random sample of highly skilled players is made to the Riot Games API. 
2. Transform that data and insert it into a PostgreSQL database. 
3. Use the data in the database to develop more insights and insert those into their own database tables.
4. Use the transformed data and insights to create infographics displaying the information. Upload the infographics to S3 bucket.
5. When discord users request information on a certain champion, retrieve the most recent corresponding infographic and display it to the discord chat.

#### NOTE:
The last step is actually the job of the frontend discord bot. It was included to give you a complete view of the functionality present in this project.


## A Deeper Look

This section will be dedicated to taking a deeper look at how the Gromp Bot functions. For those of you that are interested, keep reading!

### Functionality
The functionality of the Gromp Bot can be broken down into three major categories. 

1. The ETL operations on Riot Games API Data
2. Using the extracted data to develop further insights.
3. Creating and storing infographics to present the insights.

### 1. ETL Operations on Riot Data

These operations are tasked with ingesting sample data into a PostgreSQL database, from which insights can be extracted. The goal of the ETL step is to produce a dataset where each entry describes a player's experience in a given match of League of Legends.

For example, an entry in this data holds info such as:

- the player's name
- the champion the player chose
- which items the player bought during the match
- did the player's team win or lose?
- the amount of kills, deaths, and assists the player scored
- the id of the match that this entry describes
- etc..

This dataset can then be used to derive insights on things such as:

- which items are better on certain champions
- the winrate of different champions
- which runes are better on different champions
- etc..

The ETL operations are performed in the following steps:

1. Request the names of a random sample of highly ranked players from the Riot Games API.
2. Gather the match_ids for the recent matches played by each player and store those in a "Match Table".
3. Look at the performance of each player and create entries in the "Participant Table" to store this information.

Once these operations of done the Participant and Match tables in the database should be updated. Below shows an quick example of what they look like.

<img src="https://league-bot-image-bucket.s3.amazonaws.com/readme_pictures/PartandMatchERD.png"/>


### 2. Developing Insights

The second piece of functionality the backend provides is insight development. The backend develops insights beyond what is given by the Riot Games API. This means looking at the sample data collected in the ETL step and using it to create and store more useful data!

Currently the backend focuses its efforts on providing insights for individual champions. There are four major champion insights that are developed currently.

1. The number of matches the champion was played in.
2. The % of matches played by the champion which ended in a win by the champion's team.
3. The most played item build for the champion.
4. The most played rune build for the champion.

However, in order for these insights to be relevant day-to-day the backend needs someway of updating them as new data is ingested in the first ETL step. This is where django management commands are used. 

Django management commands are ways of writing custom command line commands. In this case the backend has a command called update_stats. When this command is run it will re-calculate all the insights with any new data that has been ingested.

Finally, these commands are set on a schedule using Heroku Scheduler. This means that they are run every 24 hours whenever new data is ingested through the ETL step. This allows for all insights to stay up to date with the current data.

### 3. Generating Infographics

Insights are great and all, but they mean much if a user can't read them.

The final piece of functionality provided by the backend is the generation of infographics. The purpose of these graphics is to display the insights in a way that is easy to read and pleasing to the eye. 

Here is what a raw infographic for a champion looks like:

<img src="https://league-bot-image-bucket.s3.amazonaws.com/readme_pictures/Aatrox08-20-2022.png"/>

Here is what a infographic looks like when posted to a discord channel:

<img src="https://league-bot-image-bucket.s3.amazonaws.com/readme_pictures/AatroxScrnsht.png"/>

These graphics are constructed with PIL; an image manipulation package for Python. The generation of these images is controlled by another django command (generate_images). This command looks at the insights stored in the database to then generate an image that will display such information.

Since the insights are stored in the database, the generate_images command has to first retrieve that information, and then use it to download the correct images from the S3 storage, where all the asset images are stored.


## Future Development Plans

Currently this project is in the MVP stage of development. The end-to-end product is working, yet there are still so many more insights and feature I would like to add. Currently a list of those feature are:

1. Insights in a specific players performance
2. Graphs for player performance overtime
3. More robust support for changes to League of Legends (if the game is updated)

Although for now this project is what I have and I hope you enjoy playing around with it!

 













