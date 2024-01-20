# goodnight_bot
discord goodnight bot to reply to goodnight messages in #general

this is less of code and more of art. the wording, the architecture, its all with purpose /s. Debugging and deploying this on an nvidia jetson was a pain but the process is easy not. push from desktop and login to the tmux on the jetson and pull to restart. the code takes care of the rest assuming I keep the api key.  

just practicing python and discord bots. 

# main.py

contains python script for the bot. the main functionality is listening for "goodnight" or "gn" messages, liking them, and responding with "Goodnight :)"

this needs to be run in the background somewhere in order for the bot to work. 


# TODO

- [ ] point based chance for rare goodnight based on 
    - muting
    - time spent in channel
    - time since last goodnight
    - streaming
- [ ] convert quotes to json files


# To Install

I followed this guide to make a bot

[Creating an application using discord developer portal](https://discord.com/developers/applications)

[Read Discord chats with Python](https://blog.tinq.ai/read-discord-chats-with-python/)

[Client parameters in python](https://stackoverflow.com/questions/71959420/client-init-missing-1-required-keyword-only-argument-intents-or-tak)
