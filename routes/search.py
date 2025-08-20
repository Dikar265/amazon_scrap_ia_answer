from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Products
from typing import List
from services.ask_ollama import get_embedding, analyze_with_ollama

router = APIRouter(
    prefix="/products",
    tags=["Search and Compare Products"]
)

@router.get("/search", response_model=List[dict])
def semantic_search(
    q: str = Query(..., description="Text for semantic search"),
    db: Session = Depends(get_db)
):
    query_embedding = get_embedding(q)

    results = (
        db.query(Products)
        .filter(Products.vector.cosine_distance(query_embedding) < 0.70)
        .order_by(Products.vector.cosine_distance(query_embedding))
        .all()
    )
    
    return [
        {
            "asin": r.asin,
            "name": r.name,
            "price": r.price,
            "url": r.url,
            "summary": r.summary
        }
        for r in results
    ]

@router.get("/compare_products")
def compare_products_ia(
    ids: List[int] = Query(..., description="Product IDs to compare"),
    db: Session = Depends(get_db)
):
    products = db.query(Products).filter(Products.id.in_(ids)).all()

    if not products or len(products) < 2:
        raise HTTPException(status_code=400, detail="At least 2 valid products are required to compare.")

    product_infos = []
    for p in products:
        info = p.json_scraped
        product_infos.append({
            "name": p.name,
            "price": p.price,
            "description": p.description,
            "colors": [c['display_name'] for c in info.get('colors', [])],
            "url": p.url
        })


    return analyze_with_ollama(product_infos, "compare_products")
