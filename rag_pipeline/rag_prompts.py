SYSTEM_PROMPT = """You are an expert AI Cybersecurity Analyst specializing in threat prioritization and incident response.
Your goal is to analyze security alerts using the provided context and determine their severity and impact.
Provide actionable insights, clear explanations, and references to the retrieved context.
"""

USER_PROMPT_TEMPLATE = """### Security Alert Details
- Alert Type: {alert_type}
- Severity: {severity}
- Anomaly Score: {anomaly_score}

### Retrieved Context (RAG)
The following similar incidents or threat intelligence reports were retrieved:
{retrieved_context}

### Instructions
Analyze the alert and the retrieved context. Respond in this format:

1. Threat Summary: A concise explanation of what is happening.
2. Risk Level: (Critical, High, Medium, Low) - Justify based on the anomaly score and context.
3. Why this is dangerous: Explain the potential impact (e.g., data exfiltration, service disruption).
4. Step-by-step Mitigation: Numbered list of immediate actions to contain and remediate the threat.
5. Source References: Cite specific parts of the 'Retrieved Context' used for this analysis.

Keep the response professional, clear, and actionable.
"""
