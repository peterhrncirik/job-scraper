import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def extract(page):
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0'}
    url = f'https://www.profesia.sk/praca/bratislavsky-kraj/?remote_work=2&search_anywhere=python&page_num={page}'
    r = requests.get(url, headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup

def transform(soup):
    
    # Get the whole jobs column
    divs = soup.find_all('li', class_ = 'list-row')

    # Iterate over each job div
    for i, item in enumerate(divs):
        
        # Skip the newsletter div
        if bool(item.find('form', class_=['form-horizontal'])):
            continue
        
        # Get parts of the job
        title = item.find('span', class_ = 'title').text.strip()
        company = item.find('span', attrs={'class': 'employer'}).text.strip()
        salary = item.find('span', class_=['label-bordered', 'green']).text.strip()
        link = item.find('span', attrs={'class': 'title'}).parent.get('href')
        # Open each job and return job summary
        summary = get_job_summary(link)
            
        job = {
            'title': title,
            'company': company,
            'salary': salary,
            'summary': summary,
            'link': f'https://www.profesia.sk{link}'
        }
        
        jobs.append(job)
    
    return

def get_job_summary(link):
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0'}
    url = f'https://www.profesia.sk{link}'
    r = requests.get(url, headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    summary_div = bool(soup.find('div', attrs={'class': 'details'}))
    
    if summary_div:
        
        # Get the whole page
        page_details = soup.find('div', attrs={'class': 'details'})

        # Remove h4 titles from the page, join text together and return it
        return ' '.join(text for text in page_details.find_all(text=True) if text.parent.name != "h4")

    else:
        return ''

# Initiate list to append each job into    
jobs = []
jobs_skills_matched = []
SKILLS = ('django', 'python', 'sql', 'flask', 'javascript', 'junior')

# Get jobs from more pages
for i in range(1, 2):
    print(f'Reading page #{i}...')
    p = extract(i)
    transform(p)

# Transform to DataFrame
df = pd.DataFrame(jobs)
df.to_csv('jobs.csv')

def analyze_job(jobs):
    
    for job in jobs:
        
        # clear job description for analysis
        summary = job['summary'].strip().replace('\n', '').replace('-', ' ').replace('?', ' ').replace('!', ' ').replace('/', ' ').replace(',', ' ').replace('.', ' ').replace('(',' ').replace(')',' ').lower()

        # create new list of all words from description
        words = summary.split()

        # check keywords in job description
        match = [i for i in SKILLS if i in words]
        
        # if match, append job link to jobs_skills_matched
        if match:
            jobs_skills_matched.append(job['link'])


def sent_email(jobs):
    pass
    
analyze_job(jobs)
