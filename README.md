# Engage2021
![image](https://user-images.githubusercontent.com/42894689/143294926-d131ca53-2128-4065-9fc4-00c02666fe08.png)

Project Repository for Microsoft Engage 2021. 

#### Name: AYUSH JAIN
#### College Name: THAPAR INSTITUTE OF ENGINEERING AND TECHNOLOGY
### Project Title: SCHEDULER

#### Link to Live Project: https://scheduler-enagage.herokuapp.com/

#### Demo Video Link: 

#### Problem Statement
To build a scheduler responsive and easy tp use web-app to allow students to submit daily preferences for attending classes in-person or remotely. The app then must assign available seats to the students and send a mail to both the teacher and the students. For teachers, the mail must contain the details of all the students going to attend the next day's classes and for the students, the mail contains all the classes for which he/she is selected for physical classes.  

Admin login credentials: username: admin and password: adminpass

#### Sample Time Table File: https://docs.google.com/spreadsheets/d/1iCEjRUBiHYviVf6SVbG1R3Nqo-MmM6YE/edit?usp=sharing&ouid=113169055127155980102&rtpof=true&sd=true
## Tech Stack Used
1. Flask (Backend) 
<p align="center">
  <img src="https://user-images.githubusercontent.com/42894689/133317407-dc868f47-fbcb-4799-be73-b25313e65b0d.png">
</p>

2. Python (Backend)
<p align="center">
  <img src="https://user-images.githubusercontent.com/42894689/143119648-0ab28a41-89f1-4f43-afcb-2e993d95c028.png">
</p>

3. HTML (Frontend)
<p align="center">
  <img src="https://user-images.githubusercontent.com/42894689/133317464-d798e31b-8622-46be-909c-a264e34b7d31.png">
</p>

4. CSS (Frontend)
<p align="center">
  <img src="https://user-images.githubusercontent.com/42894689/133317498-05875c94-9f66-47c4-b2d3-bc5a09d1361b.png">
</p>

5. JavaScript (Frontend)
<p align="center">
  <img src="https://user-images.githubusercontent.com/42894689/143118611-b9263fb6-8879-4ed6-a44c-f123383e292f.png">
</p>

6. Heroku (Hosting website)
<p align="center">
  <img src="https://user-images.githubusercontent.com/42894689/133317602-42753fcb-f12e-45b5-8983-715964902754.png">
</p>

## Flowchart Diagram
![Microsoft-Engage-2021 (1)](https://user-images.githubusercontent.com/42894689/143114663-8e53f3c9-0b80-40dc-b1a6-a80ab230c0e1.jpg)


## Databases Schemas
<p align="center">
  <img src="https://user-images.githubusercontent.com/42894689/143095720-83eebac9-9687-43bb-904d-dd40704a8751.png">
</p>
<p align="center">
  <img src="https://user-images.githubusercontent.com/42894689/143095760-4f90d601-5ee5-4d7b-a3c0-0937069ff5b9.png">
</p>
<p align="center">
  <img src="https://user-images.githubusercontent.com/42894689/143095781-f984a943-d324-4574-ac92-f4ec94310178.png">
</p>
<p align="center">
  <img src="https://user-images.githubusercontent.com/42894689/143095790-0a1d242a-e87c-4709-ae8a-e9b642ceead7.png">
</p>

## Directory structure

<p align="center">
  <img src="https://user-images.githubusercontent.com/42894689/143381955-c849b10f-3025-48c4-9ccc-b209d7854dfc.png">
</p>
1. Scheduler folder: This is our main app directory.<br/>
2.  mails directory: All the mails that are to be sent out are temporarily stored here.<br/>
3.  static directory: The styling files are stored here.<br/>
4.  templates directory: All the html webpages are stored here.<br/>
5.  uploads directory: Used to store the uploaded time-table by the admin.<br/>
6.  app.py file: The main app which contains all the routing procedures.<br/>
7.  config.py file: This file contains all the configurational information: threshold for studentSelection algorithm and the mail sending time.<br/>
8.  covidCertification.py: This file fetches the vaccination status from the mock database.<br/>
9.  credentials.py: Contains the email account details for the google account that sends the email.<br/>
10.  excelToJSON.py: This file converts the uploaded time table in JSON format for easy storage.<br/>
11.  selectionAlgo.py: This file returns list of students and teacher with all the details. The list will be used to send the emails.<br/>
12.  bulletinboard.db: Database for bulletin board.<br/>
13.  filled.db: Database to store who all have filled the preference form.<br/>
14.  physicalClasses.db: Database that stores student and class details for students who have marked their wish for physical class.<br/>
15.  user.db: Database for user details.<br/>
16.  CoWin.db: Mock database that will return vaccine status, given the beneficiary-id.<br/>
17.  TimeTable.json: The converted time-table database from the uploaded excel sheet.<br/>
18.  logs.log: Log file containing all the debugging information and website status codes. 
19. venv directory: Virtual environment for this python project. <br/>
20. requirements.py: Contains information for all the libraries used in the project.<br/>
21. runtime.txt: Specifies the python version used for the project.<br/>
22. Procfile: mechanism for declaring what commands are run by your application's dynos on the Heroku platform<br/>

## Features List

1.	Student Login<br/>
  a.	Student can sign in on the website using login credentials (username and password).<br/>
  b.	Student will be redirected dashboard which will show the following day’s class schedule along with student preference recording form and covid verification feature (discussed later).
2.	Student Signup<br/>
  a.	A new student entry can be added by the signup feature. Email-id, username and roll-number are unique so can not be used by 2 students at the same time.<br/>
  b.	Student must provide username, email-ID, password, branch, group number, degree, year. After successful submission of these details, student can sign-in to see his/her dashboard.
3.	Admin Login<br/>
  a.	Administrator can login to perform various CRUD operations on the four tables (User, PhysicalClasses, Filled and BulletinBoard whose schemas will be shown below).<br/>
  b.	Administrator can upload a new/updated time-table that will act as database (converted from excel to JSON script) for fetching class schedule for students.<br/>
  c.	Administrator can add new notices to showcase them on top of the bulletin board on the landing page of the website.
4.	Vaccine Verification<br/>
  a.	Note: The Government CoWin API was not available for public use to get the vaccination status of a person using beneficiary ID. It was available only to some organizations. Thus, I created my own mock database to mimic API call for the vaccination status.<br/>
  b.	The student who just created a new account or whose vaccination status is not yet updated can go here and provide his/her beneficiary ID from the covid certificate. The mock database will return one of four outcomes: Fully vaccinated, partially vaccinated, not vaccinated or ID not found.<br/>
  c.	The User database gets updated according to the response received.
5.	Preference Recording:<br/>
  a.	As stated above, the students are shown the following days schedule. They are given a form with class details and they must choose one of two options: Offline or Online. If a student doesn’t pick an option, it will be treated as online class.<br/>
  b.	If a student has filled his/her preference, the dashboard will show the message that they have already filled the preferences and the details of the classes on the next day. All the “Offline” preferences are stored in the PhysicalClasses database and the details of the students who have filled the details are stored in Filled database.
6.	Student Selection Algorithm:<br/>
  a.	The students from each group (for example COE1, BT2, etc.) are selected with threshold% (set by admin, by default 50) capacity each.<br/>
  b.	The selection priority is done according to vaccination status and timestamp. <br/>
  c.	A list is generated containing a list of students selected for physical classes for the next day.<br/>
  d.	A list of students and class details is generated for each teacher.
7.	Mailing concerned people about physical classes:<br/>
  a.	Mailing each teacher, the list of students and class details.<br/>
  b.	Mailing each student, the list of subjects for which they are selected for physical classes.<br/>
  c.	Mailing is done at a time set by admin in the config.py file. When the mailing is being done, the preference form is closed for all the students.
8.	Bulletin Board:<br/>
  a.	The admin can add new notices by adding the topic and the link (e.g. Google Drive link) in the Bulletin Board database. The latest notice will be shown at the top of the bulletin board.<br/>
  b.	The board is auto scrolling that showcases all the notices.

## UI Screenshots and Examples

### Home Screen (Laptop and phone)
<p align="center">
  <img src="https://user-images.githubusercontent.com/42894689/143127172-cdc92150-0c68-41c2-a32b-fa1ea5ad3edb.png">
</p>
<p align="center">
  <img src="https://user-images.githubusercontent.com/42894689/143127505-e69ce3c0-1b7f-4a49-9b71-d264230de177.png">
</p>
<p align="center">
  <img src="https://user-images.githubusercontent.com/42894689/143127973-f4e8f187-dc6b-47f2-b2a5-c320e7d0bbc7.png">
</p>

### Login Screen (Laptop and phone)
<p align="center">
  <img src="https://user-images.githubusercontent.com/42894689/143124859-829961c1-78bc-40c0-b89d-4fdecceca37c.png">
</p>
<p align="center">
  <img src="https://user-images.githubusercontent.com/42894689/143125185-2bdaa6f2-ceb2-48e8-be11-9e527726ec00.png">
</p>

### Signup Screen (Laptop and phone)
<p align="center">
  <img src="https://user-images.githubusercontent.com/42894689/143126133-a866c85f-a21f-4ed7-9781-2708db051c29.png">
</p>
<p align="center">
  <img src="https://user-images.githubusercontent.com/42894689/143126397-ca9c9952-9215-4ce3-b557-d15cdb537e7b.png">
</p>

### Admin page (Laptop and phone)
<p align="center">
  <img src="https://user-images.githubusercontent.com/42894689/143129336-aadc7ea9-4820-4ce3-9719-61f5655dc2a3.png">
</p>
<p align="center">
  <img src="https://user-images.githubusercontent.com/42894689/143129613-cd125dcf-01da-419c-8294-897296caa25e.png">
</p>
<p align="center">
  <img src="https://user-images.githubusercontent.com/42894689/143129881-8dca2773-2116-4cc6-b0b5-6fbe7deeb38f.png">
</p>
<p align="center">
  <img src="https://user-images.githubusercontent.com/42894689/143129928-018635fe-42b6-4972-994a-9da9babafea3.png">
</p>

### Time Table Upload Screen (Laptop and Phone)
<p align="center">
  <img src="https://user-images.githubusercontent.com/42894689/143130048-3dcde0fd-4392-4192-bb4f-4815841945f8.png">
</p>
<p align="center">
  <img src="https://user-images.githubusercontent.com/42894689/143130102-d852c412-795c-4754-b5db-f21338a4170a.png">
</p>

### Dashboard if there are classes and preferences not filled (Laptop and Phone)
<p align="center">
  <img src="https://user-images.githubusercontent.com/42894689/143185667-88af02ea-1ba7-4b6b-96a3-e5549ba7fa02.png">
</p>
<p align="center">
  <img src="https://user-images.githubusercontent.com/42894689/143185739-9f53718d-617f-4355-be23-0a8984052c4b.png">
</p>

### Dashboard if there are classes and preferences are filled (Laptop and Phone)
<p align="center">
  <img src="https://user-images.githubusercontent.com/42894689/143185871-443b4f23-9f44-406a-a099-35a4fdc2d107.png">
</p>
<p align="center">
  <img src="https://user-images.githubusercontent.com/42894689/143185930-4251b19c-f80a-4fe0-9ec4-178650ceed19.png">
</p>

### Dashboard if there are no classes (Laptop and Phone)
<p align="center">
  <img src="https://user-images.githubusercontent.com/42894689/143130307-f7bfd56e-5dd6-4dc5-8e9e-c86bf6a5762b.png">
</p>
<p align="center">
  <img src="https://user-images.githubusercontent.com/42894689/143130363-642e49f0-bfed-4b94-aed8-0f9d6c7d3fa9.png">
</p>

### Covid Verification Page (Laptop and Phone)
<p align="center">
  <img src="https://user-images.githubusercontent.com/42894689/143130473-36742114-1507-429d-864d-19d3efdf94c5.png">
</p>
<p align="center">
  <img src="https://user-images.githubusercontent.com/42894689/143130616-789daf15-e277-4008-bdca-83d48c8fe40e.png">
</p>

### Error pages (Laptop and phone)
<p align="center">
  <img src="https://user-images.githubusercontent.com/42894689/143130941-38a7e5ad-32d8-402a-91f5-2fa66cdf8e17.png">
</p>
<p align="center">
  <img src="https://user-images.githubusercontent.com/42894689/143131033-b2fe51f8-cba5-455f-a508-1609393461be.png">
</p>

### Alerts are displayed for different scenarios. One example shown (Laptop and Phone)
<p align="center">
  <img src="https://user-images.githubusercontent.com/42894689/143184409-db73eadf-c886-4cef-b97e-e6e9ad804a06.png">
</p>
<p align="center">
  <img src="https://user-images.githubusercontent.com/42894689/143184448-0ec84cff-0533-479f-bef7-1478a63162b9.png">
</p>

### Mails sent to the teachers
<p align="center">
  <img src="https://user-images.githubusercontent.com/42894689/143131346-e3dfe498-8c70-499a-9266-811ccfeef032.png">
</p>
<p align="center">
  <img src="https://user-images.githubusercontent.com/42894689/143131441-6049d155-f6da-415e-8360-d2f9608aabd8.png">
</p>

### Mails sent to the students
<p align="center">
  <img src="https://user-images.githubusercontent.com/42894689/143131543-af8030b3-74b3-4038-afb2-d3f57ee5d2a5.png">
</p>
<p align="center">
  <img src="https://user-images.githubusercontent.com/42894689/143131609-0cad0a18-ecd4-4aa4-bd68-f51f9568b051.png">
</p>

### Log file
![image](https://user-images.githubusercontent.com/42894689/143301583-7c1ea93c-562c-43e1-ad98-cb56aec6b0e0.png)


## Some important points to keep in mind

1. Time Table format<br/>
  a. The first column must contain the 10 timeslots for each day (8AM-5PM)
  b. All subsequent columns are for the batches (branch and subgroups, for example COE1, BT1, CE1, etc.)
  c. Each cell of the time table must have the format: Teacher-email[space]Subject-Name[space]Subject Code
  d. Each sheet contains groups of a particular combination of degree and year. For example, in sample time-table, the first sheet is for undergraduate 3rd year (ug_3).
2. The filled and physicalclasses databases are cleared after sending out the mails to repective teachers and students.
3. Admin login credentials: username: admin and password: adminpass
