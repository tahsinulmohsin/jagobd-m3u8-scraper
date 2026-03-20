import requests
from bs4 import BeautifulSoup

url = "https://www.jagobd.com/category/bangla-channel"
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')

print("Finding all links that might be a channel...")
# E.g. find all links inside the main container
links = soup.find_all('a', href=True)
channels = []
for a in links:
    href = a['href']
    if 'jagobd.com/' in href and '/category/' not in href and 'http' in href:
        title = a.get('title') or a.text.strip()
        img = a.find('img')
        if img and not title:
            title = img.get('alt', '')
        if title:
            channels.append((title, href))

# Print first 5
for c in channels[:5]:
    print(c)
