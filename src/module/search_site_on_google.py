import webbrowser
import os
from datetime import datetime

import module.speak as speak


# import speak as speak

def search_site_on_google(query):
    """
    Opens a website URL. Defaults to .com unless domain is mentioned.
    """
    query = query.lower().strip().replace(" ", "")  # final cleanup

    if "." in query:
        url = f"https://{query}"
    else:
        url = f"https://{query}.com"

    print(f"\nFinal URL: {url}")
    webbrowser.open(url)
    # speak.say("Searching...")

    log_search_history(query)


def log_search_history(query):
    folder_path = "data/search_history"
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, "search_history.txt")

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(file_path, "a") as file:
        file.write(f"{now}\nQuery: {query}\n")
        file.write("-" * 40 + "\n\n")

if __name__ == "__main__":
    test_query = input("Enter a website to open (e.g., example.com or example): ")
    print(f"Testing search_site_on_google with query: {test_query}")
    search_site_on_google(test_query)