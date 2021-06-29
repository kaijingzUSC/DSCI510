#!/usr/bin/env python
# coding: utf-8

# In[ ]:


res = list()
while(True):
    value = input("Please enter a value: ") # Let user enter a value
    if value.lower() == 'done': # If user want to end, then stop and print
        print(res)
        mini = -len(res) 
        maxi = len(res) - 1 # Calculate the range of possible index
        break
    else:
        res.append(value) # Add value to list

while(True):
    try:
        index = input(f"Please enter an integer between {mini} and {maxi}: ")
        print(res[int(index)])
        break
        # Remind user what index is vaild, and if true, then break
    except (ValueError, IndexError):
        print("Your input is invaild!")
    # If input is a invaild index, catch error and prompt for re-entry.


# In[ ]:




