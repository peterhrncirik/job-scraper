import requests
from bs4 import BeautifulSoup
import pandas as pd

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
    summary_div = bool(soup.find('div', attrs={'class': 'job-info'}))
    
    if summary_div:
        return soup.find('div', attrs={'class': 'job-info'}).text.strip().replace('\n', '')
    else:
        return ''

# Initiate list to append each job into    
jobs = []

# Get jobs from more pages
for _ in range(1, 3):
    p = extract(_)
    transform(p)

# Transform to DataFrame
df = pd.DataFrame(jobs)
df.to_csv('jobs.csv')


    
