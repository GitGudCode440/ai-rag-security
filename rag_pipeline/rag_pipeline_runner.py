import os
import chromadb
from openai import OpenAI
from rag_prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE

# Initialize ChromaDB (Using in-memory mode for easy testing)
# We initialize this once when the module is loaded
chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="threat_intelligence")

# Add some sample threat intelligence data
sample_documents = [
    "Incident #1024: Brute-force attack detected from IP 192.168.1.100 targeting SSH.",
    "Threat Report: 'Midnight Blizzard' often uses password spraying against valid accounts.",
    "Incident #1025: Multiple failed logins for user 'admin' followed by a successful login from a new device.",
    "policy_doc_v2.txt: 5 failed attempts within 1 minute requires temporary account lockout.",
    "Malware Analysis: 'Cobalt Strike' beacons often use HTTP over port 8080 with jitter.",
    "CVE-2024-XXXX: Critical SQL Injection vulnerability in login forms allowing data exfiltration."
]
collection.add(
    documents=sample_documents,
    ids=[f"doc{i}" for i in range(len(sample_documents))]
)

def get_openai_client():
    """Safely get OpenAI client, returns None if key is missing."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    return OpenAI(api_key=api_key)

def query_rag_llm(alert_type, severity, anomaly_score, description):
    """
    Retrieves context and queries the LLM to analyze the alert.
    Returns the formatted text response.
    """
    client = get_openai_client()
    if not client:
        return "⚠️ **Error**: `OPENAI_API_KEY` is not set in environment variables. Please set it to run the AI analysis."

    # 1. Retrieve Context
    try:
        results = collection.query(
            query_texts=[description],
            n_results=2
        )
        retrieved_text = "\n".join(results['documents'][0]) if results['documents'] else "No relevant context found."
    except Exception as e:
        return f"Error retrieving context: {e}"

    # 2. Format Prompt
    prompt_data = {
        "alert_type": alert_type,
        "severity": severity,
        "anomaly_score": anomaly_score,
        "retrieved_context": retrieved_text
    }
    formatted_prompt = USER_PROMPT_TEMPLATE.format(**prompt_data)

    # 3. Call LLM
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": formatted_prompt}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error calling OpenAI API: {e}"

if __name__ == "__main__":
    # Test run
    print("Running test analysis...")
    report = query_rag_llm(
        "Suspicious Login Attempt", 
        "High", 
        "0.89", 
        "User account detected with high volume of failed logins consistent with brute-force patterns."
    )
    print(report)
