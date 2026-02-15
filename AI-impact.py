import pandas as pd
import json

# Load your 200 reviews
with open('Intercom_200.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

rows = []
for review in data:
    row = {
        'review_id': review.get('review_id'),
        'publish_date': review.get('publish_date'),
        'rating': review.get('review_rating'),
        'company_size': review.get('reviewer_company_size'),
        'job_title': review['reviewer'].get('reviewer_job_title') if review.get('reviewer') else None,
        'full_content': review.get('review_content')
    }
    
    # AI Keywords to flag strategy-relevant reviews
    ai_keywords = ['ai', 'bot', 'fin', 'automation', 'copilot', 'gpt', 'intelligence']
    content_lower = row['full_content'].lower()
    row['is_ai_relevant'] = any(word in content_lower for word in ai_keywords)
    
    rows.append(row)

df = pd.DataFrame(rows)
# Save as CSV for BigQuery
df.to_csv('intercom_reviews_v1.csv', index=False)

print(f"Dataset ready: {len(df)} reviews.")
print(f"Reviews mentioning AI: {df['is_ai_relevant'].sum()} ({(df['is_ai_relevant'].sum()/len(df))*100:.1f}%)")