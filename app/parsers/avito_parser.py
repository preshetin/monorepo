from bs4 import BeautifulSoup
from typing import Optional

description_div_selector = '#app > div > div.index-module-root-_787g.index-module-responsive-edGMF.index-module-page_default-eRWW_.index-module-page_default_wide-JFTMn > div:nth-child(1) > div > div.style-item-view-PCYlM > div:nth-child(3) > div > div.style-item-view-content-left-bb5Ih > div.style-item-view-main-tKI1S.js-item-view-main.style-item-min-height-TJwyJ > div.style-item-view-block-SEFaY.style-item-view-description-k9US4.style-new-style-iX7zV > div > div'


async def extract_description(html_content: str) -> Optional[str]:
    """
    Extract description text from Avito listing HTML content

    Args:
        html_content (str): Raw HTML content from Avito page

    Returns:
        Optional[str]: Cleaned description text or None if not found
    """
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        description_div = soup.select_one(description_div_selector)

        if not description_div:
            return None

        # Get text content and remove extra whitespace
        description_text = description_div.get_text(separator=' ', strip=True)
        return description_text

    except Exception as e:
        print(f"Error parsing description: {str(e)}")
        return None
