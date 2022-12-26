# To import queue datastructure
import collections
import argparse
import requests
import sys
from bs4 import BeautifulSoup
import collections
import validators


#Assumptions
# 1.Limiting the maximum sites in a given level to 3

class SiteNode:
    # node structure to store the site data
    def __init__(self, val, level):
        self.site = val
        self.level = level


def generateSites(site_node, max_level, current_level):
    while len(queue) > 0 and current_level < max_level:
        # Dequeue node for fetching all the child sites
        currNode = queue.popleft()
        r = requests.get(currNode.site)
        s = BeautifulSoup(r.text, "html.parser")
        current_level = currNode.level
        count = 0
        for i in s.find_all("a"):
            href = i.attrs['href']
            count = count + 1  # counter to fetch the limit of 3 valid urls for a given url
            if validators.url(href): # validate the urls
                node = SiteNode(href, currNode.level+1)
                queue.append(node)
                all_sites_array.append(node)
                if count % 3 == 0:
                    break
    return all_sites_array

def get_all_images():
    for node in all_sites_array:
        if node.level <= depth:
            site_response = requests.get(node.site)
            soup = BeautifulSoup(site_response.text, 'html.parser')
            for item in soup.find_all('img'):  # fetch all the images and store it in results
                # print(item['src'])
                results.append({
                    "site": node.site,
                    "img": item['src'],
                    "depth": node.level
                })
    return


# Check if the algorithm work
if __name__ == "__main__":
    # root = SiteNode("https://www.creativebloq.com/web-design/best-blogging-platforms-121413634", 0)
    root = SiteNode(sys.argv[1], 0)
    queue = collections.deque()   # queue to fetch all the recursive sites for a given site
    all_sites_array = []     # to store all the sites
    results = []
    queue.append(root)
    all_sites_array.append(root)
    current_level = 0
    depth = int(sys.argv[2])
    print(sys.argv[1])
    print(sys.argv[2])
    # print(type(sys.argv[1]))
    # print(type(sys.argv[2]))
    generateSites(root, int(depth), 0)
    get_all_images()
    print(results)
