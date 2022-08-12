# Gromp Bot Backend
This repository holds the backend application for the discord bot that goes by the name "Gromp Bot".

Gromp Bot is a discord bot which provides easy accessibility to build, and rune information for the playable champions in League of Legends.

## What is League of Legends?

League of Legends is a online multiplayer video game. Playing the game consists of participating in a 5v5 match that lasts ~30-45min. During each match players play as one of 140+ 

## Run it locally!
Getting the Gromp Bot backend up and running locally requires the following steps:

1. Cloning from the local_dev branch! The dev and main branches of this project are both setup with production database settings. Technically you can clone from those and then just swap the database, but its much simpler to simply clone the local_dev branch and save yourself the trouble. 

2. Running inside Docker. This project comes with a docker-compose file I used for local development. To start playing with it yourself, simply run the following inside the project directory:
```
docker-compose up -d
docker exec -it league_app_container /bin/bash
```

From here you can start playing with the management commands available in the project. To view your local database, visit pgadmin at localhost:5050 and login with:

- user: admin@admin.com
- pw: root


## A High-level View of the Architecture

<img src="https://league-bot-image-bucket.s3.amazonaws.com/readme_pictures/Highest_Level.png"/>


Above you can see a high level view of how the bot transfers data to the user. 
The backend will ingest and transform data every 24 hours in the following manner:

1. Request data on a random sample of highly skilled players from the Riot Games API. 
2. Transform that data and insert it into the PostgreSQL database. 
3. Use the stored data to develop more insights and insert those into their own database tables.
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

These operations are tasked with ingesting sample data from which insights can be extracted. The goal of this function is to produce a dataset where each entry in describes a players experience in a given match of League of Legends.








