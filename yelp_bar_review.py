import sys
import re
import urllib2
import json
import HTMLParser
from BeautifulSoup import BeautifulSoup

# hReview URL 
# http://www.yelp.com/biz/tavern-on-brand-glendale-2

url = sys.argv[1]

# Parse Yelp review information
# See http://microformats.org/wiki/hreview

def parse_hreviews(url):
    try:
        page = urllib2.urlopen(url)
    except urllib2.URLError, e:
        print 'Failed to fetch ' + url
        raise e

    try:
        soup = BeautifulSoup(page)
    except HTMLParser.HTMLParseError, e:
        print 'Failed to parse ' + url
        raise e

    print soup

    # hreviews = soup.findAll(True, 'hReview')
    hreviews = soup.findAll('p', text=re.compile('review_comment'))
    print hreviews

    all_hreviews = []
    for hreview in hreviews:
        if hreview and len(hreview) > 1:

            reviewer = hreview.find(True, 'reviewer_info').text  

            dtreviewed = hreview.find(True, 'dtreviewed').text
            rating = hreview.find(True, 'rating').find(True, 'value-title')['title']
            description = hreview.find(True, 'description').text
            item = hreview.find(True, 'item').text

            all_hreviews.append({
                'reviewer': reviewer,
                'dtreviewed': dtreviewed,
                'rating': rating,
                'description': description,
                })
    return all_hreviews

reviews = parse_hreviews(url)

print json.dumps(reviews, indent=4)