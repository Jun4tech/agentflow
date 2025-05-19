from vector_store import VectorStore
import pandas as pd

pd.set_option("display.max_colwidth", None)
pd.set_option("display.width", None)
vec = VectorStore()

relevant_question = "Who are the top 3 spenders in last 3 years?"
semantic_results = vec.semantic_search(relevant_question, limit=40)
keyword_results = vec.keyword_search(relevant_question, limit=5)
hybrid_results = vec.hybrid_search(
    query=relevant_question, top_n=5, keyword_k=5, semantic_k=5
)

print(f"Questions: {relevant_question}")
# Combine 'content' and 'distance' columns into a single DataFrame and print
df = pd.DataFrame(
    {"Content": semantic_results["content"], "Distance": semantic_results["distance"]}
)
df = df.sort_values(by="Distance", ascending=True)
print(df)
