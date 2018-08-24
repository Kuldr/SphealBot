import pytumblr
import random
from login import TOKEN, TUMBLR

POST_LIMIT = 50

client = TUMBLR # Sets tokens for Tumblr stored in login

client.info() # Grabs the current user information

def getAllSphealImagesURL():
    offset = 0
    # Finds total number of posts on the blog
    postsLeft = client.blog_info("spheal-a-day")["blog"]["posts"]
    # Sets an empty array for all the URLS
    sphealArray = []
    # API hard limits to 50 posts at a time :( So this gets all of them :)
    while postsLeft > 0:
            # If there are more posts left than the limit get the limit
            if postsLeft >= POST_LIMIT:
                print("Getting %d posts" % POST_LIMIT)
                tmpSphealDict = client.posts("spheal-a-day", offset = offset, limit = POST_LIMIT)
            # Otherwise get the remaining posts
            else:
                print("Getting %d posts" % postsLeft)
                tmpSphealDict = client.posts("spheal-a-day", offset = offset, limit = postsLeft)

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

# Print the entire array for testing
sphealURLArray = getAllSphealImagesURL()
print(sphealURLArray)
print(random.choice(sphealURLArray))
