# Job scraper

Analyzes job description for keywords (skills you specify) to find more suitable positions & sends e-mail with found matches.

# Features
* search job based on your prefered position (default python)
* define skills to find more suitable positions
* send E-Mail notification with the jobs that matched your skills, sorted with score from most skill matches to least
* sends only jobs that haven't been already seen 

# Usage
`python app.py -position`

at the moment skills are not dynamic, they are defind in the constant:

```python
SKILLS = ('django', 'django developer', 'django junior developer', 'python developer', 'python junior developer', 'python junior', 'python', 'sql', 'flask', 'javascript', 'junior', 'css', 'html', 'html/css')
```

# To do:

* [x] analyze job description for keywords to filter out more suitable positions
* [ ] improve this matching algorithm
* [x] send email with found jobs
* [ ] add support for different pages
* [ ] make more dynamic - define skills dynamically etc.
* [x] keep score of jobs already checked/applied to


