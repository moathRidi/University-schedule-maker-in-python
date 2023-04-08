import colorama
from colorama import Fore
class Course:
    def __init__(self, code, year, semester):
        self.code = code
        self.year = year
        self.semester = semester
        self.prereqs = []
        self.status = False
        if len(self.code) > 6:
            self.creditHours = int(self.code[5])
        else:
            self.creditHours = 0
        self.unlocks = 0  # how manycourses does this course unlock ?
    def printCourseInfo(self):
        print("Course Code : ", self.code, 'Status is ', self.status, ' Year : ', self.year, ' Semester :',
              self.semester, ' This Course Unlocks', self.unlocks, " And Pre Reqs Are ", end="")
        for i in range(len(self.prereqs)):
            print(", " + self.prereqs[i].code, end="")
        print("")
    def preReqsMet(self):
        for i in self.prereqs:
            if i.status == False:
                return False
        return True








class Semester:
    def __init__(self, year, semester):
        self.year = year
        self.semester = semester
        self.courses = []
        if self.semester == 1 or self.semester == 2:
            self.maxCredit = 18
        else:
            self.maxCredit = 9
        self.status = False
        self.assigned = []

    def printSemesterInfo(self):
        if len(self.courses) != 0:
            print(Fore.WHITE, self.year, self.semester, end="")
            for i in self.courses:
                if i.status == True:
                    print(Fore.GREEN, i.code, end=" ")
                else:
                    print(Fore.WHITE, i.code, end=" ")
        print(" ")

    def currCredit(self):
        sum = 0
        for i in self.assigned:
            sum += i.creditHours
        return sum

