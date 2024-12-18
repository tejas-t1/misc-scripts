from pydantic import BaseModel
from typing import List, Dict
import feedparser
import requests
from bs4 import BeautifulSoup
from collections import OrderedDict
import csv
from datetime import datetime

class Summary(BaseModel):
    title: str
    published: str
    summary: str
    link: str

# Function to parse the Atom feed and summarize contributions
def summarize_contributions(feed_url: str, access_token) -> Dict[str, List[Summary]]:
    # Parse the Atom feed

    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(feed_url, headers=headers)
    response.raise_for_status()
    feed = feedparser.parse(response.content)

    # Initialize an OrderedDict to store summaries grouped by link
    summaries_by_link = OrderedDict()

    # Iterate through the feed entries
    for entry in feed.entries:
        # Extract relevant information
        title = BeautifulSoup(entry.title, 'html.parser').get_text()
        published = entry.published
        summary_text = getattr(entry, 'summary', 'N/A')
        summary_text = BeautifulSoup(summary_text, 'html.parser').get_text()
        link = entry.link

        # Create a Summary object
        summary = Summary(
            title=title,
            published=published,
            summary=summary_text,
            link=link
        )

        # Add the summary to the OrderedDict
        if link not in summaries_by_link:
            summaries_by_link[link] = []
        summaries_by_link[link].append(summary)

    return summaries_by_link

def getUrl(user, from_date) -> str:
    # Define the date range
    to_date = int(datetime.now().timestamp() * 1000)
    feed_url = f'https://jira.devtools.intel.com/activity?maxResults=1000&streams=user+IS+{user}&streams=update-date+BETWEEN+{from_date}+{to_date}&os_authType=basic&title=undefined'
    return feed_url

# URL of the Jira Atom feed (replace with your actual Jira Atom feed URL)
feed_url = getUrl(user="tejast", from_date=int(datetime(2024, 9, 15).timestamp() * 1000))
jira_token = access_token = "<>"
# Get the summaries of contributions
contributions_summaries = summarize_contributions(feed_url, jira_token)

# Print the summaries grouped by link
for index, (link, summaries) in enumerate(contributions_summaries.items()):
    print(f"{index})##### Link: {link}")
    for index, summary in enumerate(summaries):
        print(f"\t{index + 1}) Title: {summary.title}\n\tPublished: {summary.published}\n\tSummary: {summary.summary}\n\tLink: {summary.link}")
    print("\n" + "=" * 40 + "\n")

def writeCsv(path: str, contributions_summaries: Dict[str, List[Summary]]):
    with open(path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Jira Index','Link', 'Index', 'Title', 'Published', 'Summary'])

        for indexj,(link, summaries) in enumerate(contributions_summaries.items()):
            for index, summary in enumerate(summaries):
                writer.writerow([indexj+1,link, index + 1, summary.title, summary.published, summary.summary])
            writer.writerow([""]*6)

writeCsv(r"C:\Users\tejast\Downloads\Q4JiraTejas.csv", contributions_summaries)