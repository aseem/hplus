#imports
import requests
from pattern import web
from fnmatch import fnmatch
import HTMLParser
from datetime import datetime
import re

'''
data format:
url: URL for the link
title: title for the link
rank: current rank on the HN page
score: current points on the HN page
user: name of user who submitted the link
num_comments: current number of comments on the link
age: how long in minutes the link has been on HN
'''

def print_story(data):
    print str(data['rank']) + ". " + data['title']
    print data['url']
    print data['user']
    print str(data['score']) + " votes | " + str(data['age']) + " minutes old | " + str(data['num_comments']) + " comments"
    print


def get_story_age(subtext):

    # look for minutes
    pattern = '\d+ minute*'
    result = re.findall(pattern, subtext.content)
    if result:
        return int(re.findall('\d+', result[0])[0])

    # look for hours
    pattern = '\d+ hour*'
    result = re.findall(pattern, subtext.content)
    if result:
        return int(re.findall('\d+', result[0])[0]) * 60

    # look for days
    pattern = '\d+ day*'
    result = re.findall(pattern, subtext.content)
    if result:
        return int(re.findall('\d+', result[0])[0]) * 60 * 24
    else:
        return 0



def get_stories(url):
    html_parser = HTMLParser.HTMLParser()
    page = requests.get(url).text
    dom = web.Element(page)
    stories = [];

    # HN story is broken up into 3 parts:
    # - Rank
    # - Title
    # - Subtext
    subtext_tags = dom.by_class('subtext')
    title_holder_tags = dom.by_class('title')
    rank_tags = [];
    title_tags = [];
    for tag in title_holder_tags:
        anchor = tag.by_tag('a')
        if not anchor:
            rank_tags.append(tag)
        else:
            title_tags.append(tag)

    # Extract the information from the 3 parts
    for (rank, title, subtext) in zip(rank_tags, title_tags, subtext_tags):
        data = {}
        
        # parse the title tag to get title and url
        anchors = title.by_tag('a')
        data['url'] = anchors[0].attributes.get('href')
        data['title'] = anchors[0].content

        # get current rank
        data['rank'] = int(rank.content.strip('.'))

        # parse subtext to obtain the score, user, comments and age
        # (if available)
        spans = subtext.by_tag('span')
        if spans:
            data['score'] = int(re.findall('\d+', spans[0].content)[0])
        else:
            data['score'] = 0

        anchors = subtext.by_tag('a')
        if anchors:
            data['user'] = anchors[0].content
            comments = re.findall('\d+', anchors[1].content)
            if comments:
                data['num_comments'] = int(comments[0])
            else:
                data['num_comments'] = 0
        else:
            data['user'] = 'none'
            data['num_comments'] = 0

        # parse age
        data['age'] = get_story_age(subtext)

        stories.append(data)

    return stories


stories = get_stories('https://news.ycombinator.com')
for story in stories:
    print_story(story)

