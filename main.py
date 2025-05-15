from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import csv
from post import Post

POST_LIST_XPATH = '/html/body/div/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/section/div/div'
POST_XPATH = './div/div/div/article/div/div'
POST_TEXT_XPATH = './div[2]/div[2]/div[2]'
POST_TIMESTAMP_XPATH = './div[2]/div[2]/div/div/div/div/div/div[2]/div/div[3]/a/time'
POST_URI_XPATH = './div[2]/div[2]/div/div/div/div/div/div[2]/div/div[3]/a'
POST_REPOST_XPATH = './div/div/div/div/div/div[2]'
POST_USERNAME_XPATH = './div[2]/div[2]/div/div/div/div/div/div[2]/div/div'

# Create Chrome WebDriver and Action object
driver = webdriver.Chrome()
actions = ActionChains(driver)

# Go to X login page
driver.get('https://x.com/i/flow/login')

# Wait for the user to manually log in and navigate to a user's page
input("Press enter once you have manually navigated to an X user's home page.\n")

# Create an empty dictionary to accumulate posts
posts = {}

# Track the last loaded element to determine when all posts have been read
last_element = None

while True:
    # Find the post list element and the relevant individual post elements within the list
    post_list_element = driver.find_element(By.XPATH, POST_LIST_XPATH)
    post_elements = post_list_element.find_elements(By.XPATH, POST_XPATH)

    # Check for end of posts
    if last_element == post_elements[-1]:
        break

    for post_element in post_elements:
        try:
            # Extract data from each post element
            uri = post_element.find_element(By.XPATH, POST_URI_XPATH).get_attribute('href')
            post_id = uri.split('/')[-1]
            timestamp = post_element.find_element(By.XPATH, POST_TIMESTAMP_XPATH).get_attribute('datetime')
            text = post_element.find_element(By.XPATH, POST_TEXT_XPATH).text
            username = post_element.find_element(By.XPATH, POST_USERNAME_XPATH).text
            repost = 'repost' in post_element.find_element(By.XPATH, POST_REPOST_XPATH).text

            # Create a Post object to store the extracted data and add it to the posts dictionary
            post = Post(post_id, uri, timestamp, text, username, repost)
            posts[post_id] = post

        except Exception:
            print('\nERROR!\n')

    last_element = post_elements[-1]
    actions.move_to_element(last_element).perform()
    time.sleep(0.5)
    print(len(posts))

# Write the posts to a CSV file
with open('output/posts.csv', 'w', newline='', encoding='utf-8') as csv_file:
    fieldnames = ['post_id', 'uri', 'timestamp', 'text', 'username', 'repost']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()
    for post in posts.values():
        writer.writerow(
            {
                'post_id': post.post_id,
                'uri': post.uri,
                'timestamp': post.timestamp,
                'text': post.text,
                'username': post.username,
                'repost': post.repost
            }
        )
