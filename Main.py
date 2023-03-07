from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import re
import json
import random

wd = webdriver.Chrome(r'/Users/tingkangzhao/SeleniumDriver/chromedriver')
wd.implicitly_wait(10)

url = "https://amazon.jobs/en/search?offset=0&result_limit=10&sort=relevant&category%5B%5D=operations-it-support-engineering&category%5B%5D=software-development&category%5B%5D=hardware-development&category%5B%5D=business-merchant-development&category%5B%5D=machine-learning-science&category%5B%5D=project-program-product-management-technical&category%5B%5D=economics&category%5B%5D=research-science&category%5B%5D=systems-quality-security-engineering&category%5B%5D=business-intelligence&category%5B%5D=design&category%5B%5D=buying-planning-instock-management&category%5B%5D=data-science&category%5B%5D=supply-chain-transportation-management&category%5B%5D=audio-video-photography-production&category%5B%5D=database-administration&country%5B%5D=USA&distanceType=Mi&radius=24km&latitude=&longitude=&loc_group_id=&loc_query=&base_query=&city=&country=&region=&county=&query_options=&"
wd.get(url)

def getJobInfo():
    # find all job blocks on this page
    job_titles = wd.find_elements(By.CLASS_NAME, "job-tile")
    # initialization
    location_id_lst = []
    link_lst = []
    posted_lst = []
    qualification_lst = []
    title_lst = []
    # append job info into lists
    for job_title in job_titles:
        location_id_lst.append(job_title.find_element(By.CSS_SELECTOR, "p").text)
        link_lst.append(job_title.find_element(By.CSS_SELECTOR, '[href]').get_attribute('href'))
        posted_lst.append(job_title.find_element(By.CSS_SELECTOR, 'h2.posting-date').text)
        qualification_lst.append(job_title.find_element(By.CSS_SELECTOR, 'div.qualifications-preview').text)
        title_lst.append(job_title.find_element(By.CSS_SELECTOR, 'h3.job-title').text)
    # split location and job id
    location_lst = []
    id_lst = []
    for i in location_id_lst:
        temp = i.split('|')
        location_lst.append(temp[0])
        id_lst.append(temp[1])
    # converter
    jobs_dic = {}
    for i in range(len(id_lst)):
        job_dic = {}
        job_dic["jobID"] = id_lst[i][9:]
        job_dic["origin_search"] = None
        job_dic["posted"] = posted_lst[i]
        job_dic["jobTitle"] = title_lst[i]
        job_dic["companyName"] = "Amazon"
        job_dic["link"] = link_lst[i]
        location_dic = {}
        location_dic["remote"] = "not specified"
        try:
            location_dic["city"] = location_lst[i].split(', ')[2]
        except:
            location_dic["city"] = None
        try:
            location_dic["state"] = location_lst[i].split(', ')[1]
        except:
            location_dic["state"] = None
        try:
            location_dic["country"] = location_lst[i].split(', ')[0]
        except:
            location_dic["country"] = None
        job_dic["jobLocation"] = location_dic
        job_dic["educationRequirement"] = {"edication":None, "major":None}
        job_dic["jobType"] = None
        job_dic["visaSponsorship"] = None
        job_dic["salary"] = None
        job_dic["benefits"] = None
        job_dic["requirements"] = qualification_lst[i]
        job_dic["jobDescription"] = None
        jobs_dic[job_dic["jobID"]] = job_dic
    return jobs_dic

def nextPage():
    wd.find_element(By.CSS_SELECTOR, 'button.btn.circle.right').click()

def saveFile(file, index):
    with open(f'amazon{index}.json', 'w') as f:
    # convert the dictionary to JSON and write it to the file
        json.dump(file, f)

if __name__ == "__main__":
    # open the selenium driver
    wd = webdriver.Chrome(r'/Users/tingkangzhao/SeleniumDriver/chromedriver')
    wd.implicitly_wait(10)
    # feed url into the selenium driver
    url = "https://amazon.jobs/en/search?offset=0&result_limit=10&sort=relevant&category%5B%5D=operations-it-support-engineering&category%5B%5D=software-development&category%5B%5D=hardware-development&category%5B%5D=business-merchant-development&category%5B%5D=machine-learning-science&category%5B%5D=project-program-product-management-technical&category%5B%5D=economics&category%5B%5D=research-science&category%5B%5D=systems-quality-security-engineering&category%5B%5D=business-intelligence&category%5B%5D=design&category%5B%5D=buying-planning-instock-management&category%5B%5D=data-science&category%5B%5D=supply-chain-transportation-management&category%5B%5D=audio-video-photography-production&category%5B%5D=database-administration&country%5B%5D=USA&distanceType=Mi&radius=24km&latitude=&longitude=&loc_group_id=&loc_query=&base_query=&city=&country=&region=&county=&query_options=&"
    wd.get(url)

    # initialization
    dic_index = 0
    file_index = 0
    jobs_dic = {}

    # start scraping
    while True:
        jobs_dic.update(getJobInfo())
        time.sleep(random.uniform(5, 10))
        dic_index += 1

        if dic_index >= 29:
            saveFile(jobs_dic, file_index)
            file_index += 1

        try:
            nextPage()
        except:
            break

        
        
        
