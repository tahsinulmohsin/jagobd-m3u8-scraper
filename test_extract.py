import re
import ast
import requests

def extract_m3u8(channel_name):
    # e.g., btvnationalbd
    url = f"https://tvz.jagobd.com/embed.php?u={channel_name}&vw=700&vh=480&autoplay=true"
    headers = {'Referer': 'https://www.jagobd.com/'}
    r = requests.get(url, headers=headers)
    html = r.text
    
    # 1. Find the src function name
    src_match = re.search(r'src:\s*([a-zA-Z0-9_]+)\(\),', html)
    if not src_match:
        print("Could not find src function name")
        return None
        
    func_name = src_match.group(1)
    
    # 2. Find the function body
    match = re.search(rf'function {func_name}\(\)\s*\{{\s*return\((.*?)\);', html)
    if not match:
        print(f"Could not find {func_name} function")
        return None
        
    expression = match.group(1)
    base_url = ""
    
    # 3. literal arrays: ["h","t"...].join("")
    arrays = re.findall(r'(\[.*?\])\.join\([\'"][\'"]\)', expression)
    for arr in arrays:
        base_url += "".join(ast.literal_eval(arr))
        
    # 4. Variable joins: varName.join("")
    var_joins = re.findall(r'([a-zA-Z0-9_]+)\.join\([\'"][\'"]\)', expression)
    for var in var_joins:
        var_match = re.search(rf'var\s+{var}\s*=\s*(\[.*?\]);', html)
        if var_match:
            base_url += "".join(ast.literal_eval(var_match.group(1)))
            
    # 5. Span innerHTML: document.getElementById("...").innerHTML
    doc_joins = re.findall(r'document\.getElementById\([\'"]([a-zA-Z0-9_]+)[\'"]\)\.innerHTML', expression)
    if not doc_joins:
        doc_joins = re.findall(r'document\.getElementById\(([a-zA-Z0-9_]+)\)\.innerHTML', expression)
        
    for span_id in doc_joins:
        span_match = re.search(rf'<span[^>]*id=[\'\"]?{span_id}[\'\"]?[^>]*>(.*?)</span>', html)
        if span_match:
            base_url += span_match.group(1)
            
    return base_url.replace('\\/', '/')

print("BTV National:", extract_m3u8('btvnationalbd'))
print("Somoy News:", extract_m3u8('somoynewsbd'))
print("ATN Bangla:", extract_m3u8('atn-bangla'))
print("Channel 24:", extract_m3u8('channel24'))
