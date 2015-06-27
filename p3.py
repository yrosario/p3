# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 23:00:08 2015

@author: end
"""

from os import listdir
import sys
import json
#import pandas as pd
import re
import pdb
 

def main():
    dataFolder = "data"
    frequencyFile = "top250.txt"
    clusterFile = "top250clustered250.csv"
    
    #Get list of json file names
    fileList = getFiles(dataFolder)
    
     #Read all JSON files.
    #Create a list of instances; note that the same instance may be listed in more than one file;
    #all instances on your list must be unique by instance ID.
    instancesLst = getInstances(fileList[0:6])
    
    #Create a list of all persons; the persons are entities of type "Person"; note that the same
    #person may be listed in more than one file; all persons on your list must be unique by 
    #entity ID.
    #print(fileList[4:5])
    personsLst = getPersons(fileList[4:6])
    print(type(personsLst[:6]))
    
    personCount = getCount(instancesLst, personsLst)
    #Count the number of persons by year. Result should be a table of N rows and M columns.
    #N is the number of persons and M is the years
    #Maybe it should return an array with?
    #personCount = getCount(instancesLst, personsLst)
    
    #Normalize each column by dividing each number by the sum of all numbers in the column 
    #to calculate the frequencies of mentioning.
    #Arrange the rows in the decreasing order by the sum of all frequencies in a row. The 
    #top 250 rows are the top 250 most frequently mentioned persons.
    #Each row in the table is a vector of six numbers. The length of the vector is the square
    #root of the sum of the squares of the numbers. Normalize each vector by dividing each number
    #by the vector length. Alternatively, use function sklearn.preprosessing.normalize() from the
    #module sklearn.preprocessing.
    normalizeData = normalize(personCount)
    
    #Save this list in the
    #file top250.txt, one name per line. You will need only these rows for the rest of the
    #analysis.
    saveToFile(normalizeData,frequencyFile)
    
    #Do k-means clustering of the 250 vectors, using the class sklearn.cluster.KMeans: create 
    #an instance of the class and use method .cluster(). The method partitions the vectors into a number of clusters, based on their similarity. In other words, if the frequencies of mentioning of two persons were correlated (were changing together over the six years), the persons will be likely assigned to the same cluster.
    #The default number of clusters is 8. However, a rule of thumb suggests that the number of 
    #clusters shall be M~sqrt(N), where N is the number of vectors. Choosing the right number of 
    #clusters is a matter of trial-and-error: if you end up having some very small clusters, 
    #try gradually decreasing M.
    clusters = createCluster(normalizeData)
    
    
    #Save the list of persons in clusters in the CSV file top250clustered.csv. 
    #The file shall have three columns: the cluster ID (1 through M), the name of the person, 
    #and the total frequency of mentioning (used for sorting in item 7). The rows shall be 
    #ordered by the cluster ID and then by the persons' names.
    saveToFile(clusters,clusterFile, fileType = "csv")
    
 
    

    
 
#Get list of json file names   
def getFiles(folderPath):
    try:
        return listdir(folderPath)
    except:
        print("unable to locate file")
        sys.exit()
        
#Read all JSON files.
#Create a list of instances; note that the same instance may be listed in more than one file;
#all instances on your list must be unique by instance ID.    
def getInstances(fileList):
    listIt = []
    instanceIds = []
    
    for file in fileList:
        try:
           path = "data/" + file
           with open(path) as infile:
               data = json.load(infile)
               content = data["instances"]
               listIt.append(content)
           
        except IOError as io:
            print("Unable open file " + io)
            infile.close()
            sys.exit()
        except:
            print("Unable to open file instances")
            infile.close()
            sys.exit()
            
    return listIt
    
#Create a list of all persons; the persons are entities of type "Person"; note that the same
#person may be listed in more than one file; all persons on your list must be unique by 
#entity ID.    
def getPersons(fileList):
    listIt= []
    personIds = []
    for file in fileList:
        try:
            path = "data/" + file
            with open(path) as infile:
                data = json.load(infile)
            
            for key in data["entities"]:
                if data["entities"][key]["type"] == "Person" and key not in personIds:
                     personIds.append(key)
                     #print(personIds)
                     listIt.append(data["entities"][key]["name"])
                     #print(listIt)
            
        except:
            print("Unable to open file person")
            sys.exit()
            
    return listIt

#Count the number of persons by year. Result should be a table of N rows and M columns.
#N is the number of persons and M is the years
#Maybe it should return an array with?
def getCount(lstOfInstances, lstOfPersons):
    print("Place holder")
    perFreq = {}
    #print(lstOfInstances)
    date = ""
    for ins in lstOfInstances:
        if(len(ins)):
            content = ins.pop()
            date = content["document"]["published"][:4]
            k = ins.pop()
            for key in k.keys():
               #print(key)
               for person in lstOfPersons:
                   #perFreq["year"] = date
                   #perFreq["number of Persons"] = person
                   if type(k[key]) is dict:
                       for key2 in k[key].keys():
                          #print(type(k[key][key2]))
                          if type(k[key][key2]) is dict:
                              for key3 in k[key][key2]:
                                  #print(type(k[key][key2][key3]))
                                  if type(k[key][key2][key3]) is str:
                                      try:
                                          if re.match(person, k[key][key2][key3], re.I):
                                              perFreq["year"] = date
                                              perFreq["number of Persons"] = 1
                                      except:
                                          continue
                          elif type(k[key][key2]) is str:
                              try:
                                  if re.match(person, k[key][key2], re.I):
                                      perFreq["year"] = date
                                      perFreq["number of Persons"] = perFreq["number of Persons"] + 1
                              except:
                                     continue
                   elif type(k[key]) is str and type(person) is str and len(k[key]):
                       
                       #pdb.set_trace()
                       #print(k[key])
                       try:
                           if re.match(person, k[key], re.I):
                               perFreq["year"] = date
                               perFreq["number of Persons"] = 1
                       except:
                           continue
                   
                   
    print(perFreq)     
    return date


#Normalize each column by dividing each number by the sum of all numbers in the column 
#to calculate the frequencies of mentioning.
#Arrange the rows in the decreasing order by the sum of all frequencies in a row. The 
#top 250 rows are the top 250 most frequently mentioned persons.
#Each row in the table is a vector of six numbers. The length of the vector is the square
#root of the sum of the squares of the numbers. Normalize each vector by dividing each number
#by the vector length. Alternatively, use function sklearn.preprosessing.normalize() from the
#module sklearn.preprocessing.
def normalize(personCount):
    print("Place holder")
    return -1

#Save this list in the
#file top250.txt, one name per line. You will need only these rows for the rest of the
#analysis.    
def saveToFile(personCount, filename, fileType = "txt"):
    print("Place holder")
 
#Do k-means clustering of the 250 vectors, using the class sklearn.cluster.KMeans: create 
#an instance of the class and use method .cluster(). The method partitions the vectors into a number of clusters, based on their similarity. In other words, if the frequencies of mentioning of two persons were correlated (were changing together over the six years), the persons will be likely assigned to the same cluster.
#The default number of clusters is 8. However, a rule of thumb suggests that the number of 
#clusters shall be M~sqrt(N), where N is the number of vectors. Choosing the right number of 
#clusters is a matter of trial-and-error: if you end up having some very small clusters, 
#try gradually decreasing M.   
def createCluster(personCount):
    print("Place holder")
    return -1

        
if __name__ == "__main__":
    main()
    
    
