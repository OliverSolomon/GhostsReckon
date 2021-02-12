"""
Script cleans names and prepares them ready for use

Second function acts as a test but is not imported and is actually implemented locally on main.py"""

from glob import glob
from random import randint
from datetime import timedelta,date

def clean():
    with open("originalNames.txt", 'r') as f:
        test = f.readlines()
    f.close()

    # print(test)
    with open('names.txt', "a") as new:

        for i in test:
            name = i.split()
            new.write(name[0] + "\n")
            print(name[0] + " 201")
        
        new.close()

if glob("names.txt"):
    pass
else:
    clean()


"""
# combining names
def namesComb():

    # names = []

    with open("names.txt", 'r') as f:
        list = f.readlines()

    f.close()

    #name presentation formarting
    for i in list:
        age = str(randint(19,99))
        fName = i
        sName = list[-list.index(i)] 
        nameRaw = fName + sName
        name = nameRaw.replace("\n", ' ')#its password because it has the characters
        email = name.lower().replace(" ", '') + age 
        password =  name.replace(" ", '') + age +"#@" #+ "@gmail.com"
        # names.append(password)
        # dob = date(2020,11,28) - timedelta(int(age)*365)
        dob = 2020 - int(age)

        details = name + " " + email+ " " + password + " " + str(dob)

        print(details)


# namesComb()

"""