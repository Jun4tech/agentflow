from vector_store import VectorStore
import pandas as pd

pd.set_option("display.max_colwidth", None)
pd.set_option("display.width", None)
vec = VectorStore()

relevant_question = "Who are the top spends in the past 3 years?"
semantic_results = vec.semantic_search(relevant_question, limit=5)
keyword_results = vec.keyword_search(relevant_question, limit=5)
hybrid_results = vec.hybrid_search(
    query=relevant_question, top_n=5, keyword_k=5, semantic_k=5
)

print(f"Semantic Results: {semantic_results['content']}")
