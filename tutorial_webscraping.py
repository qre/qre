import requests
topics_url = 'https://github.com/topics'
response = requests.get(topics_url)
response.status_code
page_contents = response.text
from bs4 import BeautifulSoup
doc = BeautifulSoup(page_contents, 'html.parser')
selection_class = 'f3 lh-condensed mb-0 mt-1 Link--primary'
topic_title_tags = doc.find_all('p', {'class': selection_class})
desc_selector = 'f5 color-fg-muted mb-0 mt-1'
topic_desc_tags = doc.find_all('p', {'class': desc_selector})
topic_title_tags0 = topic_title_tags[0]
topic_title_tags0.parent
topic_link_tags = doc.find_all('a', {'class': 'd-flex no-underline'})
topic0_url = "https://github.com" + topic_link_tags[0]['href']
topic_titles = []
for tag in topic_title_tags:
    topic_titles.append(tag.text)
topic_descs = []
for tag in topic_desc_tags:
    topic_descs.append(tag.text.strip())
topic_urls = []
base_url = "https://github.com"
for tag in topic_link_tags:
    topic_urls.append(base_url + tag['href'])
topic_urls
import pandas as pd
topics_dict = {
    'title': topic_titles,
    'description': topic_descs,
    'url': topic_urls
}
topics_df = pd.DataFrame(topics_dict)
topics_df.to_csv('topics.csv', index=None)
print(topics_df)

## Getting info out of a topic page

topic_page_url = topic_urls[0]
response = requests.get(topic_page_url)
topic_doc = BeautifulSoup(response.text, 'html.parser')
h3_selection_class = 'f3 color-fg-muted text-normal lh-condensed'
repo_tags = topic_doc.find_all('h3', {'class': h3_selection_class})
star_tags = topic_doc.find_all('a', {'class': 'social-count js-social-count'})
def parse_star_count(stars_str):
    stars_str = stars_str.strip()
    if stars_str[-1] == 'k':
        return int(float(stars_str[:-1]) * 1000)
    return int(stars_str)
def get_repo_info(h3_tag, star_tag):
    # returns all required info about the repository
    a_tags = h3_tag.find_all('a')
    username = a_tags[0].text.strip()
    repo_name = a_tags[1].text.strip()
    repo_url = base_url + a_tags[1]['href']
    stars = parse_star_count(star_tag.text.strip())
    return username, repo_name, repo_url, stars
topic_repos_dict = {
    'username': [],
    'repo_name': [],
    'stars': [],
    'repo_url': []
}
for i in range(len(repo_tags)):
        repo_info = get_repo_info(repo_tags[i],star_tags[i])
        topic_repos_dict['username'].append(repo_info[0])
        topic_repos_dict['repo_name'].append(repo_info[1])
        topic_repos_dict['repo_url'].append(repo_info[2])
        topic_repos_dict['stars'].append(repo_info[3])
def get_topic_page(topic_url):
    #Download the page
    response = requests.get(topic_page_url)
    #Check response
    if response.status_code !=200:
        raise Exception('Failed to load page {}'.format(topic_url))
    #Parse using BS
    topic_doc = BeautifulSoup(response.text, 'html.parser')
    return topic_doc

def get_repo_info(h3_tag, star_tag):
    # returns all required info about the repository
    a_tags = h3_tag.find_all('a')
    username = a_tags[0].text.strip()
    repo_name = a_tags[1].text.strip()
    repo_url = base_url + a_tags[1]['href']
    stars = parse_star_count(star_tag.text.strip())
    return username, repo_name, repo_url, stars

def get_topic_repos(topic_doc):
    #Get h3 tags containing repo title, repo URL and username
    h3_selection_class = 'f3 color-fg-muted text-normal lh-condensed'
    repo_tags = topic_doc.find_all('h3', {'class': h3_selection_class})
    #Get star tags
    star_tags = topic_doc.find_all('a', {'class': 'social-count js-social-count'})
    topic_repos_dict = {
    'username': [],
    'repo_name': [],
    'stars': [],
    'repo_url': []
}
    #Get repo info
    for i in range(len(repo_tags)):
        repo_info = get_repo_info(repo_tags[i],star_tags[i])
        topic_repos_dict['username'].append(repo_info[0])
        topic_repos_dict['repo_name'].append(repo_info[1])
        topic_repos_dict['repo_url'].append(repo_info[2])
        topic_repos_dict['stars'].append(repo_info[3])
    return pd.DataFrame(topic_repos_dict)

topic_repos_df = pd.DataFrame(topic_repos_dict)
topic_repos_df.to_csv('topic_repos.csv', index=None)
print(topic_repos_df)
