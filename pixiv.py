from bs4 import BeautifulSoup
import requests
import os
from tqdm import tqdm

def getImageIds(UID : int):
    baseurl = f"https://www.pixiv.net/ajax/user/{UID}/profile/all?lang=en"
    response = requests.get(baseurl)
    illusts = list(response.json()['body']['illusts'])
    return illusts

def isDuplicate(file, folder):
    if os.path.exists(f'images/{folder}/{file}'):
        return True
    return False

def getImageLink(ImgID : int, ArtistID : int):
    baseurl = f"https://www.pixiv.net/en/artworks/{ImgID}"
    response = requests.get(baseurl).text
    soup = str(BeautifulSoup(response, "lxml"))
    links = []

    start = soup.find("original")
    end = soup.find("tags")
    
    links.append(soup[start + 11:end - 4])
    
    start = links[0].split('_')[0]

    end = links[0].split('_')[-1]
    end_start = end.split('.')[0]
    end_img_format = end.split('.')[-1]
    img_num = int(end_start[1:])+1
    
    while True:
        next_img = start+"_p"+str(img_num)+"."+end_img_format
        hdr = {
            'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)',
            'Referer' : 'https://www.pixiv.net/member_illust.php?mode=medium&illust_id=' + str(ArtistID)
        }
        req = requests.get(next_img, headers = hdr)
        if req.status_code == 404:
            break
        links.append(next_img)
        img_num += 1

    return links

def download(url : str, ArtistID, ImgName, title):
    try:
        headers = {
            'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)',
            'Accept-Encoding': None,
            'Referer' : 'https://www.pixiv.net/member_illust.php?mode=medium&illust_id=' + str(ArtistID)
        }
        response = requests.get(url, stream=True, headers = headers)
        content_length = int(response.headers.get("Content-Length")) #Bytes

        if not os.path.exists('images'):
            os.mkdir('images')
        if not os.path.exists(f'images/{ArtistID}'):
            os.mkdir(f'images/{ArtistID}')

        with open(f"images/{ArtistID}/{ImgName}","wb") as w:
            with tqdm(total=content_length, unit="B", unit_scale=True, desc=title, initial=0, ascii=True) as pbar:
                for chunk in response.iter_content(chunk_size=1024):         
                    if chunk:
                        w.write(chunk) 
                        pbar.update(len(chunk))
    
    except Exception as e:
        print("[Err] An Error Occured...")
        print("[INFO] ",e)
        if os.path.exists(f'images/{ArtistID}/{ImgName}'):
            os.remove(f'images/{ArtistID}/{ImgName}')
        exit()
