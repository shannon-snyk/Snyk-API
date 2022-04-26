#!/usr/bin/env python3 
#importing requests module
import requests as requests
import json 
#hiding api key token with get pass module because i want to be cool ;)
import getpass
#importing prettyprint to make results when calling look nice and pretty :)
from pprint import pprint as pp 

#static snyk api url
url = 'https://snyk.io/api/v1/'

SNYK_API_KEY = getpass.getpass('Enter Your Snyk API Token: ')
SNYK_ORG_ID = getpass.getpass("Enter Your Snyk Organization ID: ")
SNYK_PROJ_ID = getpass.getpass("Enter Your Project ID: ")
print("\n")
#headers
headers = {
    'Content-Type': 'application/json; charset=utf-8',
    'Authorization': SNYK_API_KEY
}


depGraphResponse = requests.get(url + "org/" + SNYK_ORG_ID + "/project/" + SNYK_PROJ_ID + "/dep-graph", headers=headers)

licenses_response = requests.post(url + "org/" + SNYK_ORG_ID + "/licenses", headers=headers)

print("Dependency Graph Response Code = ", depGraphResponse.status_code)
print("Licenses Response Code = ", licenses_response.status_code)
print("\n")
depArray = depGraphResponse.json()
licensesDict = licenses_response.json()

#creating a list of the dependencies where the word 'nodeId is found' after going to the correct location where the direct dependencies are located
depList = [d['nodeId'] for d in depArray['depGraph']['graph']['nodes'][0]['deps']]

#setting up licensesArray that contains dependency name and its licenses
licensesArray = []

#getting licenses + dependencies
licensesList = licensesDict['results']
def licensesCall():
    for licensesData in licensesList:
        licenses = licensesData['id']
        dependenciesList = licensesData['dependencies']
        for dependencies in dependenciesList:
            dependency_name = dependencies['id']
            data = {
                'dependency name': dependency_name,
                'license': licenses
            }
            licensesArray.append(data)
licensesCall()

#setting up direct dependencies array
directDependencies = []

#matching the dependencies from depList to licensesArray to get direct dependency names + its licenses
for d in licensesArray:
     if any(x in d['dependency name'] for x in depList):
         directDependencies.append(d)
        
pp(directDependencies)

#outputing results to .json file
with open('directDependencies.json', 'w') as xyz:
    json.dump(directDependencies, xyz, indent = 3)
print("\n")
print('\033[1;35m The direct dependencies and their licenses have also been saved in the "directDependencies.json" file \n')