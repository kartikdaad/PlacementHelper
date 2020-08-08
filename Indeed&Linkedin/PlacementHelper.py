import time
import re
import random
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from ipywidgets import widgets
from selenium.webdriver.common.keys import Keys

#Connecting Driver
driver = webdriver.Firefox()
driver.implicitly_wait(15)
driver.maximize_window()


# Basic Functions
def scrollPageDown():
    for scrollStep in range(0, 8):
        driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
        time.sleep(1)

def scrollPageUp():
    for scrollStep in range(0, 8):
        driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_UP)
        time.sleep(random.randint(2, 5))



#URL and Xpaths
companyDetailurl = "https://www.indeed.co.in/Top-Rated-Workplaces/2019-IN-Technology"
indeedUrl = "https://www.indeed.co.in"

#function to get comapny List
Links = []
Names = []
Ranks = []

def GettingCompanyList():
    driver.get(companyDetailurl)
    time.sleep(15)
    driver.execute_script("window.scrollTo(0,1000);")
    companypage = BeautifulSoup(driver.page_source , "lxml")

    for i in companypage.find_all('div', {'class': "cmp-company-tile clearfix cmp-company-featured-tile cmp-card"}):
        h4 = i.find('h4')
        companyName = h4.text
        Names.append(companyName)
        for j in i.find_all('div', {'class': "cmp-company-tile-content"}):
            temp = int(0)
            for k in j.find_all('span', {'class': 'hidden'}):
                if temp != 0:
                    Ranks.append(k.text)
                else:
                    temp = 1
        for j in i.find_all('div', {'class': "cmp-company-tile-logo"}):
            a = j.find_all('a')[-1]
            company_link = indeedUrl+a['href']
            Links.append(company_link)



#Fetching compnay details
CompanyDetailsList = []

def GettingCompanyDetailsList():
    for i in allCompanyLinksDf['Link']:
        search = i
        driver.get(search)
        time.sleep(5)
        companyDetails = BeautifulSoup(driver.page_source, "lxml")

        infoList = []
        data = []
        name = [companyDetails.find('span', {'class': 'cmp-CompactHeaderCompanyName'}).getText()]
        infoList.extend(name)

        counter = int(0)
        for div in companyDetails.find_all('div', {'class': 'cmp-AboutMetadata-itemInner'}):
            counter = counter+1
            for j in div.find_all('div', {'class': 'cmp-AboutMetadata-itemCotent'}):
                if counter < 5:
                    data.append(j.text)

        infoList.extend(data[0:5])

        website = []
        for j in companyDetails.find_all('a', {'class': 'cmp-CompanyLink'}):
            website.append(j['href'])

        print(website)
        infoList.extend(website[0:1])

        aa = []
        for exp in companyDetails.find_all('div', {'class': 'cmp-ReviewAndRatingsStory'}):
            for per in exp.find_all('td', {'class': 'cmp-RatingCategory-rating'}):
                aa.append(per.text)
        infoList.extend(aa)

        interviewExp = companyDetails.find('div', {'class': 'cmp-ExperienceCard-result'}).getText()
        infoList.append(interviewExp)


        interviewDifficulty = companyDetails.find('div', {'class': 'cmp-DifficultyCard-result'}).getText()
        infoList.append(interviewDifficulty)


        interviewTime = companyDetails.find('div', {'class': 'cmp-DurationCard-text'}).getText()
        infoList.append(interviewTime)

        CompanyDetailsList.append(infoList)

#Function to save Data obtained
def saveFile(nameOfFile, data):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    #fileName=nameOfFile+str(current_time)+".csv"
    fileName = "C:/Users/Lenovo/Desktop/" + nameOfFile + ".csv"
    data.to_csv(fileName, index=True)


GettingCompanyList()
companyLinksDf = pd.DataFrame(columns=['Company Name', 'Rating', 'Link'])
allCompanyLinksDf = pd.DataFrame({'Company Name': Names, 'Rating': Ranks, 'Link': Links})
allCompanyLinksDf = allCompanyLinksDf.head(int(15))
allCompanyLinksDf = allCompanyLinksDf[allCompanyLinksDf['Link'] != "NA"]
allCompanyLinksDf.index = range(len(allCompanyLinksDf.index))

#saving all the data
saveFile("CompanyList", allCompanyLinksDf)

#display(allCompanyLinksDf)

GettingCompanyDetailsList()
companyInfoDf = pd.DataFrame(CompanyDetailsList,columns=['CompanyName', 'Headquarters', 'Employees', 'Industry', 'Revenue', 'Website',  'Work/LifeRating', 'SalaryRating', 'JobSecurityRating', 'Managementrating', 'CultureRating', 'InterViewExperience', 'InterviewDifficulty', 'InterViewProcessTime'])
saveFile("CompanyDetailsDemo1", companyInfoDf)


##  --------------------------LinkedIn------------------------------##

#Details for profile search on Linkedin
menu1 = widgets.Dropdown(
    options=companyInfoDf['CompanyName'],
    value=companyInfoDf['CompanyName'][0],
    description='Company:')
menu2 = widgets.Dropdown(
    options=['Business Analyst', 'Software Developer', 'Data Engineer'],
    value='Business Analyst',
    description='Role:')
widgets.HBox([menu1, menu2])


# Urls and Constants
TotalProfile = 30
LinkedinUrl = 'https://www.linkedin.com'
LinkedinLoginUrl = "https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin"
LinkedinUsername = '//*[@id="username"]'
LinkedinPassword = '//*[@id="password"]'
LinkedinSignin = '//*[@class="btn__primary--large from__button--floating"]'
CurrentCompany = '//*[@id="ember2057"]'
CurrentCompanyChoice = '//*[@id="ember2057"]/input'
ApplyCompanyChoice = '//*[@id="ember181"]/span'
NextButton = '//*[@id="ember401"]/span'


#Login Credentials for Linkedin
username = "demo@gmail.com"
password = "*********"
'''We can take password as input from user using getpass() but for sake of simplicity it is not taken '''

# Login in Linkedin
driver.get(LinkedinLoginUrl)
time.sleep(3)
driver.find_element_by_xpath(LinkedinUsername).send_keys(username)
driver.find_element_by_xpath(LinkedinPassword).send_keys(password)
driver.find_element_by_class_name(LinkedinSignin)
time.sleep(5)

#Search for Profiles
search = "https://www.linkedin.com/search/results/people/?keywords=" +menu2.value + "&origin=FACETED_SEARCH"
driver.get(search)
time.sleep(3)

#Getting details of particular Company
driver.find_element_by_xpath(CurrentCompany).click()
time.sleep(1)
driver.find_element_by_xpath(CurrentCompanyChoice).send_keys(menu1.value)
time.sleep(2)
driver.find_element_by_xpath(ApplyCompanyChoice).click()
time.sleep(3)
page_url = driver.current_url
time.sleep(2)


# Getting Particular details of employees of those companies
driver.get(page_url)
page_url = ''
profileLinksDf = pd.DataFrame(colunms=['ProfileId', 'Employee Name', 'Company', 'Job Title', 'Location', 'Link'])

while True:
    # Getting values of first 5 pages
    earlier_url = page_url
    page_url = driver.current_url
    if page_url == earlier_url or page_url.find('page=5') !=-1:
        break
    scrollPageDown()

    profileList = BeautifulSoup(driver.page_source,'lxml')

    profile_Names = profileList.find_all('span', class_="name actor-name")
    name = list(map(lambda x: x.text,profile_Names))

    profile_Links = profileList.find_all('a', class_="search-result__result-link ember-view")
    links = list(map(lambda x: LinkedinUrl + x['href'], profile_Links))[::2]

    profile_ID = list(map(lambda x:x['href'][4:-1], profile_Links))[::2]

    profile_Locations = profileList.find_all('p', class_="subline-level-2 t-12 t-black--light t-normal search-result__truncate")
    locations = list(map(lambda x:x.text.replace('\n', ''), profile_Locations))

    profile_Title = profileList.find_all('p', class_="subline-level-1 t-14 t-black t-normal search-result__truncate")
    titles = list(map(lambda x:x.text.replace('\n', ''), profile_Title))

    sixprofileLinksDf = pd.DataFrame({'ProfileId': profile_ID, 'Employee Name':name, 'Company': menu1.value, 'Job Title':titles, 'Location':locations, 'Link':links})

    profileLinksDf = profileLinksDf.append(sixprofileLinksDf, ignore_index=True)
    profileLinksDf = profileLinksDf[profileLinksDf['Employee Name'] != 'Linkedin Member']

    if profileLinksDf.shape[0] >= int(TotalProfile):
        break

    driver.find_element_by_class_name(NextButton).click()
    time.sleep(5)


#Removing extra character from Job Title
for i in range(0,len(profileLinksDf['Job Title'])):
    completetitle = profileLinksDf['Job Title'][i].split()
    if 'at' in completetitle:
        profileLinksDf['Job Title'][i] = ' '.join([str(i) for i in completetitle[0:completetitle.index('at')]])
    if '@' in completetitle:
        profileLinksDf['Job Title'][i] = ' '.join([str(i) for i in completetitle[0:completetitle.index('@')]])


saveFile("ProfileList", profileLinksDf)

# Functions to fetch data of employees

def fetchExperience(page):
    fetchExperienceDf = pd.DataFrame(columns=['Profile_Id', 'Company', 'Title', 'Date', 'Duration', 'Location'])
    fetchExperienceSection = page.find('section', id="experience-section").find('ul',class_="pv-profile-section__section-info section-info pv-profile-section__section-info--has-no-more").find_all('li', class_="pv-entity__position-group-pager pv-profile-section__list-item ember-view")

    for i  in range(0,len(fetchExperienceSection)):
        title = fetchExperienceSection[i].find('h3')
        company = fetchExperienceSection[i].find('p', class_="pv-entity__secondary-title t-14 t-black t-normal")
        datee = fetchExperienceSection[i].find('h4', class_="pv-entity__date-range t-14 t-black--light t-normal")
        duration = fetchExperienceSection[i].find('span', class_="pv-entity__bullet-item-v2")
        location = fetchExperienceSection[i].find('h4', class_="pv-entity__location t-14 t-black--light t-normal block")

        if title is not None:
            expTitle = title.text.strip().split('\n')[-1]
        else:
            expTitle = "NA"

        if company is not None:
            expCompany = company.text.strip().split('\n')[0]
        else:
            expCompany = "NA"

        if datee is not None:
            expDate = datee.text.strip().split('\n')[-1]
        else:
            expDate = "NA"

        if duration is not None:
            expDuration = duration.text.strip().split('\n')[-1]
        else:
            expDuration = "NA"

        if location is not None:
            expLocation = location.text.strip().split('\n')[-1]
        else:
            expLocation = "NA"

        fetchExperienceDf = fetchExperienceDf.append(pd.DataFrame(
            {'Profile_Id': profile, 'Company': expCompany, 'Title': expTitle, 'Date': expDate,
             'Duration': expDuration, 'Location': expLocation}, index=[i]))
        print("Exit Fetch Experience  :", profile)
        if len(fetchExperienceDf) != 0:
            return fetchExperienceDf
        else:
            raise SystemError


def fetchEducation(page):
    fetchEducationDF = pd.DataFrame(columns=['Profile_Id', 'Course', 'Degree', 'Date', 'University'])
    fetchEducationSection = page.find('section', id="education-section").find('ul', class_="pv-profile-section__section-info section-info pv-profile-section__section-info--has-no-more").find_all('li', class_="pv-profile-section__list-item pv-education-entity pv-profile-section__card-item ember-view")

    for i in range(0,len(fetchEducationSection)):
        degree = fetchEducationSection[i].find('p', class_="pv-entity__secondary-title pv-entity__degree-name t-14 t-black t-normal")
        dateED = fetchEducationSection[i].find('p', class_="pv-entity__dates t-14 t-black--light t-normal")
        universityName = fetchEducationSection[i].find('h3', class_="pv-entity__school-name t-16 t-black t-bold")
        courses = fetchEducationSection[i].find('div', class_="pv-entity__degree-info")

        if degree is not None:
            edDegree = degree.text.strip().split('\n')[-1]
        else:
            edDegree = "NA"

        if dateED is not None:
            edDate = dateED.text.strip().split('\n')[-1]
        else:
            edDate = "NA"

        if universityName is not None:
            edUniname = universityName.text.strip().split('\n')[-1]
        else:
            edUniname = "NA"

        if courses is not None:
            edCourse = courses.text.strip().split('\n')[-1]
        else:
            edCourse = "NA"

        fetchEducationDF = fetchEducationDF.append(pd.DataFrame(
            {'Profile_Id': profile, 'Course': edCourse, 'Degree': edDegree, 'Date': edDate,
             'University': edUniname}, index=[i]))
        if len(fetchEducationSection) != 0:
            return fetchEducationSection
        else:
            return SystemError


def fetchSkills(page):
    skills = page.find_all('span', class_="pv-skill-category-entity__name-text")
    skillList = list(map(lambda  x: x.text.strip(), skills))[0:len(skills)]
    fetchSkillsDF = pd.DataFrame({'Profile_Id': profile, 'Skill': skillList})
    if len(fetchSkillsDF) != 0:
        return fetchSkillsDF
    else:
        return SystemError

# Getting Data of employees from the links of their profile

Experience_DF = pd.DataFrame(columns=['Profile_Id', 'Company', 'Title', 'Date', 'Duration', 'Location'])
Education_DF = pd.DataFrame(columns=['Profile_Id', 'Course', 'Degree', 'Date', 'University'])
Skills_DF = pd.DataFrame(columns=['Profile_Id', 'Skill'])

index = 0
profile = ""


while True:
    #Base Condition
    if index == len(profileLinksDf):
        break

    profile = profileLinksDf['ProfileId'][index]
    profilesearch = profileLinksDf['Link'][index]
    time.sleep(3)
    driver.get(profilesearch)
    time.sleep(3)
    scrollPageDown()

    page = BeautifulSoup(driver.page_source, 'lxml')
    Experience_DF = Experience_DF.append(fetchExperience(page), ignore_index=True)
    Education_DF = Education_DF.append(fetchEducation(page), ignore_index=True)
    Skills_DF = Skills_DF.append(fetchSkills(page), ignore_index=True)
    index = index + 1

saveFile("ExpDetails", Experience_DF)
saveFile("EduDetails", Education_DF)
saveFile("SkiDetails", Skills_DF)

# We Have all the details we need to visualize the above data

# PreProcessing of Data
prev_exp = {}
def fetch_degree(edu):
    degree_list = []
    for key, group_df in edu.groupby('Profile_Id'):
        prev_exp[key] = list(group_df['Degree'])
        for i in range(0, len(list(group_df['Degree']))):
            if ('Master' in list(group_df['Degree'])[i]) or ('Bachelor' in list(group_df['Degree'])[i]) or (
                    'Certificate' in list(group_df['Degree'])[i]):
                degree_list.append(list(group_df['Degree'])[i])

    filtered_list = list(set(degree_list))
    return filtered_list

#Loading Education data
edu = pd.read_csv("C:/Users/Lenovo/Desktop/EduDetails.csv")
#Converting Values in true or false to check NA
edu = edu[edu['Degree'].notna()]
options = fetch_degree(edu)
edu = edu[edu['Degree'].isin(options)]

#Loading Experience section
exp = pd.read_csv("C:/Users/Lenovo/Desktop/ExpDetails.csv")

# Load skills section
skill = pd.read_csv("C:/Users/Lenovo/Desktop/SkiDetails.csv")

# Load profile section
profile = pd.read_csv("C:/Users/Lenovo/Desktop/ProfileList.csv")

# Section to get previous company
prev_company = {}
new_dict = {}

for key, group_df in exp.groupby('Profile_Id'):
    prev_company[key] = list(group_df['Company'])

for key, value in prev_company.items():
    if (len(value) > 1):
        new_dict[key] = value[1]
    else:
        new_dict[key] = 'NA'

df = pd.DataFrame(
    [{"ProfileId": name, "Previous Company": value} for (name), value in new_dict.items()])


# section to calculate previous experience
prev_exp = {}
prev_exp_dict = {}
for key, group_df in exp.groupby('Profile_Id'):
    prev_exp[key] = list(group_df['Duration'])

for key, value in prev_exp.items():
    for j in prev_exp.items():
        years = []
        months = []
        duration = []
        for i in range(1, len(value)):

            if 'yr' in value[i]:
                years.append(re.findall(r"(\d+) yr", value[i]))

            if 'mos' in value[i] or 'mo' in value[i]:
                months.append(re.findall(r"(\d+) mo", value[i]))

            elif 'less than a year' in value[i]:
                months.append('6')
        years = [item for sublist in years for item in sublist]
        years = [int(i) for i in years]

        duration = [item for sublist in months for item in sublist]
        duration = [int(i) for i in duration]
        break

    prev_exp_dict[key] = sum(years) * 12 + sum(duration)

df_comp = pd.DataFrame(
    [{"ProfileId": name, "Previous Experience (in months)": value} for (name), value in prev_exp_dict.items()])

new_df = pd.merge(df, df_comp, on='ProfileId')



def format_rows(old, new):
    if new in old:
        return old.replace(old, new)


# Last Degree
highest_edu = {}
for key, group_df in edu.groupby('Profile_Id'):
    if 'Master' in list(group_df['Degree'])[0].partition(' ')[0]:
        highest_edu[key] = format_rows(list(group_df['Degree'])[0].partition(' ')[0], 'Master')
    elif 'Bachelor' in list(group_df['Degree'])[0].partition(' ')[0]:
        highest_edu[key] = format_rows(list(group_df['Degree'])[0].partition(' ')[0], 'Bachelor')
    else:
        highest_edu[key] = list(group_df['Degree'])[0].partition(' ')[0]

df_edu = pd.DataFrame(
    [{"ProfileId": name, "Last Degree": value} for (name), value in highest_edu.items()])

new_df = pd.merge(new_df, df_edu, on='ProfileId')


# Skills section
skills = {}
for key, group_df in skill.groupby('Profile_Id'):
    skills[key] = list(group_df['Skill'])

df_skill = pd.DataFrame(
    [{"ProfileId": name, "Top skills": value} for (name), value in skills.items()])

new_df = pd.merge(new_df, df_skill, on='ProfileId')


# FINAL DATATSET
mergedFinalDataset = pd.merge(profile, new_df, on='ProfileId')
saveFile("FinalDataset", mergedFinalDataset)