import requests
from bs4 import BeautifulSoup

def fetch_web_content(url):
    # This 'Header' makes it look like a real browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/110.0'
    }
    
    try:
        # Pass the headers into the request
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove junk
            for script_or_style in soup(["script", "style", "header", "footer", "nav"]):
                script_or_style.decompose()

            text = soup.get_text()
            # Clean up the spacing
            lines = (line.strip() for line in text.splitlines())
            clean_text = '\n'.join(line for line in lines if line)
            
            return clean_text[:2000] 
        else:
            return f"Access Denied. Status: {response.status_code}"
            
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    test_url = "https://en.wikipedia.org/wiki/Artificial_intelligence"
    print(f"--- Fetching content from {test_url} ---")
    print(fetch_web_content(test_url))