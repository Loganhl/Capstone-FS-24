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
Create a realm called biovault.
You will need to create at least one Account for your realm.

### importing the clients into your realm.
go to the clients tab in the keycloak admin console in the realm you created click import client

<img src="/Docs/client-import1.PNG"><img>
click browse and go to the keycloak folder in your cloned repo and select `frontend.json` and then click save at the bottom
Repeat this process with `biovault-client.json` and `backend.json`

# accessing the dashboard
When This project is ready the dashboard will hopefully be started when docker compose up is run but for now we are started it manually in their local folders.
To start the backend make sure you have completed the steps above steps correctly when it comes to creating your keycloak realm and importing the clients.

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
# Keystroke logger windows service
This service can be installed by running `python KsLog.py install` 
Currently this service is incomplete however the install command works as does the remove command. Next steps are to inegrate the keystroke logger functions we wrote with the service. To start the service you need to run `python kslog.py start` keep in mind that you have to run the install command first.
# URL FOR JIRA
https://umsystem-biovault-capstone.atlassian.net/jira/software/projects/KAN/boards/1?assignee=unassigned