import wikipedia

def search_wikipedia(search_term):
    # Search for the term and get the top 5 results
    results = wikipedia.search(search_term, results=5)
    
    # List to store titles and summaries
    titles_and_summaries = []
    
    for result in results:
        try:
            # Get the page for each result
            page = wikipedia.page(result)
            # Append the title and summary
            titles_and_summaries.append((page.title, page.summary))
        except wikipedia.exceptions.DisambiguationError as e:
            # Handle disambiguation pages by just listing possible options without details
            titles_and_summaries.append((result, "This page is a disambiguation page."))
        except wikipedia.exceptions.PageError:
            # Handle cases where no page matches the result
            titles_and_summaries.append((result, "No page found for this title."))
    
    return titles_and_summaries

# Example usage
search_results = search_wikipedia("laion ai")
for title, summary in search_results:
    print(f"Title: {title}\nSummary: {summary}\n")
