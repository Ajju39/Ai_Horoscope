import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_ai_horoscope(name, sun, moon, asc):
    prompt = f"""
You are a thoughtful horoscope guide speaking to a real person.

Write a personalized horoscope for {name} using:
- Sun Sign: {sun}
- Moon Sign: {moon}
- Ascendant: {asc}

Style rules:
- Sound warm, natural, and human.
- Do not sound robotic, generic, or overly mystical.
- Avoid phrases like "based on the provided information", "it is important to note", or "as an AI".
- Use simple, conversational language.
- Keep it personal and easy to read.
- Use short paragraphs, not stiff bullet points.
- Avoid extreme claims or guaranteed outcomes.
- Avoid medical, legal, or financial certainty.

Cover these areas naturally:
- Personality
- Career
- Finance
- Health
- Relationships

End with 3 short practical tips.

Keep the response around 250 to 400 words.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=700
    )

    return response.choices[0].message.content


def generate_ai_chat_reply(name, sun, moon, asc, question, history):
    if history:
        history_text = "\n".join([
            (
                f"- Date: {item.get('created_at', '')}\n"
                f"  Sun: {item.get('sun_sign', '')}\n"
                f"  Moon: {item.get('moon_sign', '')}\n"
                f"  Ascendant: {item.get('ascendant', '')}\n"
                f"  Career: {item.get('career', '')}\n"
                f"  Finance: {item.get('finance', '')}\n"
                f"  Health: {item.get('health', '')}\n"
                f"  Relationship: {item.get('relationship', '')}"
            )
            for item in history
        ])
    else:
        history_text = "No previous horoscope history available."

    prompt = f"""
You are a warm, thoughtful Vedic horoscope guide.

Current user profile:
- Name: {name}
- Sun Sign: {sun}
- Moon Sign: {moon}
- Ascendant: {asc}

Past horoscope history:
{history_text}

User question:
{question}

Instructions:
- Answer like a human guide, not like a chatbot template.
- Sound supportive, clear, and natural.
- Use the past horoscope history when it helps.
- If you notice a pattern in the user's past readings, mention it in a subtle, helpful way.
- Do not use robotic phrases like "based on the provided information".
- Do not overuse spiritual clichés.
- Avoid extreme claims and avoid certainty about health, money, or life events.
- Keep it personal, grounded, and easy to read.
- Use short paragraphs.
- Keep the answer around 120 to 180 words.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=450
    )

    return response.choices[0].message.content