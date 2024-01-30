import argparse
import requests
from concurrent.futures import ThreadPoolExecutor

def test_path(base_url, path, wordlist_path, max_depth, current_depth):
    try:
        url = f"{base_url}/{path.strip()}"
        response = requests.get(url)
        if response.status_code != 404:
            print(f"Found: {url}")
            if current_depth < max_depth:
                enumerate_paths(url, wordlist_path, max_depth, current_depth + 1)
    except requests.RequestException as e:
        print(f"Error checking {url}: {e}")

def enumerate_paths(base_url, wordlist_path, max_depth, current_depth=0, max_threads=10):
    with open(wordlist_path, 'r') as file:
        paths = [line.strip() for line in file if line.strip() and not line.startswith('#')]

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = [executor.submit(test_path, base_url, path, wordlist_path, max_depth, current_depth) for path in paths]
        for future in concurrent.futures.as_completed(futures):
            pass  # Future results or exceptions can be handled here if needed

def main():
    parser = argparse.ArgumentParser(description="Web Directory Enumeration Script with Recursion")
    parser.add_argument("-u", "--url", required=True, help="Target URL")
    parser.add_argument("-w", "--wordlist", required=True, help="Path to the wordlist file")
    parser.add_argument("-r", "--recursive", type=int, default=0, help="Recursion depth")
    
    args = parser.parse_args()

    enumerate_paths(args.url, args.wordlist, args.recursive)

if __name__ == "__main__":
    main()
