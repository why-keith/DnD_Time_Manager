day, tenday, month, year=1,1,1,1

def out():
    print(day, tenday, month, year)
    
def move(x):
    global day, tenday, month, year
    day+=x
    
z=50 #day 1=0
day_to_ten=[int(z/10),z%10]
day_to_month=[int(z/30),z%30]
day_to_year=[int(z/360),z%360]



y=int(z/360)+1
m=int((z%360)/30)+1
t=int((z%30)/10)+1
d=z%30+1


print(d,t,m,y)



