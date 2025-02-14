from typing import Dict
import aiohttp
from fastapi import HTTPException
from .parsers.avito_parser import extract_description
from .services.openai_service import analyze_description


async def fetch_avito_listing(url: str) -> Dict:
    """
    Fetch and parse Avito listing data from provided URL
    """
    if not url.startswith("https://www.avito.ru/"):
        raise HTTPException(
            status_code=400,
            detail="Invalid URL. Only Avito URLs are supported"
        )

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    raise HTTPException(
                        status_code=response.status,
                        detail="Failed to fetch Avito listing"
                    )

                html_content = await response.text()
                description = await extract_description(html_content)

                # Analyze the description using OpenAI
                analysis_result = await analyze_description(description)

                return {
                    "url": url,
                    "status": "success",
                    "description": description or "Description not found",
                    "analysis": analysis_result,
                    "message": "Listing fetched successfully"
                }

    except aiohttp.ClientError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch Avito listing: {str(e)}"
        )
