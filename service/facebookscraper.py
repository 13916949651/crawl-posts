import os
from random import random

import requests
from facebook_scraper import get_posts, get_profile, get_group_info

# https://github.com/kevinzg/facebook-scraper
# for post in get_posts('vapempireklangparade', pages=10, credentials={'luotaibin@gmail.com', 'ltb518818lfan'}):
#     print(post['post_url'][:50])
#     print(post['video'])
print('get_profile ---> ', get_profile("Obs.official", credentials={'luotaibin@gmail.com', 'ltb518818lfan'}))
# print('get_group_info ---> ', get_group_info("latesthairstyles", cookies="cookies.txt"))
