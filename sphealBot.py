import pytumblr
import discord
import random
import asyncio
from login import TOKEN, TUMBLR

#===============================================================================
# IDEAS
# GIVE TITLE FOR ANSWERS / PHOTOS
# CAN @SPHEAL_BOT AND IT WILL RESPOND
# Look into default discord help command
# Look into regex in python
# Refactor so that you don't have to add the beginning everytime
#===============================================================================

POST_LIMIT = 50

clientTumblr = TUMBLR # Sets tokens for Tumblr stored in login
clientDiscord = discord.Client()

clientTumblr.info() # Grabs the current user information

def getAllSphealImagesURL():
    offset = 0
    # Finds total number of posts on the blog
    postsLeft = clientTumblr.blog_info("spheal-a-day")["blog"]["posts"]
    # Sets an empty array for all the URLS
    sphealArray = []
    # API hard limits to 50 posts at a time :( So this gets all of them :)
    while postsLeft > 0:
            # If there are more posts left than the limit get the limit
            if postsLeft >= POST_LIMIT:
                print("Getting %d posts" % POST_LIMIT)
                tmpSphealDict = clientTumblr.posts("spheal-a-day", offset = offset, limit = POST_LIMIT)
            # Otherwise get the remaining posts
            else:
                print("Getting %d posts" % postsLeft)
                tmpSphealDict = clientTumblr.posts("spheal-a-day", offset = offset, limit = postsLeft)

            # Extract the URLs of the images from the posts
            #   NB: THIS IS HIGHLY CUSTOM TO THIS BLOG
            for x in tmpSphealDict["posts"]:
                if x["type"] == "answer":
                    splitAnswer = x["answer"].split("\"")
                    if len(splitAnswer) >= 8:
                        if not (splitAnswer[7] == "tumblr_blog"):
                            sphealArray.append(splitAnswer[7])
                    elif x["type"] == "photo":
                        sphealArray.append(x["photos"][0]["original_size"]["url"])

            # Adjust the counters
            postsLeft -= POST_LIMIT
            offset += POST_LIMIT
    return sphealArray

def getLatestSpheal():
    print("Finding the latest shpeal")
    tmpSphealDict = clientTumblr.posts("spheal-a-day", limit = POST_LIMIT)

    # Extract the URLs of the images from the posts
    #   NB: THIS IS HIGHLY CUSTOM TO THIS BLOG
    for x in tmpSphealDict["posts"]:
        if x["type"] == "answer":
            splitAnswer = x["answer"].split("\"")
            if len(splitAnswer) >= 8:
                if not (splitAnswer[7] == "tumblr_blog"):
                    return splitAnswer[7]
                elif x["type"] == "photo":
                    return x["photos"][0]["original_size"]["url"]
    # TODO: WHAT IF IT DOESN'T FIND A SPHEAL!!!

# Loads the last latest shpeal on start up
lastLatestURL = getLatestSpheal()

# Checks whether the latest spheal is different to what it last saw
def isLatestDifferent():
    latestURL = getLatestSpheal()
    if lastLatestURL == latestURL:
        return False
    else:
        return True

# Search for a new latest spheal and post if it is new
async def searchForNewSpheal():
    await clientDiscord.wait_until_ready()
    channel = clientDiscord.get_channel(423833486151909404)
    while not clientDiscord.is_closed():
        if isLatestDifferent():
            sphealLatest = getLatestSpheal()
            global lastLatestURL
            lastLatestURL = sphealLatest
            await channel.send("Here is my newest friend (:3)\"\n%s" % sphealLatest)
        else:
            print("No new spheal")
        await asyncio.sleep(1800) # task runs every 60*60/2 seconds (1/2 hour)

# When the client is set up and conneted it will print to the system running
#   the bot that it has connected
@clientDiscord.event
async def on_ready():
    print('Logged in as')
    print(clientDiscord.user.name)
    print(clientDiscord.user.id)
    print('------')
    await clientDiscord.change_presence(activity = discord.Game(name = "with my cute friends (:3)\""))
    print('Set playing status')

#This is where all the on message events happen
@clientDiscord.event
async def on_message(message):
    # Makes sure the bot can't respond to itself
    if clientDiscord.user.id != message.author.id:
        if message.content.upper().startswith('SPHEAL!HELP') or message.content.upper().startswith('SPHEAL?HELP'):
            helpText = ('Hiya (:3)\"\n'
                        'Here are all the cool things I can do:\n'
                        '```\n'
                        'My prefix is spheal? or spheal!'
                        '- \'blog\' will get you a link to find more of my friends\n'
                        '- \'random\' will get you a random picture of my friends (rnd can be used for short)\n'
                        '- \'latest\' will get you a picture of the latest spheal (daily will also work)\n'
                        '- \'metalGear\' will get you a picture of a metal gear spheal\n'
                        '- \'support\' will list the ways you can support the artist```'
                        'For example spheal!random will find a random spheal YAY! (:3)\"')
            await message.channel.send('%s' % helpText)
        elif message.content.upper().startswith('SPHEAL!BLOG') or message.content.upper().startswith('SPHEAL?BLOG'):
            blogText = "You can find more of my friends at https://spheal-a-day.tumblr.com (:3)\""
            await message.channel.send('%s' % blogText)
        elif message.content.upper().startswith('SPHEAL!RND') or message.content.upper().startswith('SPHEAL?RND') or message.content.upper().startswith('SPHEAL!RANDOM') or message.content.upper().startswith('SPHEAL?RANDOM'):
            tmp = await message.channel.send('Finding you a random spheal (:3)\"')
            sphealURLArray = getAllSphealImagesURL()
            await tmp.edit(content = "I found all my friends, picking the cutest one for you (:3)\"")
            rndURL = random.choice(sphealURLArray)
            print("Random Spheal choosen")
            await tmp.edit(content = "%s (:3)\"" % rndURL)
        elif message.content.upper().startswith('SPHEAL!LATEST') or message.content.upper().startswith('SPHEAL?LATEST') or message.content.upper().startswith('SPHEAL!DAILY') or message.content.upper().startswith('SPHEAL?DAILY'):
            tmp = await message.channel.send('Finding you the latest spheal (:3)\"')
            sphealLatest = getLatestSpheal()
            await tmp.edit(content = "Here is my newest friend (:3)\"\n%s" % sphealLatest)
        elif message.content.upper().startswith('SPHEAL!METALGEAR') or message.content.upper().startswith('SPHEAL?METALGEAR'):
            snakeText = "Spheal? Spheal!? SPHEAAAAAAAAAAAL!\n"
            if random.randint(0, 1) == 1:
                snakeText += "https://78.media.tumblr.com/452988b3dbc9bac19b450d7eedeb119a/tumblr_inline_p8qkuyrRYX1sarpkj_1280.jpg"
            else:
                snakeText += "https://78.media.tumblr.com/525bc24ca1f1c21f0684340988c55b2d/tumblr_inline_oup0067dFI1sarpkj_1280.jpg"
            await message.channel.send('%s' % snakeText)
        elif message.content.upper().startswith('SPHEAL!SUPPORT') or message.content.upper().startswith('SPHEAL?SUPPORT'):
            helpText = ('Thanks for offering support (:3)\"\n'
                        'You can support the artist on\n\n'
                        'Ko-fi: https://ko-fi.com/spheal\n'
                        'Patreon: https://www.patreon.com/dailyspheal')
            await message.channel.send('%s' % helpText)
        elif message.content.upper().startswith('SPHEAL!') or message.content.upper().startswith('SPHEAL?'):
            await message.channel.send('I\'m sorry I don\'t understand (:3)\"\nYou can use spheal!help to see what I can do')

#Start the background task looking for a new spheal
clientDiscord.loop.create_task(searchForNewSpheal())

# Run the bot with the token provided
clientDiscord.run(TOKEN)

# # Print the entire array for testing
# sphealURLArray = getAllSphealImagesURL()
# print(sphealURLArray)
# print(random.choice(sphealURLArray))
