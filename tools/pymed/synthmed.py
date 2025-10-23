from pymed import PubMed

# Instantiate PubMed with your tool name and email
pubmed = PubMed(tool="SynthMed", email="jaywarfield@gmail.com")

# Define a search query
query = "COVID-19 treatment"

# Execute the query
results = pubmed.query(query, max_results=10)

# Iterate through the results and print article titles
for article in results:
    print(article.title)

