# 🛡️ AI RAG Security Threat Prioritizer

**An intelligent assistant that helps cybersecurity teams work smarter, not harder.**

---

### 📖 Short Description
Security analysts are often overwhelmed by thousands of alerts every day. This project uses AI to automatically analyze, prioritize, and explain security threats, cutting down the noise so teams can focus on real dangers.

---

### 🚀 Project Overview
The **AI RAG Security Threat Prioritizer** is a tool designed to support Security Operations Centers (SOCs). Instead of just flagging an alert, our system investigates it. It looks up historical data, checks security policies, and uses a Large Language Model (LLM) to provide a complete "Threat Report" with actionable advice.

Think of it as a junior analyst that never sleeps—it triages alerts instantly and tells you exactly **why** something is dangerous and **how** to fix it.

---

### 🔄 System Workflow
Here is how the system processes a security alert, step-by-step:

1.  **Ingestion**: A security alert (e.g., "Suspicious Login") is received.
2.  **Retrieval (RAG)**: The system searches its database for similar past incidents, known threat patterns, or company policies.
3.  **Context Assembly**: It combines the alert details with the retrieved information.
4.  **AI Analysis**: This combined context is sent to the AI (LLM), acting as an expert cyber analyst.
5.  **Output**: The AI generates a structured report containing the Risk Level, Explanation, and Mitigation Steps.
6.  **Dashboard**: The analyst views the prioritized report on an interactive dashboard.

---

### 🛠️ Technologies Used
*   **Python**: The core programming language.
*   **Streamlit**: For building the interactive web dashboard.
*   **OpenAI GPT-4o**: The "brain" that analyzes the threats.
*   **ChromaDB**: The memory (Vector Database) that stores context and past incidents.
*   **Pandas**: For handling data and metrics.

---

### ✨ Key Features
*   **Automated Triage**: Instantly sorts alerts by severity (Critical, High, Medium, Low).
*   **Context-Aware**: Doesn't just guess; uses real past data to inform decisions.
*   **Actionable Advice**: Provides step-by-step instructions on how to contain the threat.
*   **Interactive Dashboard**: A clean, dark-mode UI for analysts to review alerts.
*   **Performance Tracking**: Built-in evaluation scripts to measure time savings and accuracy.

---

### 🏃 How to Run the Project

Follow these simple steps to get started:

1.  **Prerequisites**:
    Make sure you have Python installed and an OpenAI API Key.

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set Up API Key**:
    Set your OpenAI API key in your environment variables.
    *   *Windows (PowerShell)*: `$env:OPENAI_API_KEY="your-key-here"`
    *   *Mac/Linux*: `export OPENAI_API_KEY="your-key-here"`

4.  **Run the Dashboard**:
    ```bash
    streamlit run dashboard.py
    ```

5.  **Run Evaluation (Optional)**:
    To see how well the system performs:
    ```bash
    python evaluation.py
    ```

---

### 📊 Evaluation Metrics
We measure success using the following metrics (check `evaluation.py` for details):
*   **Critical Alerts Accuracy**: How often the AI correctly identifies severe threats.
*   **Response Time Reduction**: The percentage of time saved compared to manual analysis.
*   **Mitigation Relevance**: How useful the AI's suggested fixes are.
*   **Citation Accuracy**: Ensuring the AI references the correct internal docs.

---

### ⚖️ Ethical & Security Considerations
*   **Human in the Loop**: AI is a tool to assist, not replace. A human analyst should always review critical decisions.
*   **Data Privacy**: Ensure sensitive PII (Personally Identifiable Information) is scrubbed before sending data to any external LLM.
*   **Bias Awareness**: We continuously monitor the AI to ensure it treats all alert sources fairly and objectively.

---

### 🎯 Conclusion
The AI RAG Security Threat Prioritizer transforms the chaotic flood of security alerts into a manageable stream of intelligence. By combining the speed of AI with the context of organizational knowledge, we enable security teams to respond faster and more effectively to the threats that matter most.