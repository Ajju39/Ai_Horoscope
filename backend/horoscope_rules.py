def generate_horoscope_reading(sun_sign: str, moon_sign: str, ascendant: str):
    finance_map = {
        "Aries": "You may do well when taking bold but calculated financial steps.",
        "Taurus": "You are naturally steady with money and may benefit from long-term planning.",
        "Gemini": "Your finances may improve through communication, networking, or multiple income ideas.",
        "Cancer": "You may prefer financial security and careful savings over risk.",
        "Leo": "You may attract opportunities when you confidently present your skills.",
        "Virgo": "Financial progress may come through discipline, detail, and smart budgeting.",
        "Libra": "Partnerships and balanced decisions can support financial growth.",
        "Scorpio": "You may do well when making strategic and deeply researched money decisions.",
        "Sagittarius": "Growth may come from learning, travel, or trying new opportunities carefully.",
        "Capricorn": "You tend to build wealth slowly and steadily through consistency.",
        "Aquarius": "Creative ideas and unconventional paths may help your finances.",
        "Pisces": "You may benefit from mixing intuition with practical money management."
    }

    career_map = {
        "Aries": "You are likely to thrive in action-oriented roles and leadership situations.",
        "Taurus": "You may do best in stable careers where patience and consistency matter.",
        "Gemini": "You may shine in communication, analysis, sales, or fast-changing work.",
        "Cancer": "You may excel in supportive, people-focused, or caregiving environments.",
        "Leo": "Recognition and visibility can play a big role in your career growth.",
        "Virgo": "You may do well in analytical, structured, and service-based roles.",
        "Libra": "You may thrive in collaboration, negotiation, and relationship-driven careers.",
        "Scorpio": "You may do well in deep research, investigation, transformation, or strategy.",
        "Sagittarius": "You may enjoy careers involving learning, movement, or expansion.",
        "Capricorn": "Career success may come through discipline, persistence, and long-term planning.",
        "Aquarius": "Innovation, technology, and unconventional thinking may support your career.",
        "Pisces": "You may be drawn to creative, healing, or intuitive career paths."
    }

    health_map = {
        "Aries": "Focus on balancing your energy levels and avoiding burnout from overexertion.",
        "Taurus": "Consistency in food, sleep, and routine may support your well-being.",
        "Gemini": "Mental rest and stress management may be especially important for you.",
        "Cancer": "Emotional balance can strongly influence your physical wellness.",
        "Leo": "A healthy routine with movement and confidence-building habits may help you most.",
        "Virgo": "You may feel best when daily habits, diet, and routine stay organized.",
        "Libra": "Balance is key—avoid extremes in work, food, or rest.",
        "Scorpio": "Inner stress may affect health, so emotional release and recovery matter.",
        "Sagittarius": "Movement, outdoor activity, and freedom in routine may support your health.",
        "Capricorn": "Discipline and consistency can be your biggest strength in health matters.",
        "Aquarius": "You may benefit from unique wellness approaches and a flexible routine.",
        "Pisces": "Rest, hydration, and emotional calm may be especially valuable for you."
    }

    relationship_map = {
        "Aries": "You may be passionate and direct in relationships, valuing honesty and energy.",
        "Taurus": "You may seek loyalty, comfort, and emotional stability in relationships.",
        "Gemini": "Communication and mental connection may matter greatly to you.",
        "Cancer": "You may value emotional safety, care, and deep bonds.",
        "Leo": "Warmth, affection, and appreciation may be central in your relationships.",
        "Virgo": "You may show love through care, support, and thoughtful actions.",
        "Libra": "Harmony, fairness, and companionship may define your relationship style.",
        "Scorpio": "You may form deep, intense, and loyal emotional connections.",
        "Sagittarius": "You may value freedom, honesty, and growth in relationships.",
        "Capricorn": "You may be serious and dependable in long-term commitments.",
        "Aquarius": "Friendship, individuality, and shared ideas may matter most to you.",
        "Pisces": "You may bring empathy, softness, and emotional depth into relationships."
    }

    return {
        "finance": finance_map.get(sun_sign, "Financial growth may come through balance and planning."),
        "career": career_map.get(ascendant, "Career progress may come through self-awareness and steady effort."),
        "health": health_map.get(moon_sign, "Health improves when you maintain a balanced lifestyle."),
        "relationship": relationship_map.get(moon_sign, "Relationships may improve through honesty and emotional awareness.")
    }