import requests
import argparse
from bs4 import BeautifulSoup
import pandas as pd

import time
import random

# For readability and progress bar
from rich import print
from rich.progress import track

# Text analysis
from rake_nltk import Rake

# Email
from notify import notify

# Usage
parser = argparse.ArgumentParser(description='Job position')
parser.add_argument('-p', default='python', help='what position are you looking for?', type=str)
args = parser.parse_args()

# Initiate list to append each job into    
jobs = []
jobs_skills_matched = []
jobs_already_seen = []
SKILLS = ('django', 'django developer', 'django junior developer', 'python developer', 'python junior developer', 'python junior', 'python', 'sql', 'flask', 'javascript', 'junior', 'css', 'html', 'html/css')

# load IDs of already seen jobs
with open('ids.txt') as file:
    
    for id in file:
        jobs_already_seen.append(id.strip())


def extract(page):
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0'}
    url = f'https://www.profesia.sk/praca/bratislavsky-kraj/?remote_work=2&search_anywhere={args.p}&page_num={page}'
    r = requests.get(url, headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup

def transform(soup):
    
    # Initialize Rake object
    rake = Rake()

    # Get the whole jobs column
    divs = soup.find_all('li', class_ = 'list-row')

    # Iterate over each job div
    for item in track(divs, description='Extracting job infos...'):
        
        # Print progress bar
        time.sleep(2)


        # Skip the newsletter div
        if bool(item.find('form', class_=['form-horizontal'])):
            continue
        
        # Get parts of the job
        title = item.find('span', class_ = 'title').text.strip()
        company = item.find('span', attrs={'class': 'employer'}).text.strip()
        salary = item.find('span', class_=['label-bordered', 'green']).text.strip()
        link = item.find('span', attrs={'class': 'title'}).parent.get('href')

        # Split URL for ID and save it to avoid sending same job postings
        id = link.split('/')[-1]
        
        if id not in jobs_already_seen:
            with open('ids.txt', 'a+') as file:

                file.write(id + '\n')
        
        # Open each job and return job summary
        summary = get_job_summary(link)
        
        # Analyze summary for keywords
        rake.extract_keywords_from_text(summary)

        job = {
            'id': id,
            'title': title,
            'company': company,
            'salary': salary,
            # Append summary keywords as a set to remove duplicates
            'summary': set(rake.get_ranked_phrases()),
            'link': f'https://www.profesia.sk{link}'
        }
        
        jobs.append(job)
    
    return

def get_job_summary(link):
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0'}
    url = f'https://www.profesia.sk{link}'
    r = requests.get(url, headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup.find('main', attrs={'id': 'detail'}).text
    

# Get jobs from more pages
for i in range(1, 3):
    print(f'Reading page #{i}...')
    p = extract(i)
    transform(p)

# Transform to DataFrame and export to csv
# df = pd.DataFrame(jobs)
# df.to_csv('jobs.csv')

def analyze_job(jobs):

    for job in track(jobs, description="Analyzing jobs..."):

        # Print progress bar
        time.sleep(2)

        # check for keywords in summary as well in title
        match = [skill for skill in SKILLS if skill in job['summary'] or skill in job['title'].lower()]
                
        # if match and not already seen, append job link to jobs_skills_matched
        if match and job['id'] not in jobs_already_seen:
            jobs_skills_matched.append(f'Score: {len(match)} | Skills: {match} | {job["link"]}')
            
    return

    
analyze_job(jobs)

# send email  
notify(jobs=sorted(jobs_skills_matched, reverse=True))

