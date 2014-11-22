'''
Created on Nov 14, 2014

@author: taolu
'''
import csv
import sys
import math
import operator

#read users.tsv
readfile_users = open("users.tsv",'r')
userfile_users = csv.reader(readfile_users, delimiter = '\t', quotechar = '|')
users = {}
for row in userfile_users:
    item = row[0]
    if users.get(item) == None:
        users[item] = {}
    (users[item])["City"] = row[1];
    (users[item])["State"] = row[2];
    (users[item])["DegreeType"] = row[5];
    (users[item])["Major"] = row[6];
    (users[item])["TotalYearExperience"] = row[9];
    (users[item])["RecentJob"] = None

#read users_history.tsv, add the most recently job to users' attribute
readfile_history = open("user_history.tsv",'r')
userfile_history = csv.reader(readfile_history,delimiter = '\t', quotechar = '/')
history = {}
index = 0
for row in userfile_history:
    #if index > 4:
        #break
    #index += 1
    item = row[0]
    if history.get(item) == None:
        history[item] = {}
        (history[item])["JobTitle"] = row[2]
        (users[item])["RecentJob"] = row[2]

#test, print users
#print "users info", users
#print "\n"
#print"userfile", history    
    
# find knn for user2
def getUserNeighbors(userSet,testUser,k):
    distances = []
    testrow = users.get(testUser)
    #print testrow
    for row in userSet:
        #print row
        #print row[0]
        if row != testUser:
            similarity = 0;
            #print userSet[row]
            #print testrow
            #for x in range(1,6):
                #if (userSet[row]) == testrow[x]:
            if (userSet[row])["City"] != testrow["City"]:
                similarity += 1
            if (userSet[row])["Major"] != testrow["Major"]:
                similarity += 1
            if (userSet[row])["DegreeType"] != testrow["DegreeType"]:
                similarity += 1
            if (userSet[row])["State"] != testrow["State"]:
                similarity += 1
            #print (userSet[row])["RecentJob"]
            if (userSet[row])["RecentJob"] != None and testrow["RecentJob"] != None and (userSet[row])["RecentJob"] != testrow["RecentJob"]:
                similarity += 1
            #print "1", (userSet[row])["TotalYearExperience"]
            #print "2",testrow["TotalYearExperience"]
            #if (userSet[row])["TotalYearExperience"] != ' ' and testrow["TotalYearExperience"] != ' ' and math.fabs(int((userSet[row])["TotalYearExperience"]) - int(testrow["TotalYearExperience"])) > 2:
            if (userSet[row])["TotalYearExperience"] != testrow["TotalYearExperience"]:
                similarity += 1
            #print "similarity", similarity
            distances.append((row,math.sqrt(similarity)))
    distances.sort(key = operator.itemgetter(1))
    #print "distance", distances
    neighbors = []
    for x in range(k):
        neighbors.append(distances[x][0])
    return neighbors
print  "getUserNeighbors", getUserNeighbors(users,'679942',10)

#read job file
readfile_job = open("jobs.tsv",'r')
jobsfile = csv.reader(readfile_job,delimiter = '\t', quotechar = '/')
jobs = {}
for row in jobsfile:
    item = row[0]
    if jobs.get(item) == None:
        jobs[item] = {}
    (jobs[item])["JobTitle"] = row[1]
    (jobs[item])["City"] = row[4]
    (jobs[item])["State"] = row[5]
    (jobs[item])["EndDate"] = row[6]

#print "Jobs", jobs
#find knn for job
def getJobNeighbors(userSet,testUser,k):
    distances = []
    testrow = users.get(testUser)
    for row in userSet:
        if row[0] != testrow[0]:
            similarity = 0;
            for x in range(1,4):
                if row[x] == testrow[x]:
                    similarity += 1
            distances.append(row[0],math.sqrt(similarity))
    distances.sort(key = operator.itemgetter(1))
    neighbors = []
    for x in range(k):
        neighbors.append(distances[x][0])
    return neighbors

#read application file
readfile_apps = open("apps.tsv",'r')
userfile_apps = csv.reader(readfile_apps, delimiter = '\t', quotechar = '|')
apps = {}
for row in userfile_apps:
    item = row[0]
    if apps.get(item) == None:
        apps[item] = {}
        (apps[item])["JobID"] = []
    (apps[item])["JobID"].append(row[2])
    
#index = 0
#for row in apps:
    #if index > 4:
       #break
    #index+=1
    #print "apps info", apps 
    #print"\n"

#read user2 file
readfile_user2 = open("user2.tsv",'r')
userfile_user2 = csv.reader(readfile_user2, delimiter = '\t', quotechar = '|')
user2 = {}
#applications = {}
predict = {}

index = 0
for row in userfile_user2:
    #if index > 4000:
        #break
    #index+=1
    #print "row",row
    #print row[0]
    applications = {}
    user_neighbors = getUserNeighbors(users,row[0],10)
    #print user_neighbors
    for neighbors_id in user_neighbors:
        #print neighbors_id
        if apps.get(neighbors_id) != None:
            #print "apps.get(neighbors_id)",apps.get(neighbors_id)
            #print "apps.get(neighbors_id)",(apps.get(neighbors_id))["JobID"]
            for item in (apps.get(neighbors_id))["JobID"]:
                #print item
                if applications.has_key(item):
                    applications[item] += 1
                else:
                    #print"aplication.get(item)", applications.get(item)
                    applications[item] = {}
                    applications[item] = 1
                #print"aplication.get(item)", item, applications.get(item)
    #print"application",applications
    #print"application count ", (applications[item])["count"]
    #sorted_x = sorted(x.items(), key=operator.itemgetter(1))
    sorted_app = sorted(applications.items(),key=operator.itemgetter(1),reverse = True)
    #print "sorted_app",sorted_app
    predict[row[0]] = sorted_app[0]
    #print "sorted_app[0]",predict[row[0]]
    #print "jobid",(predict[row[0]])[0]
    #print "count", (predict[row[0]])[1]
    #print "predict", predict

#print"application",applications
#print"application count ", (applications[item])["count"]

# find the top 150 predictions, write them in file
filename = "output.tsv"
f = open(filename,'w')

#sort prediction
sorted_prediction = sorted(predict.iteritems(),key=lambda kvt:kvt[1][1],reverse = True)
#print "sorted_prediction", sorted_prediction
#print "sorted_prediction[0]", sorted_prediction[0]
#print "(sorted_prediction[0])[0]", (sorted_prediction[0])[0]
#print "(sorted_prediction[0])[1]", (sorted_prediction[0])[1]
#print "((sorted_prediction[0])[1])[0]", ((sorted_prediction[0])[1])[0]
for x in range(0,150):
    f.write((sorted_prediction[x])[0] + '\t' + ((sorted_prediction[x])[1])[0] + '\n')
f.close()

        
        