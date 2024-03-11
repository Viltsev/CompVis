import os
import asyncio
import uuid
from io import BytesIO
import httpx
from bs4 import BeautifulSoup
import requests
from PIL import Image
import logging
from context import ctx
import hashlib
import base64

async def fetch(url):
    headers = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
    }
    req = requests.get(url, headers, verify=False)
    src = req.text
    return src

# save image to a folder and database
async def saveImage(url, directory):
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get(url)

        if response.status_code == 200:
            imageName = str(uuid.uuid4()) + ".jpg"
            imagePath = os.path.join(directory, imageName)
            await compressImage(response.content, imagePath)


# load images from the page
async def loadPageImages(url, directory):
    html = await fetch(url)
    imageUrls = await scrapeImageURL(html)
    tasks = []
    for imgURL in imageUrls:
        newImage = "https:" + imgURL
        # check: can we scrape images
        tasks.append(saveImage(newImage, directory))
    await asyncio.gather(*tasks)


# image url scraper
async def scrapeImageURL(html):
    soup = BeautifulSoup(html, 'lxml')

    imagesBlock = soup.find(class_="main-content-wrapper")
    image_urls = [img['src'] for img in imagesBlock.find_all('img')]
    return image_urls

# image compressor
async def compressImage(imageContent, imagePath, quality=70, maxSize=1024 * 1024):
    if len(imageContent) > maxSize:
        with Image.open(BytesIO(imageContent)) as img:
            img.save(imagePath, optimize=True, quality=quality)
    else:
        with open(imagePath, 'wb') as f:
            f.write(imageContent)

async def crawler(startURL, directory, visitedUrls):
    # if we haven't visited the page
    if startURL not in visitedUrls:
        visitedUrls.add(startURL)

        # load images from the page
        await loadPageImages(startURL, directory)
    else:
        # else check the next pages
        logging.info(f"This page {startURL} has been visited! I'm going to the next page...")

    html = await fetch(startURL)
    soup = BeautifulSoup(html, 'lxml')
    pageUrl = soup.find("li", class_="pagination-next").find("a").get("href")
    nextPage = "https://www.saintalfred.com" + pageUrl
    # checking the case when all pages have been scraped
    try:
        task = crawler(nextPage, directory, visitedUrls)
        await asyncio.gather(task)
    except Exception:
        return
    else:
        # save visited urls into the file
        with open("visitedURL.txt", "w") as f:
            f.write("\n".join(visitedUrls))
        return


async def main(startUrl, directory, visitedUrls):
    visitedURL = visitedUrls

    if os.path.exists("visitedURL.txt"):
        with open("visitedURL.txt", "r") as f:
            visitedURL = set(f.read().splitlines())

    # start the crawler
    await crawler(startUrl, directory, visitedURL)

if __name__ == "__main__":
    ctx.make_directory()
    ctx.init_visited_pages()
    asyncio.run(main(ctx.startUrl, ctx.directory, visitedUrls=ctx.visitedPages))