import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_ai_horoscope(name, sun, moon, asc):
    prompt = f"""
    You are an expert astrologer writing a personalized horoscope.

        User:
        - Name: {name}
        - Sun Sign: {sun}
        - Moon Sign: {moon}
        - Ascendant: {asc}

        Write these sections:
        1. Personality
        2. Career
        3. Finance
        4. Health
        5. Relationships
        6. 3 practical tips

        Keep it warm, specific, realistic, and not extreme.
        Avoid guaranteed predictions and avoid medical or financial certainty.
        """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500
    )

    return response.choices[0].message.content