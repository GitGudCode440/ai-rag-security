import os
from openai import OpenAI
from rag_prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

alert_data = {
    "alert_type": "Multiple Failed Login Attempts",
    "severity": "High",
    "anomaly_score": "0.92",
    "retrieved_context": "These login attempts match known brute-force patterns from previous incidents."
}

prompt = USER_PROMPT_TEMPLATE.format(**alert_data)

try:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    print(response.choices[0].message.content)

except Exception as e:
    print(f"Error calling OpenAI API: {e}")
