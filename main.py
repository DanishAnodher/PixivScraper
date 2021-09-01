from pixiv import *

def main():
    ArtistID = input("Artist's iD : ")
    illustrations = getImageIds(ArtistID)
    total_illusts = len(illustrations)
    print(f"[INFO] Illustrations Found = {total_illusts}")
    for index, illusts in enumerate(illustrations):
        images = getImageLink(illusts, ArtistID)
        for img in images:
            img_name = img.split('/')[-1]
            download(img, ArtistID, img_name)
            print(f"[INFO] Downloaded Image {img_name} ({index+1}/{total_illusts})")

if __name__ == "__main__":
    main()