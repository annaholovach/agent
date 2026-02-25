from duckduckgo_search import DDGS

def search_tool(query):
    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=5)
        if not results:
            return "No relevant results found."

        candidate_texts = []
        for r in results:
            text = r["body"]
            paragraphs = [p.strip() for p in text.split("\n") if len(p.strip()) > 30]
            candidate_texts.extend(paragraphs)

        if not candidate_texts:
            return "No relevant results found."

        top_paragraphs = candidate_texts[:3]

        combined = "\n\n".join(top_paragraphs)
        return combined