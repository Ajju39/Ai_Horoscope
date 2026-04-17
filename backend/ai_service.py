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

Style:
- Sound warm, natural, and human.
- Write like a wise, practical guide — not like an AI assistant.
- Avoid robotic phrases like "based on the information provided", "it is important to note", or "you may find that".
- Avoid sounding overly mystical, dramatic, or vague.
- Do not overuse headings, bullet points, or repeated sentence patterns.
- Use short paragraphs and smooth transitions.
- Be personal, grounded, and easy to read.
- Use contractions naturally where they fit.
- Avoid certainty about health, money, or life events.

Content:
- Talk about personality, career, finance, health, and relationships in a natural flow.
- End with 3 practical, realistic tips.

Length:
- Around 250 to 400 words.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You write in a warm, human, conversational tone and avoid sounding generic or robotic."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.9,
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

Current profile:
- Name: {name}
- Sun Sign: {sun}
- Moon Sign: {moon}
- Ascendant: {asc}

Past horoscope history:
{history_text}

User question:
{question}

Style:
- Answer like a real person talking naturally.
- Sound supportive, clear, and warm.
- Do not sound like a chatbot template.
- Avoid phrases like "based on the data", "according to the information", or "it is important to note".
- Avoid overused mystical clichés.
- Use short paragraphs.
- Keep it grounded and practical.
- If past readings show a pattern, mention it gently and naturally.
- Do not make extreme claims.
- Vary sentence length and avoid making every paragraph sound the same.
- Write as if you are talking to one person, not writing a report.

Length:
- Around 120 to 180 words.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a warm, perceptive guide. Your tone should feel human, natural, and emotionally intelligent."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.95,
        max_tokens=450
    )

    return response.choices[0].message.content