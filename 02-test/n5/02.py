import requests as rq
import json

hd = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 7.1.2; AFTMM Build/NS6265; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/70.0.3538.110 Mobile Safari/537.36',
}

url = 'https://api.github.com/user/repos?page=3'

session = rq.Session()
username = 'fernando_1999_ticona_@hotmail.com',
password = 'nix_git96dgfake',

rs = rq.get(url, headers=hd, auth=(username, password))

repos = rs.json()

for repo in repos:
    print(repo['name'])
    
