
Andmebaaside päringu mikroteenus restserv
======================================================================

Tegu on pythonis kodeeritud REST mikroteenusega, mis kasutab Flaski
ja andmebaasimootorina sqlite3

1) Nõuded
----------------------------------------------------------------------
python 3.5
sqlite3

Programmi restserv installeerimiseks peab olema eelnevalt installeeritud
python3.5 ja sqlite3.

Sqlite3 andmebaasi kasutame kuna see on kõige lihtsam moodust test
baaside loomiseks.

2) Programmi installeerimine
----------------------------------------------------------------------
Valida kataloog ning avada sinna lahti restserv.tgz programmi-pakett

$ ls
api  chinook2.db  chinook.db  README.txt

Failid chinook.db ja chinook2.db on kaks andmebaasi, mis lähtuvalt ülesandest
on

3) Virtuaalkeskonna install
----------------------------------------------------------------------
Järgnevalt tuleb installeerida pythoni virtuaalkeskond
olles eelnevalt lahtipakitud programmi kataloogis(punkt2.)
installeerida Pythoni virtuaalkekond

python3.5 -m venv .

$ ls
api  bin  chinook2.db  chinook.db  include  lib  lib64  pyvenv.cfg  README.txt  share

Virtuaalkeskonna käivitamine
Kui virtuaalkeskonna teegid on installeeritud tuleb virtuaalkeskond käivitada

selleks käivitada järgnev käsurida
source bin/activate

Kui virtuaalkeskond on edukalt käivitunud tekib iseloomulik käsurea viip:
(restserv)kasutaja2masin:..restserv$


Järgnevalt installeerimie tööks vajalikud pythoni tarkvarateegid antud
virtuaalkeskonna tarbeks

pip install flask
pip install flask-restful
pip install sqlalchemy
pip install configparser
pip install requests
pip install pytest


4) Esmane käivitamine
----------------------------------------------------------------------
Liikuda kataloogi api

Käivitada server:
python api.py

Avada teine terminalaken ja teha serveri vastu päring

curl -iX GET  'http://localhost:5000/api/employee/1'
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 522
Server: Werkzeug/0.12.2 Python/3.5.2
Date: Sun, 30 Jul 2017 12:01:44 GMT

[
    {
        "Phone": "+1 (780) 428-9482",
        "Fax": "+1 (780) 428-3457",
        "Address": "11120 Jasper Ave NW",
        "LastName": "Adams",
        "HireDate": "2002-08-14 00:00:00",
        "State": "AB",
        "Country": "Canada",
        "City": "Edmonton",
        "ReportsTo": null,
        "EmployeeId": 1,
        "Email": "andrew@chinookcorp.com",
        "PostalCode": "T5K 2N1",
        "BirthDate": "1962-02-18 00:00:00",
        "Title": "General Manager",
        "FirstName": "Andrew"
    }
]

Logid on jälgitavad server.log failist
(Juhul kui seda pole konfiguratsioonifailis config.ini muudetud)



5) Testjuhtude käivitamine
----------------------------------------------------------------------
Lihtsamate testjuhtude pakett on failis test_api.py
Testjuhtude käivitamiseks
    1.jätta server tööle pordis 5000 (Nagu on vaikimisi config.ini failis)
    2. Avada uus terminalaken ja virtuaalkeskkond
    3. käsurealt sisestada:
     $ pytest

========================================== test session starts ==========================================
platform linux -- Python 3.5.2, pytest-3.1.3, py-1.4.34, pluggy-0.4.0
rootdir: ../restserv/api, inifile:
collected 6 items

test_serv.py ......

======================================= 6 passed in 0.17 seconds ========================================

Kõik kuus testi on edukalt läbitud

6) REST päringud

Andmebaasist päring. Praegusel juhul saab teha päringuid vaid andmebaasist Employee tabelist ID järgi

 Päringuks on sobilik kasutada curl programmi

 curl -iX GET  'http://localhost:5000/api/employee/1'

 /api/employee on päring mis kasutab parameetriks integer väärtust id leidmiseks.



Andmebaasi sisestamine

curl -iX POST 'http://localhost:5000/api/employee/' -H "Content-Type: application/json" -d
'{"LastName":"Gulliver", "FirstName":"Lemuel", "BirthDate": "1661-11-12","Email":"pole@olla.co.uk"}'

sisestamiseks Employees tabelisse on antud restserv teenuse puhul vajalik et oleks täidetud
järgmiste väljad andmetega
LastName,FirstName,BirthDate ja Email

Kui sama kirje esineb mõlemas baasis, siis väljastab programm sellest ühe kirje
(olles eelnevalt sisuliselt andmeid kontrollinud)

Kui üks andmebaasidest pole kättesaadav kuvatakse teise andmebaasi tulemus kuid
vastus on HTTP_206_PARTIAL_CONTENT , mitte 200 OK

Kui andmeid ei leita ilmub teade HTTP_404_NOT_FOUND








