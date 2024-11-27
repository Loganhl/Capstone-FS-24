# Capstone-FS-24
This is a Capstone project for the University of Missouri - Information Technology Degree Program. This specific project is a biometric authentication software that is utilized as an additional layer of a cybersecurity framework. 
# Keycloak
in order to setup keycloak you will need to have docker installed.

```
cd BioVaultDevEnv
docker compose up
```
Once keycloak and the containers are finished initializing you can reach keycloak at http://localhost:8080
The default username and password  is  `admin`
## Setting up Your keycloak realm
go click on the realms dropdown form the control panel and select 'Create Realm'  a form should appear where you can name or your realm or browse for a realm config file. We will go to our project `CAPSTONE-FS-24/keycloak` folder and select `realm-export.json` then just click create at the bottom and your realm will be created. 
You will need to create at least one User  Account for your realm.

### importing the clients into your realm.
go to the clients tab in the keycloak admin console in the realm you created click import client

<img src="/Docs/client-import1.PNG"><img>
click browse and go to the keycloak folder in your cloned repo and select `backend.json` and then click save at the bottom. You should now have clients called `frontend` and `backend` as well as `biovault-client`.

# accessing the dashboard
When This project is ready the dashboard will hopefully be started when docker compose up is run but for now we are started it manually in their local folders.
## getting the backend api ready
To start the backend make sure you have completed the steps above steps correctly when it comes to creating your keycloak realm and importing the clients.
You will also need to create a `.env` file with the following values:
```
DB=biometric_auth
DB_USER=root
DB_PASS=secretsquirrels
DB_PORT=3307
DB_HOST=localhost
KEYCLOAK_CLIENT=backend
KEYCLOAK_CLIENT_SECRET=YOUR_CLIENT_SECRET_HERE
KEYCLOAK_URL=http://localhost:8080
KEYCLOAK_REALM=biovault
```
To Retrieve your client secret you will need to go to your keycloak administration console and select the backend client and go to the credentials tab and copy the client secret and add it to the `.env` file.
### start the backend
From the main repo folder run:
```
cd kcbackend
npm run i
npm run start
```
Now the api should be listening on http://localhost:2500

Next from the main repo folder run:
```
cd frontend
npm run i
npm run start
```
this should load load your Dashboard.
Enter the username and password for the account you created on your biovault realm.
<img src="/Docs/uicap.PNG"></img>

# Building the application
<p>In order to build the data collection application make sure you have the python requirements installed.
If you do not have them installed you can install them by running  ```pip install -r requirements.txt ```
in the root of the cloned repo. Next you will run </p>

```
cd BiovaultDataCollection
build
```  
<p>You will get some output from your terminal and your executable should be built.</p>

# URL FOR JIRA
https://umsystem-biovault-capstone.atlassian.net/jira/software/projects/KAN/boards/1?assignee=unassigned
