# yvy-discord-bot
discord bot for pulling recent plays from osu!

I just made a new github because my last one was all over the place with unfinished projects. I had a few prior commits that better
showed what was happening as time progressed but I have a written timeline of my thoughts in the working code files. 

The unfinished, poorly written code that is not in use and has been refactored is in the dead code section of the files. 

Yvy bot stores a users osu! profile in a mongoDB database, connecting the account with their DiscordID. There are just a few simple discord bot 
commands that pull data from the osu! api and return it in a discord embed. 

Commands can be found by using *help in the discord yvy is active, but will be listed here as well.

Aside from a few general commands, each osu! command requires a second argument that specifies the player. 
If an osu! account is already connected to a discord user, then the osu! account will automatically be used as the profile for each command. However, it can still be overwritten if the user enters a seperate osu! profile name. 
If no account is pre specified, then an error will be thrown if the commands are being used without specifying the profile. When this happens, the user is prompted to use the *setprofile command to link their discord account with their osu! profile

osu! commands are as follows
- *setprofile
  This simply links the discord user to their osu! profile. There is no authorization and this can be changed as many times as the user would like just by using the
  command again. What is stored in the MongoDB database is their discord ID, discord name, osu! profile, what discord and channel they joined from, the time in which
  they first linked their accounts, when they last changed their linked profile, as well as the amount of times they have used the bot. 

- *osu
  This is a profile overview. Using the osu! profile argument, some information about the users osu! profile (link, name, highest play, overall ranking, etc.)
  is pulled from the discord API and condensed into a discord embed to be sent to the channel in which the discord user used the command.
  
 - *recent / *r
  This is a method to return the most recent score an osu! player received, including failures. If no play has been submitted in the past 24 hours, no play will be found
  and that will be displayed to the user. Hwoever if a play was found, it will give you statistics on the play such as the score, ranking, miss count and some others
  and display them in a discord embed. 
  
 A real challenge for me was making sure the token was refreshed, as the token given from the osu! API was changed every 24 hours. 
 With Oauth 2.0, a second key is usually given if the token is to be refreshed after a certain time, but after digging I didn't find a refresh token given to me and instead wrote a method that would refresh the token every 80,000 seconds.
 
 I now have the discord bot running locally from a raspberry Pi in order to keep it running around the clock. 
 
Using the discord API was one of the first things I did while learning python and always kept project ideas using it in the back of my mind while continuing to learn python. After becoming comfortable enough with my abilities, I dove head first into this project and dedicated a lot of time into creating this bot. 
I learned many new abstract concepts and the art of refactoring while creating this bot, alongside knowledge and experience that I will take with me into more passion projects I pursue in the future. 
