# Job scraper

Looking for a job can be exhausting. Made this script for my personal use to make the process easier.
At the moment scrapes Profesia jobs. Analyzes job description for keywords (skills you specify) to find more suitable positions.

# Features
* search job based on your prefered position (default python)
* define skills to find more suitable positions
* send E-Mail notification with the jobs that matched your skills, sorted with score from most skill matches to least

# Usage
`python app.py -position`

# To do:

* [x] analyze job description for keywords to filter out more suitable positions
* [ ] improve this matching algorithm
* [x] send email with found jobs
* [x] add support for different pages
* [ ] make more dynamic - define skills dynamically etc.
* [ ] keep score of jobs already checked/applied to


