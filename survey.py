# -*- coding: utf-8 -*-

#İTÜRO ANKET MANİPÜLE UYGULAMASI


#%%
import pandas as pd
import glob


path = r'...path...' # use your path
all_files = glob.glob(path + "\*.csv")

li = []

for filename in all_files:
    df2 = pd.read_csv(filename, index_col=None, header=0)
    li.append(df2)

df = pd.concat(li, axis=0, ignore_index=True)


#if the data is greater than expected, 64bit stored datas should be converted into 8bits
df.gsm = [str(each) for each in df.gsm]

df.fillna(df.mean(),inplace = True)
columns = [each for each in df.columns]

df.role = df.role.fillna('unknown')
df.purpose = df.purpose.fillna('unknown')

#%%
writer = pd.ExcelWriter('..path..\general_info.xlsx')
df.to_excel(writer,'ITURO22')
writer.save()
#%%

ages = [int(each) for each in df.age]

froms = [item for item in df.suggest]

def search4ages(src,search):
      i = 0
      new_list = []
      for item in src:
          if(item == search):
              new_list.append(ages[i])
              i+=1
          else:
              i+=1
              
      if(len(new_list) != 0):
          avg = sum(new_list)/len(new_list)
      else:
          avg = 0
          
      return new_list,avg

linkedin_ages,linkAvg = search4ages(froms, 'linkedin')
insta_ages,instAvg = search4ages(froms, 'insta')
twitter_ages,twitAvg = search4ages(froms, 'twitter')
youtube_ages,utubeAvg = search4ages(froms, 'youtube')
website_ages,wsiteAvg = search4ages(froms, 'website')
other_ages,otherAvg = search4ages(froms, 'other_suggest')            

avg_ages = sum(ages)/len(ages)


import matplotlib.pyplot as plt

plt.figure()
plt.title('AGE / SUGGEST CORRELATION')
plt.scatter(froms,ages, alpha = 1,marker ='x' , c = 'red', label = "suggest/age")
plt.axhline(y = avg_ages, color = 'blue', alpha=0.3, label ='general average', linestyle = '-')
plt.axhline(y = linkAvg, color = 'navy', alpha=0.3, label ='linkedin average', linestyle = '-')
plt.axhline(y = twitAvg, color = 'cornflowerblue', label ='twitter average', alpha=0.3, linestyle = '-')
plt.axhline(y = instAvg, color = 'pink', alpha=0.4, label ='instagram average', linestyle = '-')
plt.axhline(y = utubeAvg, color = 'red', alpha=0.3, label ='youtube average', linestyle = '-')
plt.axhline(y = wsiteAvg, color = 'orange', alpha=0.3, label ='website average', linestyle = '-')
plt.axhline(y = otherAvg, color = 'black', alpha=0.3, label ='other comers average', linestyle = '-')
plt.xlabel('Where participants came from')
plt.ylabel('Their ages')
plt.legend(loc = "best")
plt.show

#%%
#age / rating correlation

#SGE ==> respectively seminars, general , exhibition
rating_SGE = [[each for each in df.star_seminar],[each for each in df.star_general],[each for each in df.star_exh ]]
ratingSGE_avg = [] #rating averages of categories (overall points)
for i in range(len(rating_SGE)):
    ratingSGE_avg.append(sum(rating_SGE[i])/len(rating_SGE[i]))



plt.figure()
plt.title('RATING/AGE INSPECTON')
plt.scatter(ages,rating_SGE[0], alpha = 1 , color = 'red', label = "seminar/rating")
plt.scatter(ages,rating_SGE[1], alpha = 1 , color = 'blue', label = "general/rating")
plt.scatter(ages,rating_SGE[2], alpha = 1 , color = 'green', label = "exhibition/rating")
plt.axhline(y = ratingSGE_avg[0], color = 'red', alpha=0.3, label ='Seminar Avg Rating', linestyle = '-')
plt.axhline(y = ratingSGE_avg[1], color = 'blue', alpha=0.3, label ='General Avg Rating', linestyle = '-')
plt.axhline(y = ratingSGE_avg[2], color = 'green', label ='Exhibition Avg Rating', alpha=0.3, linestyle = '-')
plt.xlabel('Their ages')
plt.ylabel('Rates')
plt.legend(loc = "best")
plt.show




#%%
df.role = df.role.fillna('unknown')
df.purpose = df.purpose.fillna('unknown')
roles = [each for each in df.role]


def avgRating4roles(src,SGE,search4):
    keys = []
    values = []
    sum_role = 0
    i = 0
    avg_val = 0
    for item in src:
        if(item == search4):
            
            if(keys.count(item)==0):
                keys.append(item)
            
            sum_role = sum_role + rating_SGE[SGE][i]
            
        else:
            sum_role = sum_role + 0
        i+=1    
    i = 0
    if(sum_role != 0):
        avg_val = sum_role/src.count(search4)
        values.append(avg_val)
        sum_role = 0
        
    else:
        values.append(avg_val)
        sum_role = 0
        
    
    return [keys,values]
  
    
all_roles = ['ortaokul','lise','univ','calisan_ilgili','calisan_diger','isveren','merakli','diger_role','unknown']

#for seminar avg/role
seminar_avgRole = []
for each in all_roles:
    seminar_avgRole.append(avgRating4roles(roles, 0, each))
        
#for general avg/role
general_avgRole = []
for each in all_roles:
    general_avgRole.append(avgRating4roles(roles, 1, each))
    
#for exh. avg/role
exh_avgRole = []
for each in all_roles:
    exh_avgRole.append(avgRating4roles(roles, 2, each))
    
    


plt.figure()
plt.title('ROLE/RATING INSPECTON')
plt.scatter(roles,rating_SGE[0], alpha = 0.2 , color = 'red', label = "seminar/rating")
plt.scatter(roles,rating_SGE[1], alpha = 0.2 , color = 'blue', label = "general/rating")
plt.scatter(roles,rating_SGE[2], alpha = 0.2 , color = 'green', label = "exhibition/rating")
plt.axhline(y = ratingSGE_avg[0], color = 'red', alpha=0.3, label ='Seminar Avg Rating', linestyle = '-')
plt.axhline(y = ratingSGE_avg[1], color = 'blue', alpha=0.3, label ='General Avg Rating', linestyle = '-')
plt.axhline(y = ratingSGE_avg[2], color = 'green', label ='Exhibition Avg Rating', alpha=0.3, linestyle = '-')
plt.xlabel('Their Roles')
plt.ylabel('Their rates')
plt.legend(loc = "best")
plt.show

#%%

plt.figure()

plt.subplot(2, 3, 1)

for i in range(len(general_avgRole)):
    plt.title('general rating')
    plt.bar(general_avgRole[i][0],general_avgRole[i][1],width=0.2)
    plt.ylabel('average ratings')
plt.subplot(2, 3, 3)

for i in range(len(seminar_avgRole)):
    plt.title('Seminar rating')
    plt.bar(seminar_avgRole[i][0],seminar_avgRole[i][1],width=0.2)
    plt.ylabel('average ratings')
plt.subplot(2, 3, 5)
for i in range(len(exh_avgRole)):
    plt.title('exhibition rating')
    plt.bar(exh_avgRole[i][0],exh_avgRole[i][1],width=0.2)
    plt.ylabel('average ratings')
plt.suptitle('Avg. ratings according to roles',fontsize=20)

plt.show

#%%

times  = [int(each) for each in df.how_manyTimes]

def avgAttend(src,timeSet,what2search):
    i = 0
    sum_time = 0
    avg_time = 0
    keys = []
    values = []
    for item in src:
        if(item == what2search):
            if(keys.count(item)==0):
                keys.append(item)
            
            sum_time = sum_time + times[i]
        else:
            sum_time = sum_time + 0
        i+=1    
    i = 0
    if(sum_time != 0):
        avg_time = sum_time/src.count(what2search)
        values.append(avg_time)
        sum_time = 0
        
    else:
        values.append(avg_time)
        sum_time = 0
        
    
    return [keys,values]
            

roleTime = []
for role in all_roles:
    roleTime.append(avgAttend(roles, times, role))
    
#%%

def whereAttend(src,timeSet,what2search):
    i = 0
    sum_time = 0
    avg_time = 0
    keys = []
    values = []
    for item in src:
        if(item == what2search):
            if(keys.count(item)==0):
                keys.append(item)
            
            sum_time = sum_time + times[i]
        else:
            sum_time = sum_time + 0
        i+=1    
    i = 0
    if(sum_time != 0):
        avg_time = sum_time/src.count(what2search)
        values.append(avg_time)
        sum_time = 0
        
    else:
        values.append(avg_time)
        sum_time = 0
        
    
    return [keys,values]


all_suggest = ['insta','twitter','utube','linkedin','website','someone','other_suggest']
whereAttendList = []
for suggest in all_suggest:
    whereAttendList.append(whereAttend(froms, times, suggest))

#%%
plt.figure()

plt.subplot(1, 2, 1)

for i in range(len(roleTime)):
    plt.title('Average attendance time acc. to their roles')
    plt.bar(roleTime[i][0],roleTime[i][1],width=0.2)
    plt.ylabel('average attendance')
plt.subplot(1, 2, 2)

for i in range(len(whereAttendList)):
    plt.title('Avg attendance time acc. to where they heard ITURO')
    plt.bar(whereAttendList[i][0],whereAttendList[i][1],width=0.2)
    plt.ylabel('average attendance')
        


plt.suptitle('Avg. attendance according ...',fontsize=20)


plt.show



#%%

nyr = [each for each in df.nyr]

plt.figure()
plt.title('Are the attendees will come back next year (Acc. to age)')
plt.scatter(ages,nyr,marker = '1',label = 'age/scale point',alpha = 0.5,color = 'r')
plt.xlabel('Ages')
plt.ylabel('opinions about attending next year (scale [0-100])')
plt.legend(loc = 'best')
plt.show()



#%%
