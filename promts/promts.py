# prompts.py

PROMPTS = {
    "highest_lowest_rating": """
You are an expert data analyst specializing in JSON data extraction and summarization.

Given the following list of Amazon products, each with the fields: name, link, price_complete, price_symbol, and reviews (formatted like "4.8 out of 5 stars" or "0 reviews"):

Please perform these tasks clearly and strictly following the instructions:

1. List the product(s) with the highest rating (numerical value), showing:
   - Product name
   - Rating as a number (e.g., 4.8)
   - URL link (use exactly the 'link' field from the data without any modification)

2. List the product(s) with the lowest rating (numerical value), excluding any product with "0 reviews", showing:
   - Product name
   - Rating as a number
   - URL link (exactly as in the 'link' field)

3. Provide the total number of products analyzed.

4. Briefly mention if any products have "0 reviews" and list their names.

IMPORTANT:
- Always include the link exactly as it appears in the 'link' field.
- Do not paraphrase, shorten, or omit any URLs.
- Format your answer as a clear, numbered text list.
- Do not output JSON or any other format.

Here is the data:
{data}

Answer clearly and concisely in English.
""",

    "detailed_product_analysis": """
You are a meticulous and expert product analyst specializing in extracting detailed insights from product data.

Given the following Amazon product JSON with fields: 
- name
- price_complete
- price_symbol
- reviews (e.g., "4.8 out of 5 stars")
- about_item (detailed product description)
- colors (list of option objects with 'display_name')
- link

Please perform a thorough analysis and generate a clear, professional, and engaging summary that includes:

- A concise introduction naming the product and its price.
- The overall customer rating expressed numerically and what it implies.
- A breakdown of the key features and benefits described in 'about_item'.
- Insights about the variety of colors, editions or options available.
- Suggestions about the product's ideal use cases or target audience.
- The product URL exactly as provided.
- Use natural, flowing language suitable for an informed buyer considering this product.

Do NOT output any JSON or code, just a well-structured natural language paragraph or two.

Here is the data:
{data}

Answer clearly and professionally in English.
""",
"compare_products": """
You are a product expert. Critically compare the following products and provide a detailed analysis:

Products: {data}

For each product, provide:
1. Key strengths
2. Key weaknesses
3. Overall recommendation

Output in a clear, structured format, ideally as a list with each product and its analysis.
"""
}