"""
API Comparison for JobCraftAI - Different LLM providers
"""

# 1. OpenAI GPT-4 (Current - Best Quality)
def openai_gpt4(prompt, api_key):
    from openai import OpenAI
    client = OpenAI(api_key=api_key)
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Cost-effective
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )
    return response.choices[0].message.content

# 2. Anthropic Claude (Excellent Alternative)
def anthropic_claude(prompt, api_key):
    import anthropic
    
    client = anthropic.Anthropic(api_key=api_key)
    
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

# 3. Google Gemini (Cost-Effective)
def google_gemini(prompt, api_key):
    import google.generativeai as genai
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
    
    response = model.generate_content(prompt)
    return response.text

# 4. Mistral AI (EU-based)
def mistral_ai(prompt, api_key):
    from mistralai.client import MistralClient
    from mistralai.models.chat_completion import ChatMessage
    
    client = MistralClient(api_key=api_key)
    
    response = client.chat(
        model="mistral-large-latest",
        messages=[ChatMessage(role="user", content=prompt)]
    )
    return response.choices[0].message.content

# Cost comparison for your use case
COST_COMPARISON = {
    "OpenAI GPT-4o-mini": "$2-5/month",
    "Anthropic Claude 3.5": "$1-3/month", 
    "Google Gemini Pro": "$0.50-1/month",
    "Mistral Large": "$1-2/month"
}

# Quality comparison
QUALITY_RANKING = {
    "1. OpenAI GPT-4": "Best overall quality",
    "2. Anthropic Claude": "Excellent, often better for long texts",
    "3. Google Gemini": "Good quality, very cost-effective",
    "4. Mistral AI": "Good quality, EU-based"
}
