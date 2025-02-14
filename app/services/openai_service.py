import json
import aiohttp
from typing import Dict
from fastapi import HTTPException

# Should be moved to environment variables
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"


async def analyze_description(description: str) -> Dict:
    """
    Analyze property description using OpenAI API to determine if males are allowed
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": [{
                    "text": "Analyze the rental property description to determine if male tenants are accepted. Respond only with a JSON object indicating whether males are allowed.\n\n# Steps\n\n1. **Translation** (optional): If the description is in a different language, translate it to English for better understanding.\n2. **Text Analysis**: Look for keywords or phrases in the description that specifically mention gender preferences or restrictions regarding tenants.\n3. **Determine Gender Preference**: Based on the analysis, conclude if male tenants are allowed, not allowed, or if it is unknown from the description provided.\n4. **Categorize Response**: Convert the conclusion into the JSON format as specified.",
                    "type": "text"
                }]
            },
            {
                "role": "user",
                "content": [{
                    "type": "text",
                    "text": description
                }]
            }
        ],
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "name": "gender_status",
                "schema": {
                    "type": "object",
                    "required": ["males"],
                    "properties": {
                        "males": {
                            "enum": ["true", "false", "unknown"],
                            "type": "string",
                            "description": "Indicates the male status with possible values: true, false, or 'unknown'."
                        }
                    },
                    "additionalProperties": False
                },
                "strict": True
            }
        },
        "temperature": 1,
        "max_tokens": 2048,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0,
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(OPENAI_API_URL, json=payload, headers=headers) as response:
                if response.status != 200:
                    raise HTTPException(
                        status_code=response.status,
                        detail="Failed to analyze description with OpenAI"
                    )

                data = await response.json()
                result = json.loads(data['choices'][0]['message']['content'])
                return result

    except aiohttp.ClientError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to analyze description: {str(e)}"
        )
