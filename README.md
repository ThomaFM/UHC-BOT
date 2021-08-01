# UHC-BOT
This is the Open Source Version of the UHC BOT on the Apollo Discord, this code may not reflect the bot's active running code

main.py is the bot's code, right now it's not split into classes or using the cog's feature for discord.py mostly because when i started this projected i didn't expect for
it to spiral out of controll and become a big mess. I may refactor it eventually in the future but for now development on this has likely stopped.

UHC BOT is a folder containing files that the bot uses, this includes texture folders for !loot as well as storage files that are made throught the python pickle library allowing for persisten
variable storage acrossed bot restarts, the bot should automatically create these folders if they do not exist in your environment.

All API tokens are stored in environmental variables that are obviously not shown on this github repo, if you want to use this code or test it you must make your own api keys and either set
them as environmental variables or change the code to store them as raw variables (don't do this if you plan on hosting this in a public way)

You are free to use any of the code in this repo and make pull requests if you want. Though if you do use any of the code or the bot its self you should tell me, not to ask for permission 
you don't need my permission but rather to just let me know that someone is actually using something i created.
