from bs4 import BeautifulSoup
import requests
import os

def getImageIds(UID : int):
    baseurl = f"https://www.pixiv.net/ajax/user/{UID}/profile/all?lang=en"
    response = requests.get(baseurl)
    illusts = list(response.json()['body']['illusts'])
    return illusts

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

def download(url : str, ArtistID, ImgName):
    headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)',
        'Accept-Encoding': None,
        'Referer' : 'https://www.pixiv.net/member_illust.php?mode=medium&illust_id=' + str(ArtistID)
    }
    response = requests.get(url, stream=True, headers = headers)

    if not os.path.exists('images'):
        os.mkdir('images')
    if not os.path.exists(f'images/{ArtistID}'):
        os.mkdir(f'images/{ArtistID}')

    with open(f"images/{ArtistID}/{ImgName}","wb") as w:
        w.write(response.content)
