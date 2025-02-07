from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests

url = 'https://catalog.unc.edu/courses/'
data = requests.get(url)
html = data.text
soup = BeautifulSoup(html, 'html.parser')
dictionary_for_Raad = {} 

def main():
    print("running")
    megaclass = []
    program_classes = []
    megaprereq = []
    links = soup.select('a[href^="/courses/"]')
    links = links[3:153] #153

    for link in links:
        #accesses class catalogs for each program
        subUrl = link.attrs['href']
        subObj = BeautifulSoup(urlopen("https://catalog.unc.edu" + subUrl), 'html.parser')

        program_classes = getClasses(subObj)
        for course in program_classes:
            megaclass.append(course)

        prereqs = getPrereq(subObj)
        for prereq in prereqs:
            megaprereq.append(prereq)
            if(prereq == [""]):
                index = megaprereq.index(prereq)
                megaprereq.remove(megaprereq[index])
                megaclass.remove(megaclass[index])

    multiassign(dictionary_for_Raad, megaclass, megaprereq)
    print(dictionary_for_Raad)

    
def multiassign(d, keys, values):
    dictionary_for_Raad.update(zip(keys, values))

def getLink(subObj):
    link_list = []
    clickOn = subObj.find_all("div", {'class':'cols no indent'})

    link = soup.select()
    link_list.append(link)
    return link_list

# def getAbbr(program):
#     abbr = program[len(program) - 5:len(program) -1]
#     return abbr

def getClasses(subObj):
    class_list = []
    classes = subObj.find_all('div',{'class':'cols noindent'})
    for course in classes:
        course = course.get_text()
        #course = course.replace("\xa0", "")
        course = course[:8]
        if(course != "" and course != " "):
            if (course[len(course) - 1] == "."):
                course = course[:7]
            class_list.append(course)

    return (class_list)

#def getPrereq(subObj):

def getPrereq(subObj):
    prereq_list_big = []
    total_courses = (subObj.find_all("div", {'class': 'courseblock'}))
    for course in total_courses:
        prereq_list = []
        if ("text detail-requisites margin--default" in str(course)):
            url2 = course.find_all('a', {'class': 'bubblelink code'})
            for url in url2:
                url = url.get("href")
                if(str(url) != ""):
                    source = "https://catalog.unc.edu" + str(url)
                    #print("src: " + source)
                    dataClicky = requests.get(source)
                #prereq page accessed
                    htmlClicky = dataClicky.text
                    clickySoup = BeautifulSoup(htmlClicky, 'html.parser')
                    prereq = "".join(getClasses(clickySoup))
                    prereq_list.append(prereq)
        else: 
            prereq = ""
            prereq_list.append(prereq)
        
        prereq_list_big.append(prereq_list)
    return prereq_list_big

if __name__ == "__main__":
    main()