from requests_html import HTMLSession
import os
import pandas as pd
from flatten_json import flatten

import googleapiclient.discovery

api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = "AIzaSyB32r77YhdQiheZicUEJA-2sQZXT1tIAgI"

def query_youtube_search():
    session = HTMLSession()
    topics = ['climate', 'agriculture', 'health', 'economics']
    url = "https://www.youtube.com/results?search_query=good+health"
    response = session.get(url)
    response.html.render(sleep=5, timeout = 1000, keep_page = True, scrolldown = 10)
    
    return response

response = query_youtube_search()

def get_youtube_links(response):
    link_list = []
    for links in response.html.find('a#video-title'):
        link = next(iter(links.absolute_links))
        
        if 'shorts' in link:
            pass
        else:
            link_list.append(link)
    
    return link_list

links_list = get_youtube_links(response)

def get_youtube_video_ids(links_list):
    """
        Description: Get youtube video ids from links collected
    """
    
        

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)

    request = youtube.commentThreads().list(
        part="id, snippet",
        videoId="P-dUmZOsdJ4"
    )
    response = request.execute()
    response = response['items']
    listing = []
    
    for item in response:
        data = flatten(item)
        listing.append(data)

    dataframe = pd.DataFrame(listing)
    dataframe.to_csv("data.csv")
    print("exported")

if __name__ == "__main__":
    main()