import pandas as pd

def calculate_metrics(results_df):
    """
    Calculates key performance indicators for the AI RAG System.
    """
    metrics = {}

    # 1. Critical Alerts Accuracy
    # Calculate how often the AI correctly identified 'Critical' or 'High' threats compared to Ground Truth
    # We treat 'Critical' and 'High' as positive classes for this specific metric
    critical_mask = results_df['Ground_Truth_Risk'].isin(['Critical', 'High'])
    accurate_predictions = results_df[critical_mask]['AI_Risk_Level'] == results_df[critical_mask]['Ground_Truth_Risk']
    metrics['Critical Alerts Accuracy'] = accurate_predictions.mean()

    # 2. Mitigation Relevance Score (Average)
    # This assumes a score (0-10) is assigned to the AI's mitigation steps by a human reviewer or advanced eval model
    metrics['Avg Mitigation Relevance Score'] = results_df['Mitigation_Quality_Score'].mean()

    # 3. Response Time Reduction (%)
    # Compare Manual Analysis Time vs AI Analysis Time
    total_manual_time = results_df['Manual_Time_Mins'].sum()
    total_ai_time = results_df['AI_Time_Mins'].sum()
    metrics['Response Time Reduction (%)'] = ((total_manual_time - total_ai_time) / total_manual_time) * 100

    # 4. RAG Citation Accuracy
    # Percentage of times the AI correctly cited the expected source document
    metrics['RAG Citation Accuracy'] = (results_df['Correct_Citation_Found'] == True).mean()

    return metrics

if __name__ == "__main__":
    print("--- 🛡️ AI RAG Security Threat Prioritizer - Evaluation Module ---")

    # Sample Test Data
    # In a real scenario, this would be collected from logs or user feedback loops
    test_data = [
        {
            "Alert_ID": 101,
            "Alert_Type": "Suspicious Login",
            "Ground_Truth_Risk": "High",
            "AI_Risk_Level": "High",
            "Mitigation_Quality_Score": 9.5,  # Score out of 10
            "Manual_Time_Mins": 15,           # Time taken by human analyst
            "AI_Time_Mins": 0.5,              # Time taken by AI
            "Correct_Citation_Found": True    # Did AI cite the correct policy/log?
        },
        {
            "Alert_ID": 102,
            "Alert_Type": "SQL Injection",
            "Ground_Truth_Risk": "Critical",
            "AI_Risk_Level": "Critical",
            "Mitigation_Quality_Score": 10.0,
            "Manual_Time_Mins": 30,
            "AI_Time_Mins": 0.5,
            "Correct_Citation_Found": True
        },
        {
            "Alert_ID": 103,
            "Alert_Type": "False Positive Ping",
            "Ground_Truth_Risk": "Low",
            "AI_Risk_Level": "Medium",     # AI overestimated this one
            "Mitigation_Quality_Score": 7.0,
            "Manual_Time_Mins": 5,
            "AI_Time_Mins": 0.4,
            "Correct_Citation_Found": False # Missed specific context
        },
        {
            "Alert_ID": 104,
            "Alert_Type": "Data Exfiltration",
            "Ground_Truth_Risk": "Critical",
            "AI_Risk_Level": "Critical",
            "Mitigation_Quality_Score": 9.0,
            "Manual_Time_Mins": 45,
            "AI_Time_Mins": 0.6,
            "Correct_Citation_Found": True
        }
    ]

    # Create DataFrame
    df = pd.DataFrame(test_data)
    
    print(f"\nEvaluating on {len(df)} sample alerts...\n")
    print("--- Detailed Test Results ---")
    print(df[['Alert_ID', 'Ground_Truth_Risk', 'AI_Risk_Level', 'AI_Time_Mins']])

    # Calculate Metrics
    results = calculate_metrics(df)

    # Display Output
    print("\n" + "="*40)
    print("📊 PERFORMANCE REPORT")
    print("="*40)
    for metric, value in results.items():
        # Format percentages and scores nicely
        if "Accuracy" in metric or "%" in metric:
            print(f"{metric:<30}: {value:.1%}") # Display as percentage
        else:
            print(f"{metric:<30}: {value:.2f} / 10.0")
    print("="*40)
    
    print("\n✅ Evaluation complete. The system demonstrates significant time savings.")
