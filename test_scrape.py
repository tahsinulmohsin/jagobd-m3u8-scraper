import requests
import re

url = "https://tvz.jagobd.com/embed.php?u=btvnationalbd&vw=700&vh=480&autoplay=true"
headers = {'Referer': 'https://www.jagobd.com/'}
r = requests.get(url, headers=headers)

m3u8s = re.findall(r'(https?://[^\s\"\'<>]*\.m3u8[^\s\"\'<>]*)', r.text)
if m3u8s:
    print("M3U8 Links found:")
    for m in m3u8s:
        print(m)
else:
    print("No direct m3u8. Looking for JS strings that look like base64 or tokens...")
    with open('test_embed.html', 'w', encoding='utf-8') as f:
        f.write(r.text)
    print("Saved to test_embed.html")
