import requests
from bs4 import BeautifulSoup
import re
import ast
from concurrent.futures import ThreadPoolExecutor

def generate_playlist():
    categories = [
        "https://www.jagobd.com/category/bangla-channel",
        "https://www.jagobd.com/category/sports",
        "https://www.jagobd.com/category/news-paper",
        "https://www.jagobd.com/category/islamic",
        "https://www.jagobd.com/category/bangla-radio",
        "https://www.jagobd.com/category/kids",
        "https://www.jagobd.com/category/music"
    ]
    
    channel_links = {}
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1'
    })
    
    # Extract channel URLs
    for cat in categories:
        try:
            r = session.get(cat, timeout=10)
            soup = BeautifulSoup(r.text, 'html.parser')
            links = soup.find_all('a', href=True)
            for a in links:
                href = a['href']
                if 'jagobd.com/' in href and '/category/' not in href and 'http' in href:
                    excluded = ['contact-us', 'faq', 'privacy-policy.html', 'terms.html', 'technical-help', 'facebook.com', 'twitter.com']
                    if any(ex in href for ex in excluded):
                        continue
                    
                    title = a.get('title') or a.text.strip()
                    img = a.find('img')
                    if img and not title:
                        title = img.get('alt', '')
                        
                    if not title:
                        continue
                        
                    if href not in channel_links:
                        channel_links[href] = title.strip()
        except:
            pass
            
    results = []
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(extract_m3u8_from_page, session, href, title) for href, title in channel_links.items()]
        for future in futures:
            res = future.result()
            if res and res[1]:
                results.append(res)
                
    playlist = "#EXTM3U\n"
    for title, url in results:
        playlist += f'#EXTINF:-1 tvg-id="" tvg-name="{title}" tvg-logo="" group-title="JagoBD",{title}\n'
        playlist += f'#EXTVLCOPT:http-referrer=https://www.jagobd.com/\n'
        playlist += f'#EXTVLCOPT:http-user-agent=Mozilla/5.0\n'
        playlist += f'{url}|Referer=https://www.jagobd.com/\n'
        
    return playlist

def extract_m3u8_from_page(session, url, title):
    try:
        r = session.get(url, timeout=10)
        html = r.text
        
        iframe_match = re.search(r'<iframe[^>]*src=[\"\']?([^\"\'>]+embed\.php[^\"\'>]+)[\"\']?[^>]*>', html, re.IGNORECASE)
        if not iframe_match:
            m = re.search(r'(https?://[^\s\"\'<>]*\.m3u8[^\s\"\'<>]*)', html)
            if m:
                return (title, m.group(1).replace('\\/', '/'))
            return None
            
        embed_url = iframe_match.group(1)
        headers = {'Referer': url}
        
        embed_r = session.get(embed_url, headers=headers, timeout=10)
        embed_html = embed_r.text
        
        src_match = re.search(r'src:\s*([a-zA-Z0-9_]+)\(\),', embed_html)
        if not src_match:
            m = re.search(r'(https?://[^\s\"\'<>]*\.m3u8[^\s\"\'<>]*)', embed_html)
            if m:
                return (title, m.group(1).replace('\\/', '/'))
            return None
            
        func_name = src_match.group(1)
        func_match = re.search(rf'function {func_name}\(\)\s*\{{\s*return\((.*?)\);', embed_html)
        if not func_match:
            return None
            
        expression = func_match.group(1)
        base_url = ""
        
        arrays = re.findall(r'(\[.*?\])\.join\([\'"][\'"]\)', expression)
        for arr in arrays:
            base_url += "".join(ast.literal_eval(arr))
            
        var_joins = re.findall(r'([a-zA-Z0-9_]+)\.join\([\'"][\'"]\)', expression)
        for var in var_joins:
            var_match = re.search(rf'var\s+{var}\s*=\s*(\[.*?\]);', embed_html)
            if var_match:
                base_url += "".join(ast.literal_eval(var_match.group(1)))
                
        doc_joins = re.findall(r'document\.getElementById\([\'"]([a-zA-Z0-9_]+)[\'"]\)\.innerHTML', expression)
        if not doc_joins:
            doc_joins = re.findall(r'document\.getElementById\(([a-zA-Z0-9_]+)\)\.innerHTML', expression)
            
        for span_id in doc_joins:
            span_match = re.search(rf'<span[^>]*id=[\'\"]?{span_id}[\'\"]?[^>]*>(.*?)</span>', embed_html)
            if span_match:
                base_url += span_match.group(1)
                
        return (title, base_url.replace('\\/', '/'))
    except Exception:
        return None

if __name__ == '__main__':
    print("Generating M3U8 Playlist...")
    m3u8_content = generate_playlist()
    with open('playlist.m3u8', 'w', encoding='utf-8') as f:
        f.write(m3u8_content)
    print("Playlist saved to playlist.m3u8 successfully.")
