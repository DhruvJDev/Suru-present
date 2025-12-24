import os
import webbrowser
from datetime import datetime

import module.speak as speak


# import speak as speak

def search_on_google(query):
    """
    Opens a Google search for the given query.
    """
    search_query = query.replace(' ', '+')
    google_url = f"https://www.google.com/search?q={search_query}"
    webbrowser.open(google_url)
    # speak.say("Searching on Google.")

    log_search_history(query)


def log_search_history(query):
    folder_path = "data/search_history"
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, "search_history.txt")

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(file_path, "a") as file:
        file.write(f"{now}\nQuery: {query}\n")
        file.write("-" * 40 + "\n\n")