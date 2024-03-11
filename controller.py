from contextlib import asynccontextmanager
from fastapi import FastAPI
from context import ctx
import scraper

@asynccontextmanager
async def lifespan(app: FastAPI):
    ctx.make_directory()
    ctx.init_visited_pages()
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/imageCount")
async def scrapeImages(imageCount: int):
    await scraper.main(startUrl=ctx.startUrl, directory=ctx.directory, imageCount=imageCount, visitedUrls=ctx.visitedPages)
    return {"message": "images have been scrapped"}