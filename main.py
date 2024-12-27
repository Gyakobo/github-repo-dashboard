import requests

# Colored console output
# ANSI escape sequences for text colors
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
RESET = "\033[0m"

# Read Config file
with open('config.txt', 'r') as file:
    lines file.readlines()

# Replace these with your GitHub username and token
GITHUB_USERNAME = ''
TOKEN = ''

# Headers with authentication
headers = {
    'Authorization': f'token {TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}

# Get all repositories
repos_url = f'https://api.github.com/users/{GITHUB_USERNAME}/repos'
response = requests.get(repos_url, headers=headers)
repos = response.json()

repo_response = []

def get_daily_traffic(repo_name, owner=GITHUB_USERNAME):
    # Traffic views URL
    traffic_url = f'https://api.github.com/repos/{owner}/{repo_name}/traffic/views'

    # Make the request
    response = requests.get(traffic_url, headers=headers)

    if response.status_code == 200:
        traffic_data = response.json()

        if not traffic_data.get('views', []):
            print(f"{RED}No views{RESET}")
            return

        print(f"Repository: {repo_name}")
        print(f"{GREEN}Date       {RESET}| {YELLOW}Views {RESET}| {RED}Uniques{RESET}")
        print("-" * 30)

        for view in traffic_data.get('views', []):
            date = view["timestamp"][:10] # Extract date(YYYY-MM-DD)
            count = view["count"]
            uniques = view["uniques"]
            print(f"{GREEN}{date} {RESET}| {YELLOW}{count:5} {RESET}| {RED}{uniques:7}{RESET}")
        print("-" * 30)
    else:
        print(f"Failed to fetch traffic data for {repo_name} (Status Code: {response.status_code})")


def get_traffic_with_sources(repo_name, owner=GITHUB_USERNAME):
    # Traffic views URL
    traffic_views_url = f'https://api.github.com/repos/{owner}/{repo_name}/traffic/views'
    traffic_referrers_url = f'https://api.github.com/repos/{owner}/{repo_name}/traffic/popular/referrers'
    
    # Fetch traffic referrers
    referrers_response = requests.get(traffic_referrers_url, headers=headers)
    
    if referrers_response.status_code == 200:
        referrers_data = referrers_response.json()
        
        # Display referrer data
        if not referrers_data:
            print(f"No referrer data available for {repo_name}.")
        else:
            print("Top Referrers:")
            print("Source               | Views | Uniques")
            print("-" * 40)
            for referrer in referrers_data:
                source = referrer['referrer']
                count = referrer['count']
                uniques = referrer['uniques']
                print(f"{source:<20} | {count:5} | {uniques:7}")
            print("-" * 40)
    else:
        print(f"Failed to fetch referrer data for {repo_name} (Status Code: {referrers_response.status_code})")

# Example usage
get_traffic_with_sources('your_github_username', 'repo_name')



# The GitHub API only provides repository traffic data for the last 14 days 
# in an aggregated form (total views and unique visitors), but it also 
# includes detailed daily statistics within that 14-day window. 
# To extract daily views, you can use the endpoint:

# Fetch traffic data for each repository
for repo in repos:
    repo_name = repo['name']
    owner = repo['owner']['login']
    traffic_url = f'https://api.github.com/repos/{owner}/{repo_name}/traffic/views'
    
    traffic_response = requests.get(traffic_url, headers=headers)
    if traffic_response.status_code == 200:
        
        traffic_data = traffic_response.json()

        repo_response.append( {
            "Repository": repo_name,
            "Views": traffic_data['count'],
            "Unique Views": traffic_data['uniques']
        })

        print(f"Repository: {BLUE}{repo_name}{RESET}")
        print(f"Views: {GREEN}{traffic_data['count']}{RESET} | Unique Views: {YELLOW}{traffic_data['uniques']}{RESET}", end='\n')
        
        get_daily_traffic(repo_name=repo_name)
        get_traffic_with_sources(repo_name=repo_name)
        # print("-" * 40, end='\n')
        print(end='\n\n')
    else:
        print(f"Failed to fetch traffic data for {repo_name}")
