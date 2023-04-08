import json
from random import randint
from LinuxClasses import *

cb1 = open('CourseBrowser_1.json')  # load jason files -> Dicts
cb1Data = json.load(cb1)
cb2 = open('CourseBrowser_2.json')
cb2Data = json.load(cb2)
cb3 = open('CourseBrowser_3.json')
cb3Data = json.load(cb3)

semesters = {  # create a semester dict -> each key has a value of a Semester Object
    "1,1": Semester(1, 1),
    "1,2": Semester(1, 2),
    "1,3": Semester(1, 3),
    "2,1": Semester(2, 1),
    "2,2": Semester(2, 2),
    "2,3": Semester(2, 3),
    "3,1": Semester(3, 1),
    "3,2": Semester(3, 2),
    "3,3": Semester(3, 3),
    "4,1": Semester(4, 1),
    "4,2": Semester(4, 2),
    "4,3": Semester(4, 3),
    "5,1": Semester(5, 1),
    "5,2": Semester(5, 2),
    "5,3": Semester(5, 3),
    "6,1": Semester(6, 1),
    "6,2": Semester(6, 2),
    "6,3": Semester(6, 3),
    "7,1": Semester(7, 1),
}

courses = {}  # Dict for courses
fread = open("CEStudyPlan.txt", "r").read().split("\n")
flag=0
for i in range(len(fread)):  # Read courses from file & create Objects
    c = fread[i].split(",")
    if len(c) < 2:
        continue
    if(flag==1):
      courses[c[2]] = Course(c[2], c[0], c[1])
      key = str(c[0]) + "," + str(c[1])
      semesters[key].courses.append(courses[c[2]])
    flag=1
e = open("Electives.txt", "r").read().split("\n")  # electives file
flag=0
for i in range(len(e)):
    el = e[i].split(",")
    if(flag==1):
      courses[el[1]] = Course(el[1], 0, 0)  # add electives to courses Dict -> Treat as normal course
    flag=1
for i in range(len(
        e)):  # iterate over all courses again & add its' pre requisites as objects in its' preReqs list. [for elective courses]
    el = e[i].split(",")
    pre = el[2:]
    for j in range(1,len(pre)):
        courses[pre[j]].unlocks += 1
        courses[el[1]].prereqs.append(courses[pre[j]])

for i in range(len(fread)):  # same process for normal courses
    c = fread[i].split(",")
    pre = c[3:]
    for j in range(1,len(pre)):
        if pre[j] not in courses.keys(): courses[pre[j]] = Course(pre[j], 0, 0); courses[pre[j]].status = True
        courses[pre[j]].unlocks += 1
        courses[c[2]].prereqs.append(courses[pre[j]])

for i in semesters.keys():  # Print [][]
    semesters[i].printSemesterInfo()


def collision(D1: dict,
              D2: dict):  # function that determines whether 2 Dicts (course sectiosn from  jason file) collide i.e. that cannot both be registered together
    cond = True
    for i in D1.keys():
        if len(i) != 1:
            continue
        for j in D2.keys():
            if j != i:
                continue
            # if it gets here -> its a match in days
            # condition 1 : D1  after D2 -> check if D1 larger than D2
            condition1 = True if (int(D2[j].split(" - ")[1].split(":")[0]) < int(
                D1[i].split(" - ")[0].split(":")[0])) or ((int(D2[j].split(" - ")[1].split(":")[0]) == int(
                D1[i].split(" - ")[0].split(":")[0])) and (int(D2[j].split(" - ")[1].split(":")[1]) < int(
                D1[i].split(" - ")[0].split(":")[1]))) else False
            #

            # condition 2 : D2  after D1 -> check if D2 larger than D1
            condition2 = True if (int(D2[j].split(" - ")[0].split(":")[0]) > int(
                D1[i].split(" - ")[1].split(":")[0])) or ((int(D2[j].split(" - ")[0].split(":")[0]) == int(
                D1[i].split(" - ")[1].split(":")[0])) and (int(D2[j].split(" - ")[0].split(":")[1]) > int(
                D1[i].split(" - ")[1].split(":")[1]))) else False
            #
            finalCondition = condition1 or condition2
            cond = cond and finalCondition

    return not (cond)


def countDays(solution,
              Data):  # counts days in a solution (list of sections) which are keys in the Data [Jason file Data]
    days = []
    for i in solution:
        for j in Data[i].keys():
            if len(j) == 1 and j not in days:
                days.append(j)
    return len(days)


def allSemsDone():  # checks if all semesters are done i.e. all have been iterated over & assigned courses
    for i in semesters.keys():
        if semesters[i].status == False: return False
    return True


def testSolution(sol1,
                 Data):  # tests an entire solution for its' validity -> if no course collides with another course -> Return true.
    for k in range(len(sol1)):
        for z in range(len(sol1)):
            if k != z and collision(Data[sol1[z]], Data[sol1[k]]):
                return False
    return True


def findData(currSem):  # Return the proper json file data (Dict) based on the Current Semester.
    if currSem.split(",")[1] == '1':
        return cb1Data
    elif currSem.split(",")[1] == '2':
        return cb2Data
    elif currSem.split(",")[1] == '3':
        return cb3Data


def totalCredit(Desired):  # Desired is a list of course objects -> Return the sum of  all credit hours
    sum = 0
    for i in Desired:
        sum += i.creditHours
    return sum

 # prints information about a given semester key [from the dict (semesters)] &&& discriminate passed courses from assigned.
def printSemester(currSem):
    for i in semesters.keys():
        if i == currSem:
            print(Fore.MAGENTA, semesters[i].year, semesters[i].semester, semesters[i].maxCredit, end=" ")
            for j in semesters[i].assigned:
                print(Fore.RED, j.code, end="  ")

        else:
            print(Fore.WHITE, semesters[i].year, semesters[i].semester, semesters[i].maxCredit, end=" ")
            for j in semesters[i].assigned:
                if j.status == True:
                    print(Fore.GREEN, j.code, end="  ")
                else:
                    print(Fore.WHITE, j.code, end="  ")
        print(" ")


exit = False
while exit == False:  # enter main loop (start of  actual algorithm here)
    filename = input("Enter the name of the file : ")
    filelocation = input("Enter the location of the file: ")
    record = filelocation + "/" + filename
    sRecord = None
    while True:
        try:
            sRecord = open(record, "r").read().split("\n")
            break
        except:
            record = input('file name does not exist , please enter new file name\n')  # read file until valid name
            continue

    for i in range(len(sRecord)):  # read record file, check every course, if its' grade > 60 -> status = True
        rec = sRecord[i].split(",")
        c = rec[2:]
        for j in range(len(c)):
            if int(c[j].split(":")[1]) > 60:
                courses[c[j].split(":")[0]].status = True
                key = str(rec[0]) + "," + str(rec[1])
                semesters[key].assigned.append(courses[c[j].split(":")[0]])
        semesters[key].status = True  # semester status = True -> wil not make a schedule for it

    for i in semesters.keys():
        semesters[i].printSemesterInfo()

    numOfDays = 5 - int(input('Enter the number of free days\n'))

    maxFirstSem = int(input('Enter The Maximum Number of Credit Hours in First Semester\n'))
    if maxFirstSem > 18:
        maxFirstSem = 18
    maxSecondSem = int(input('Enter The Maximum Number of Credit Hours in Second Semester\n'))
    if maxSecondSem > 18:
        maxSecondSem = 18
    maxThirdSem = int(input('Enter The Maximum Number of Credit Hours in Summer Semester\n'))
    if maxThirdSem > 9:
        maxThirdSem = 9
    numOfSems = int(input('Enter Number Of Semesters for scheduling\n'))  # read prefrences

    for i in semesters.keys():  # set max credit hours per semester as desired by the student
        if i.split(",")[1] == '1':
            semesters[i].maxCredit = maxFirstSem
        elif i.split(",")[1] == '2':
            semesters[i].maxCredit = maxSecondSem
        else:
            semesters[i].maxCredit = maxThirdSem

    finalSolution = {}  # dict where we will append our schedule for every semester
    while allSemsDone() == False:  # loop for all semesters
### Wanted -> List of courses that have not been completed from previous semesters & courses that belong to current semester
        Wanted = []
        currSem = None
        for i in semesters.keys():
            if semesters[i].status == True:
                for j in semesters[i].courses:
                    if j.status == False:
                        Wanted.append(j)
            if semesters[i].status == False:
                currSem = i
                Wanted.extend(semesters[currSem].courses)
                break

        print(Fore.MAGENTA + "\n\nCURRENTLY SCHEDULING SEMESTER ", currSem, "\n\n")
        print(Fore.WHITE + '')

        Data = findData(currSem)  # find proper data based off current semester -> Data = Dict
        Wanted.sort(key=lambda x: x.unlocks, reverse=True)  # sort by unlocks -> number of courses each course unlocks
        # start cleaning wanted and move into Desired
        Desired = []
        # Desired -> list
        for i in Wanted:
            if len(i.code) < 4:
                Desired.append(i)
            elif 'xx' in i.code:
                for k in Data.keys():
                    if k.split("-")[0] not in courses.keys() and k.split("-")[0] != 'Discussion' and (
                            'ENCS' in k.split("-")[0]):
                        courses[k.split("-")[0]] = Course(k.split("-")[0], 0, 0)
                    if i.code[0:6] in k and courses[k.split("-")[0]].status == False and courses[
                        k.split("-")[0]] not in Desired:
                        if courses[k.split("-")[0]].preReqsMet() == False: continue
                        if totalCredit(Desired) + courses[k.split("-")[0]].creditHours <= semesters[currSem].maxCredit:
                            Desired.append(courses[k.split("-")[0]])
                        break
            elif i.preReqsMet():
                for j in Data.keys():
                    if i.code == j.split("-")[0]:
                        if i not in Desired and totalCredit(Desired) + i.creditHours <= semesters[currSem].maxCredit:
                            Desired.append(i)
                        break
        # DESIRED -> Courses we want to take & they're avaiable this semester -> available in json file (Data)

        available = []  # available is a list which contains every single section for every single course in DESIRED
        for i in Desired:
            miniList = []
            if 'COMP' not in i.code:
                for j in Data.keys():
                    if j != "Discussion-Discussion" and i.code == j.split("-")[0]:
                        miniList.append(j)
                if len(miniList) != 0: available.append(miniList)
            else:
                Lab = []
                Lect = []
                for j in Data.keys():
                    if j != "Discussion-Discussion" and i.code == j.split("-")[0] and j.split("-")[1] == 'Lab':
                        Lab.append(j)
                    elif j != "Discussion-Discussion" and i.code == j.split("-")[0]:
                        Lect.append(j)
                if len(Lab) != 0: available.append(Lab)
                available.append(Lect)

        bestSolution = []  # solution
        for j in available:
            bestSolution.append(j[randint(0, len(j) - 1)])  # give initial solution
        for i in range(10000):  # try 10k solutions at random -> 99.9% guaarenteed solution in 10,000 iterations
            index = []
            for j in available:
                index.append(j[randint(0, len(j) - 1)])  # get random solution
            if testSolution(bestSolution, Data) == False and testSolution(index, Data) == True: bestSolution = index
            if testSolution(index, Data) and countDays(bestSolution, Data) >= countDays(index, Data):
                bestSolution = index  # if its best that current best solution -> replace
            if countDays(bestSolution, Data) <= numOfDays: break  # if we meet prefrences -> break

        for i in bestSolution:
            print(i, Data[i])  # print sol

        if countDays(bestSolution, Data) > numOfDays:  # if prefrences not met -> let user know
            print(Fore.CYAN, "Sorry ! we could not achieve the desired number of days , as we only achieved : ",
                  countDays(bestSolution, Data), 'Desired #  = ', numOfDays)

        for i in Desired:
            i.status = True  # set courses status to True -> assume it will be passed
            semesters[currSem].assigned.append(i)
        semesters[currSem].status = True
        if len(semesters[currSem].assigned) != 0:  # print sem info
            printSemester(currSem)
            finalSolution[currSem] = bestSolution

        numOfSems -= 1
        if numOfSems == 0: break

    decision = input(
        'Would you Like to save the information on a file? \n')  # offer to save data to file (after while loop)

    if decision == 'Yes':
        fwrite = open("SuggestedCourses.txt", "w")
        for i in finalSolution.keys():
            fwrite.write(i + str(finalSolution[i]) + '\n')
            exit = True
    else:
        x = input("okay, would you like to continue or exit?\n")
        if x == 'exit':
            exit = True
        else:
            for i in semesters.keys():
                semesters[i].assigned = []
                semesters[i].status = False
            for c in courses.keys():
                courses[c].status = False
            exit = False