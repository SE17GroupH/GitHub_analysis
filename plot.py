import numpy as np
import matplotlib.pyplot as plt
  
User1 = np.array([1,1,0,2,0,0,6,2,1,0,0,0,0])
User2 = np.array([0,0,5,4,0,0,4,0,1,0,0,0,4])
User3 = np.array([0,5,4,2,0,3,13,4,0,0,0,0,0])

N = len(User1)
ind = np.arange(1,N+1)
width = 0.5           # the width of the bars: can also be len(x) sequence


colors = ('b', 'r', 'orange')
data = (User1, User2, User3)
bottom = np.zeros(N)
arr=[]
for elem, color in zip(data, colors):
    a = plt.bar(ind, elem, width, bottom=bottom, color=color)
    arr.append(a[0])
    bottom += elem

#plt.title("Repository Activity")
#plt.ylabel('Lines of Code Changed')
plt.title("Commit Activity")
plt.ylabel("Commits")
plt.xlabel('Weeks')

#plt.xticks(ind+width/2, ('Found Guilty: Felony', 'Pled Guilty: Mis', 'Pled Guilty: Felony' ) )
#plt.yticks(np.arange(10,200,10))
plt.legend (arr, ('User1', 'User2','User3'))

plt.show()