from selenium import webdriver
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.chrome.options import Options 
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
from login_info import username, password
options = Options()
options.add_experimental_option("detach", True) # Keeps the driver open even after function finishes

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), 
                          options=options)
#Get the website 
driver.get("https://piazza.com")



#Obtain the sign up link 
link = driver.find_element("xpath", '//*[@id="login_button"]')
link.click()

# Obtain the signup Fields and upload sign in information 
time.sleep(1)

input_field_1 = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[3]/form/div[1]/div[1]/div/input')
input_field_1.click()
input_field_1.send_keys(username) # Your account email 

input_field_2 = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[3]/form/div[1]/div[2]/div/input')
input_field_2.click()
input_field_2.send_keys(password) # Your account password 

link = driver.find_element("xpath", '//*[@id="modal_login_button"]')
link.click()

# Find all posts on piazza
post_elements = driver.find_elements(By.CLASS_NAME, "feed-item-wrapper")

# Prepare the CSV file and iterate throughout it 

# Create a CSV file to store the results
csv_filename = 'piazza_posts.csv'
with open(csv_filename, 'w', newline='') as csvfile:
    fieldnames = ['Post_title', 'Post_text', 'Instructor_response']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Write the CSV header
    writer.writeheader()
  
    # Click on each post element to navigate to the individual post pages
    for i, post_element in enumerate(post_elements): 
        post_element.click()


        try: 
            # Find the post title 
            response = True

            title = WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.CLASS_NAME, 'history-selection')))
            post_content = title.text
            
            # Find the instructor's reponse 
            try:
                i_response = WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-id='i_answer']")))
                i_response_text = i_response.text                
                writer.writerow({'Post_title': i, 'Post_text': post_content, 'Instructor_response': i_response_text})
            except:
                print("instructor response not found.")
                writer.writerow({'Post_title': i, 'Post_text': post_content, 'Instructor_response': "No response found"})


        except:
            print("could not find the question")

        # In the case where the post is at the reading list category
        try:
            time.sleep(0.5) 
            add_reading_button = driver.find_element(By.XPATH, '//*[@id="qanda-content"]/div[2]/button')
            if "I’ve read this" in add_reading_button.text:
                # Click on the button

                # Wait for the modal dialog to disappear
                WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.CLASS_NAME, "modal")))
                add_reading_button.click()
            else:
                print("Button does not have the expected text.")
            

        except:
            print("button not found")
            continue 


