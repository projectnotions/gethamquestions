# from https://medium.com/@hafizabdullaha93/20-extremely-useful-single-line-python-codes-de44928a1a3b
# One line codes:
# 1. One-line For Loop
# 2. One-Line while Loop
# 3. One-Line If Else Statement
# 4. Merging dictionaries in one line
# 5. One Line Function
# 6. Recursion in one line
# 7. Filtering an array in one line
# 8. Exception Handling in One Line
# 9. Converting a List to a Dictionary in One Line
# 10. One-Line Multiple Variables
# 11. Swapping values in one line
# 12. One-Line Sorting
# 13. Reading a file in one line
# 14. One-Line Class
# 15. One-Line semicolon
# 16. One Line Print
# 17. One Line Map Function
# 18. Deleting the Mul elements from the first row of the list
# 19. One Line Print Pattern
# 20. Find Primes in a range in a single line of code

#For loop in one line
mylist = [200, 300, 400, 500]
#Single line For loop
result = [] 
for x in mylist: 
    if x > 250: 
        result.append(x) 
print(result) # [300, 400, 500]
#One-line code way
result = [x for x in mylist if x > 250] 
print(result) # [300, 400, 500]

# One line While Loop
#Method 1 Single Statement   
while True: print(1) #infinite 1  
#Method 2 Multiple Statements  
x = 0   
while x < 5: print(x); x= x + 1 # 0 1 2 3 4 5

#if Else In a single line.  
#Example 1 if else  
print("Yes") if 8 > 9 else print("No") # No  
#Example 2 if elif else   
E = 2   
print("High") if E == 5 else print("数据STUDIO") if E == 2 else   
print("Low") # Data STUDIO   
   
#Example 3 only if  
if 3 > 2: print("Exactly") # Exactly

# Merging dictionaries in one line  
d1 = { 'A': 1, 'B': 2 }   
d2 = { 'C': 3, 'D': 4 }  
#Method1   
d1.update(d2)   
print(d1) # {'A': 1, 'B': 2, 'C': 3, 'D': 4}  
#Method2   
d3 = {**d1, **d2}   
print(d3) # {'A': 1, 'B': 2, 'C': 3, 'D': 4}

#Function in one line  
#Method1
def fun(x): return True if x % 2 == 0 else False   
print(fun(2)) # False  
#Method2
fun = lambda x : x % 2 == 0   
print(fun(2)) # True   
print(fun(3)) # False

# Single-line recursion 
#Fibonaci Single-line recursion example  
def Fib(x): return 1 if x in {0, 1} else Fib(x-1) + Fib(x-2)  
print(Fib(5)) # 8  
print(Fib(15)) # 987

# Filtering arrays in a single line  
mylist = [2, 3, 5, 8, 9, 12, 13, 15]  
#Normal way  
result = []   
for x in mylist:   
    if x % 2 == 0:   
        result.append(x)  
print(result) # [2, 8, 12]  
# One-line method  
result = [x for x in mylist if x % 2 == 0]   
print(result) # [2, 8, 12]

# Exception handling in one line  
#Original method  
try:  
    print(x)  
except:  
    print("Error")  
#Single line way  
exec('try:print(x) \nexcept:print("Error")') # Error

# Dictionary in one line  
mydict = ["John", "Peter", "Mathew", "Tom"]  
mydict = dict(enumerate(mydict))  
print(mydict) # {0: 'John', 1: 'Peter', 2: 'Mathew', 3: 'Tom'}

#Multiple variable assignments in one line.  
#Single-line method  
x = 5   
y = 7   
z = 10   
print(x , y, z) # 5 7 10  
#Single line way  
a, b, c = 5, 7, 10   
print(a, b, c) # 5 7 10

#Swap values in one line  
#Single-line method 
v1 = 100  
v2 = 200  
temp = v1  
v1 = v2   
v2 = temp  
print(v1, v2) # 200 100  
# One-line value swapping 
v1, v2 = v2, v1   
print(v1, v2) # 200 100

# Sort in one line  
mylist = [32, 22, 11, 4, 6, 8, 12]   
# Method1
mylist.sort()   
print(mylist) # # [4, 6, 8, 11, 12, 22, 32]  
print(sorted(mylist)) # [4, 6, 8, 11, 12, 22, 32]

#Reading a file in one line  
#Single-line method 
with open("data.txt", "r") as file:   
    data = file.readline()   
    print(data) # Hello world  
#Single line way  
data = [line.strip() for line in open("data.txt","r")]   
print(data) # ['hello world', 'Hello Python']

# One-line class  
#Regular way  
class Emp:   
    def __init__(self, name, age):   
        self.name = name   
        self.age = age  
        emp1 = Emp("a44", 22)   
print(emp1.name, emp1.age) # 
#Single line way  
#Method 1 Lambda with Dynamic Attributes 
  
Emp = lambda:None; Emp.name = "a44"; Emp.age = 22  
print(Emp.name, Emp.age) # 
  
#Method 2 
from collections import namedtuple  
Emp = namedtuple('Emp', ["name", "age"]) ("a44", 22)   
print(Emp.name, Emp.age)

# One-line semicolon 
# exsample 1   
a = "Python"; b = "Programming"; c = "languages"; print(a, b, c)  
# print
# Python Programming languages

# One line print
#Single-line method
for x in range(1, 5):  
    print(x) # 1 2 3 4  
#Single line way  
print(*range(1, 5)) # 1 2 3 4  
print(*range(1, 6)) # 1 2 3 4 5

#One line map function 
print(list(map(lambda a: a + 2, [5, 6, 7, 8, 9, 10])))  
# print
# [7, 8, 9, 10, 11, 12]

# Deleting the Mul elements from the first row of the list
mylist = [100, 200, 300, 400, 500]  
del mylist[1::2]  
print(mylist) # [100, 300, 500]

# One line print pattern#   
# Single-line method  
for x in range(3):  
    print('😀')  
# print
# 😀 😀 😀  
#Single line way  
print('😀' * 3) # 😀 😀 😀   
print('😀' * 2) # 😀 😀   
print('😀' * 1) # 😀

# Find primes in a range in a single line of code
print(list(filter(lambda a: all(a % b != 0 for b in range(2, a)),  
                  range(2,20))))  
# print
# [2, 3, 5, 7, 11, 13, 17, 19]

