import pytumblr
import discord
import random
from login import TOKEN, TUMBLR

POST_LIMIT = 50

clientTumblr = TUMBLR # Sets tokens for Tumblr stored in login
clientDiscord = discord.Client()
# Look into default discord help command

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
                        sphealArray.append(sphealArray = sphealArray + x["photos"][0]["original_size"]["url"])

            # Adjust the counters
            postsLeft -= POST_LIMIT
            offset += POST_LIMIT
    return sphealArray

# When the client is set up and conneted it will print to the system running
#   the bot that it has connected
@clientDiscord.event
async def on_ready():
    print('Logged in as')
    print(clientDiscord.user.name)
    print(clientDiscord.user.id)
    print('------')

#This is where all the on message events happen
@clientDiscord.event
async def on_message(message):
    # Makes sure the bot can't respond to itself
    if clientDiscord.user.id != message.author.id:
        # If the bot is being issued a command checks to see if its in the correct channel
        #   This will hopefully avoid spam
        if message.content.upper().startswith('SPHEAL!RND') or message.content.upper().startswith('SPHEAL?RND'):
            tmp = await clientDiscord.send_message(message.channel, 'Finding you a random spheal (:3)\"')
            sphealURLArray = getAllSphealImagesURL()
            await clientDiscord.edit_message(tmp, "I found all my friends, picking the cutest one for you (:3)\"")
            rndURL = random.choice(sphealURLArray)
            await clientDiscord.edit_message(tmp, "%s (:3)\"" % rndURL)
        elif message.content.upper().startswith('SPHEAL!HELP') or message.content.upper().startswith('SPHEAL?HELP'):
            helpText = ('Hiya (:3)\"\n'
                        'Here are all the cool things I can do:\n\n'
                        '- spheal!rnd will get you a random picture of my friends\n')
            await clientDiscord.send_message(message.channel, '%s' % helpText)
        elif message.content.upper().startswith('SPHEAL!') or message.content.upper().startswith('SPHEAL?'):
            await clientDiscord.send_message(message.channel, 'I\'m sorry I don\'t understand (:3)\"\nYou can use spheal!help to see what I can do')

# Run the bot with the token provided
clientDiscord.run(TOKEN)

# # Print the entire array for testing
# sphealURLArray = getAllSphealImagesURL()
# print(sphealURLArray)
# print(random.choice(sphealURLArray))
