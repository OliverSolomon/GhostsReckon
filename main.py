from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from glob import glob
from random import randint
from datetime import timedelta,date
from hashlib import sha256

from namesClean import clean

app = Flask(__name__)   
#database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)

#database structure
class Ghosts(db.Model):
    Id = db.Column(db.Integer, nullable = False, primary_key = True)
    fName = db.Column(db.String(20), nullable = False)
    sName = db.Column(db.String(20), nullable = False)
    email = db.Column(db.String(200), nullable = False)
    password = db.Column(db.String(64), nullable = False)
    dob = db.Column(db.String(20), nullable = False)

    def __repr__(self):
        return f"User(name = {self.fName + self.sName}, email = {self.email}, Birthday = {self.dob})"



def createDb():
    if glob("database.db"):
        pass
    else:
        db.create_all()

createDb()

if glob("names.txt"):
    print("found names.txt")
    # pass
else:
    clean()

@app.route("/")
def run():
    # combining names
    def namesComb():

        # names = []

        with open("names.txt", 'r') as f:
            list = f.readlines()

        f.close()

        #name presentation formarting
        count = 1
        for i in list:
            age = str(randint(19,99))
            fName = i.replace("\n", ' ')
            sName = list[-list.index(i)].replace("\n", ' ')
            name = fName + sName
            password = name.lower().replace(" ", '') + age + str(randint(int(age), 1000))
            passphrase = sha256((password).encode('utf-8')).hexdigest()#hashing passwords
            email = password #+ "@gmail.com"
            # names.append(password)
            # dob = date(2020,11,28) - timedelta(int(age)*365)
            dob = 2020 - int(age)

            details = name + " " + passphrase + " " + email + " " + str(dob)

            # print(details)

                 
            #adding data to db
            ghost = Ghosts(
                Id = count,
                fName = fName,
                sName = sName,
                email = email,
                password = passphrase,
                dob = dob
            )
            count +=1

            db.session.add(ghost)
            db.session.commit()
        
        return

    if Ghosts.query.all():
        pass
    else:
        namesComb()



    return "<h1> Accounts Generated and added to DB  Proceed to run formFiller and get your accounts generated</h1>"


if __name__ == "__main__":
    app.run(debug=True)