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
    url = "https://www.youtube.com/results?search_query=agriculture"
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

def get_youtube_video_ids(links_list):
    """
        Description: Get youtube video ids from links collected
    """
    video_ids = []
    for url in links_list:
        video_id = url.split("v=")[-1]
        ampersand_position = video_id.find("&")
        if ampersand_position != -1:
            video_id = video_id[:ampersand_position]
        video_ids.append(video_id)
        
    return video_ids

def get_data_from_youtube(video_ids):
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)
    dataset = pd.DataFrame()
    
    for id in video_ids:
        request = youtube.commentThreads().list(
            part="id, snippet",
            videoId= f"{id}"
        )
        response = request.execute()
        
        response = response['items']
        listing = []
        
        for item in response:
            is_public = item['snippet']['isPublic']
            if not is_public:
                print("This comment is restricted and not publicly visible.")
            else:
                data = flatten(item)
                listing.append(data)

        dataframe = pd.DataFrame(listing)
        dataset = dataset.append(dataframe)
    
    return dataset

def main():
    links_list = get_youtube_links(response)
    video_ids = get_youtube_video_ids(links_list)
    df = get_data_from_youtube(video_ids)
    
    return df    

if __name__ == "__main__":
    main()