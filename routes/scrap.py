from fastapi import APIRouter, HTTPException
from services.scrap import url_list, url_single
import re

router = APIRouter(
    prefix="/scrap",
    tags=["Scrap Amazon Products"]
)

AMAZON_LIST_URL_REGEX = r"^https://www\.amazon\.com/s\?k=.+"
AMAZON_PRODUCT_URL_REGEX = r"^https://www\.amazon\.com/.+/dp/[A-Z0-9]+"

@router.post("/list_url", summary="link example: https://www.amazon.com/s?k=computer")
async def post_url(url: str, total_pages: int):
    if not re.match(AMAZON_LIST_URL_REGEX, url):
        raise HTTPException(status_code=400, detail="URL must be a valid Amazon search URL")
    return url_list(url, total_pages)

@router.post("/single_product", summary="link example: https://www.amazon.com/Dell-15-i7-1195G7-Bluetooth-Microsoft/dp/B0D4TZNPMX")
async def post_url_single(url: str):
    if not re.match(AMAZON_PRODUCT_URL_REGEX, url):
        raise HTTPException(status_code=400, detail="URL must be a valid Amazon product URL")
    return url_single(url)
