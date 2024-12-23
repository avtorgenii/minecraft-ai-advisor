from duckduckgo_search import DDGS

# Your search query
query = "how much lp does tier 4 blood altar store max"

# Perform the search
results = DDGS().text(query, max_results=2)

# Display the results
for result in results:
    print(result)
