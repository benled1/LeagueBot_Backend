# Gromp Bot Backend
This repository holds the backend application for the discord bot that goes by the name "Gromp Bot".

Gromp Bot is a discord bot which provides easy accessibility to build, and rune information for the playable champions in League of Legends.

## A High-level View of the Architecture

<img src="https://league-bot-image-bucket.s3.amazonaws.com/readme_pictures/Highest_Level.png"/>

## Functions of the Backend

1. Ingests data from the Riot Games API to a PostgreSQL database about matches that have been played recently.
2. Calculates statistics on the winrates, item builds, and rune builds for different champions based on the data ingested.
3. Generates infographics to present this information and stores them in Amazon's S3 bucket.




