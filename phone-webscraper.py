# Make sure to import with "pip install selenium"

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import re
import random
import time

option = webdriver.ChromeOptions()
option.add_argument('--headless')
browser = webdriver.Chrome(ChromeDriverManager().install(), options=option)
browser.get('https://www.craigslist.org')

post = ""
resultStr = ""
indexed = []
filtered = []

# define pattern recognition for phone numbers
num = re.compile('\d\d\d[\s_-]\d\d\d[\s_-]\d\d\d\d|\d\d\d\d\d\d\d\d\d\d|\(\d\d\d\)[\s_-]\d\d\d[\s_-]\d\d\d\d')

# take input for what category to search
category = input(
    "What category would you like to search? \naos = automotive\nbts = beauty services\ncms = cell phone/mobile services\ncps = computer services\ncrs = creative services\ncys = cycle services\nevs = event services\nfgs = farm + garden services\nfns = financial services\nhws = health/welness services\nhss = household services\nlbs = labor/move\nlgs = legal services\nlss = lessons\nmas = marine services\npas = pet services\nrts = real estate\nsks = skilled trade\nbiz = small business ads\ntrv = travel/vacation services\nwet = writing/editing/translation\nCategory tag must be entered as displayed(lowercase, 3 letters)")

# take input for amount of posts to search. Would do specific number of posts, but rounding integers to nearest 120 is too complicated for a tired high school student
count = int(input("How many pages of posts would you like to search(each page has 120 posts)"))
print(f'{count * 120} + " posts will be searched.")

# take input for how to output numbers
while True:
    output = input("How would you like to output found numbers? f = output to .txt file, t = list in terminal, tf = both")
    if output == "f" or output == "t" or output == "tf":
        break
    else:
        print("Invalid input. Please enter one of the provided options.")
        continue

# search for that element
browser.find_element_by_class_name(category).click()


# defines the method for extracting phone number from post body
def extract_phone(post):
    match = num.search(post)
    if match is None:
        return None
    return match.group(0)


postLinks = []
# get array of links to posts for later use
for x in range(count):
    posts = browser.find_elements_by_xpath('/html/body/section/form/div[4]/ul/li/a')
    for j in posts:
        postLinks.append(j.get_attribute('href'))
    print("Update: Posts acquired. Extracting phone #s...")

    browser.find_element_by_partial_link_text('next').click()

z = 1
# cycle through links and search the post for phone number, index phone number
for x in postLinks:
    browser.get(x)
    post = browser.find_element_by_id('postingbody').text
    indexed.append(extract_phone(post))
    print("[Index #:" + str(z) + "]" + "[Link: " + x + "] [Return: " + str(extract_phone(post)) + "]")
    z = z + 1
print("Update: Phone #s extracted. Indexing and filtering...")

# 1st filter: remove non-phone number returns
for x in indexed:
    if x is not None:
        filtered.append(x)
    else:
        continue

# 2nd filter: remove unwanted characters
filtered2 = []
for y in filtered:
    y = y.replace("(", "")
    y = y.replace(")", "")
    y = y.replace("-", "")
    y = y.replace(" ", "")
    y = y.replace("_", "")
    filtered2.append(y)

# 3rd filter: remove duplicates
f2 = set(filtered2)


if output == "t" or output == "tf":
    print(f"{len(f2)}  numbers were found.")
    # print list
    for x in f2:
        print(x)

if output == "f" or output == "tf":
    file = open("numbers.txt", "w")
    for x in f2:
        file.write(x + "\n")
    file.close()

