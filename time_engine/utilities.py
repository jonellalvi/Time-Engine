__author__ = 'Jonell'

import hashlib

# function to grab gravitar
def getGravatarImage(emailAddress, imageSize=64):
    defimg = 'mm'
    return 'https://www.gravatar.com/avatar/%s?d=%s&s=%s' % (hashlib.md5(emailAddress).hexdigest(), defimg, imageSize)
