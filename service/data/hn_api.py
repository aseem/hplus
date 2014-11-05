import pymongo
from firebase import firebase
import logging
import time
from datetime import datetime
import sys

# get top 100 stories on HN
def get_top_100(api, collection, logging):

    # clear out the collection
    collection.remove(None, safe=True)

    try:
        top_stories =api.get('topstories', None);
    except:
        logging.error('Encountered error get HN top 100')
        e = sys.exc_info()[0]
        logging.error("Exception: %s" % e)

    for index, story_id in enumerate(top_stories):
        try:
            story = api.get('item', story_id)
        except:
            logging.error('Encountered error, skipping story')
            e = sys.exc_info()[0]
            logging.error("Exception: %s" % e)
            continue

        if (not story):
            logging.error('Encountered error, skipping story')
            continue

        # add to Top 100 collection
        try:
            collection.update(
                {'url' : story['url']},
                {
                    'rank' : index + 1,
                    'title' : story['title'],
                    'url' : story['url'],
                    'id' : story['id'],
                    'score' : story['score'],
                    'time' : story['time'],
                    'by' : story['by'],
                    'type': story['type']
                },
                upsert=True,
                safe=True
            )
            #print index+1
        except:
            logging.error('Encountered error, skipping story')
            e = sys.exc_info()[0]
            logging.error("Exception: %s" % e)

def update_top_100(collection, collection_refresh, logging):
    #clear out current top 100
    collection.remove(None, safe=True)

    # copy over new to 100
    for story in collection_refresh.find():
        collection.insert(story, safe=True)



# Configure the logging system
logging.basicConfig(
    filename='hn_api.log',
    level=logging.DEBUG
)

logging.getLogger("requests").setLevel(logging.WARNING)

# settings
DATA_DELAY = 5 # minutes


# setup database
db_client = pymongo.MongoClient()
db = db_client['hacker_news_test']
db_top_100 = db['top_100']
db_top_100_refresh = db['top_100_refresh']
db_data = db['data']
db_data.ensure_index('url', unique=True)

# setup API access
hn = firebase.FirebaseApplication('https://hacker-news.firebaseio.com/v0/', None)

while True:
    logging.info('Starting top 100 download at %s' % datetime.now())
    get_top_100(hn, db_top_100_refresh, logging)
    logging.info('Starting database update at %s' % datetime.now())
    update_top_100(db_top_100, db_top_100_refresh, logging)
    logging.info('Completed top 100 update at %s' % datetime.now())
    time.sleep(25*60)
#print "Script completed!"



