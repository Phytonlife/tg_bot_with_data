def get_post_template(style_num=1):
    templates = {
        1: """
🔥 Новая вакансия!

📋 {title}
🏢 Компания: {company}
📍 Локация: {location}

📝 Описание:
{description}

📅 Актуально до: {end_date}

👉 Откликнуться: {apply_button}
""",
        2: """
💼 ВАКАНСИЯ ДНЯ 💼

⭐️ {title} ⭐️
━━━━━━━━━━━━━━━
📍 {location}
🏢 {company}

🔍 О работе:
{description}

⏰ До: {end_date}
━━━━━━━━━━━━━━━
{apply_button}
"""
    }
    return templates.get(style_num, templates[1])