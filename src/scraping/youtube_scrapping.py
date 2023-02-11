from requests_html import HTMLSession
import os
import pandas as pd

import googleapiclient.discovery

# session = HTMLSession()
# url = "https://www.youtube.com/results?search_query=health&sp=CAISBAgBEAE%253D"
# response = session.get(url)
# response.html.render(sleep=5, timeout = 1000, keep_page = True, scrollwork = 10)

# # print(response.html.find('a#video-title'))

# for links in response.html.find('a#video-title'):
#     link = next(iter(links.absolute_links))
#     print(link)

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "AIzaSyB32r77YhdQiheZicUEJA-2sQZXT1tIAgI"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)

    request = youtube.commentThreads().list(
        part="id, snippet",
        videoId="XTjtPc0uiG8"
    )
    response = request.execute()

    dataframe = pd.DataFrame.from_dict(response)
    
    print(dataframe)

if __name__ == "__main__":
    main()