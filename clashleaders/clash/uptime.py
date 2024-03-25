import requests

url = "https://api.uptimerobot.com/v2/getMonitors"
payload = (
    "api_key=m779046523-0ff280258ee526d52b15679f&format=json&custom_uptime_ratios=14"
)
headers = {
    "content-type": "application/x-www-form-urlencoded",
    "cache-control": "no-cache",
}


def monitor():
    response = requests.request("POST", url, data=payload, headers=headers).json()
    return response["monitors"][0]
