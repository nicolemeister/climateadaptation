import re

# Test the sentence splitting logic
test_text = """The Asian Development Bank (ADB) will design projects to help build climate resilience of infrastructure in Azerbaijan, Trend reports citing the Bank's Country Partnership Strategy for Azerbaijan for 2025-2029.

"Azerbaijan is subject to multiple natural hazards that can derail sustained economic growth. Water scarcity poses a significant threat to agricultural production, employment, water supply, and hydroelectric power generation. Glacial melt threatens to bring severe flooding, land degradation, and damage to infrastructure such as reservoirs. To mitigate these risks, ADB will design projects based on a thorough analysis of climate and disaster vulnerability risks to help build the climate resilience of infrastructure and protect ecosystems and vulnerable communities. Measures to support climate adaptation and stronger disaster risk management are integral to this Country Partnership Strategy," reads the document.

ADB notes that Azerbaijan has an abundance of natural resources and a diverse range of climate zones. Although the country contributes only 0.1% to global greenhouse gas (GHG) emissions, it faces significant climate change impacts, including desertification, emerging water scarcity, and sea level decline."""

# Remove HTML tags (simulating the clean_data.py logic)
content_text = re.sub(r'<.*?>', '', test_text)

# Split into sentences (same logic as clean_data.py)
sentence_splitter = re.compile(r'(?<=[.!?])\s+')
sentences = sentence_splitter.split(content_text)

print("Number of sentences found:", len(sentences))
print("\nSentences:")
for i, sent in enumerate(sentences):
    print(f"{i+1}: {sent.strip()[:100]}...")

# Test keyword search
keyword = "climate adaptation"
keyword_pattern = re.compile(re.escape(keyword), re.IGNORECASE)

print(f"\nSearching for '{keyword}':")
for idx, sent in enumerate(sentences):
    if keyword_pattern.search(sent):
        print(f"Found in sentence {idx+1}: {sent.strip()}")
        
        # Get context (2 before, current, 2 after)
        prev2_sent = sentences[idx-2].strip() if idx > 1 else ""
        prev1_sent = sentences[idx-1].strip() if idx > 0 else ""
        next1_sent = sentences[idx+1].strip() if idx < len(sentences)-1 else ""
        next2_sent = sentences[idx+2].strip() if idx < len(sentences)-2 else ""
        
        snippet_parts = []
        if prev2_sent:
            snippet_parts.append(prev2_sent)
        if prev1_sent:
            snippet_parts.append(prev1_sent)
        snippet_parts.append(sent.strip())
        if next1_sent:
            snippet_parts.append(next1_sent)
        if next2_sent:
            snippet_parts.append(next2_sent)
        
        snippet = " ".join(snippet_parts)
        print(f"Context snippet ({len(snippet_parts)} parts): {snippet}")
