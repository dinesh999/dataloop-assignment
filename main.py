import argparse
import requests
import sys
from bs4 import BeautifulSoup
import collections

# lists
crawled_urls = []
results = []
depth = 0


# function created
def capture_images_for_given_level(site):
    depth = 3
    for i in range(1, depth+1):
        crawl_website_recursively(site, i)



def crawl_website_recursively(site, depth):
    # getting the request from url
    if (depth >= 2):
        return
    r = requests.get(site)

    # converting the text
    s = BeautifulSoup(r.text, "html.parser")

    for i in s.find_all("a"):

        href = i.attrs['href']

        # if href.startswith("/"):
            # site = site + href

        if href not in crawled_urls:
            crawled_urls.append(href)
            site_response = requests.get(href)
            soup = BeautifulSoup(site_response.text, 'html.parser')
            for item in soup.find_all('img'):
                # print(item['src'])
                results.append({
                    "site": href,
                    "img": item['src'],
                    "depth": depth
                })
            # calling it self
        crawl_website_recursively(href, depth)


def levelOrderTraversal(site, level):
    ans = []

    # Return Null if the tree is empty
    if level == 3:
        return ans

    # Initialize queue
    queue = collections.deque()
    r = requests.get(site)

    # converting the text
    s = BeautifulSoup(r.text, "html.parser")

    for i in s.find_all("a"):

        href = i.attrs['href']
        queue.append(href)

    # Iterate over the queue until it's empty
    while queue:
        # Check the length of queue
        currSize = len(queue)
        currList = []

        while currSize > 0:
            # Dequeue element
            currNode = queue.popleft()
            currList.append(currNode.val)
            currSize -= 1

            # Check for left child
            if currNode.left is not None:
                queue.append(currNode.left)
            # Check for right child
            if currNode.right is not None:
                queue.append(currNode.right)

        # Append the currList to answer after each iteration
        ans.append(currList)

    # Return answer list
    return ans


# main function
if __name__ == "__main__":
    # website to be scrape
    site = "https://www.creativebloq.com/web-design/best-blogging-platforms-121413634"

    # calling function
    crawl_website_recursively(site, depth)
    print(results)
