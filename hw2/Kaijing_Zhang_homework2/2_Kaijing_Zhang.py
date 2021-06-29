#!/usr/bin/env python
# coding: utf-8

# In[ ]:


total = 0
while(True):
    coin = int(input("Enter a coin! "))
    if coin == -1:
        break
    elif (coin == 10) or (coin == 25) or (coin == 50):
        total += coin
    else: 
        print("Please enter a valid coin value!")
# Use while loop to let user enter a number. 

if total == 0:
    print("I can't make change as: ")
else:
    print("I can make change as: ")
# Decide if the total number user input is greater than 0. 
    
res = {1:0, 2:0, 5:0, 10:0, 25:0, 50:0}
# Record how many each bill or coin have. 

if total % 10 == 5:
    res[25] += 1
    total -= 25
if total // 500 >= 1:
    res[5] += total // 500
    total -= 500 * (total // 500)
if total // 200 >= 1:
    res[2] += total // 200
    total -= 200 * (total // 200)
if total // 100 >= 1:
    res[1] += total // 100
    total -= 100 * (total // 100)
if total // 50 >= 1:
    res[50] += total // 50
    total -= 50 * (total // 50)
if  total // 10 >= 1:
    res[10] += total // 10
    total -= 10 * (total // 10)
# Calculate how we can exchange the total by descending order. 

if total != 0:
    print(f"ERROR!{total}")
# If something wrong, then error. 

if res[5] == 1:
    print("1 $5 bill")
elif res[5] > 1:
    print(f"{res[5]} $5 bills")
    
if res[2] == 1:
    print("1 $2 bill")
elif res[2] > 1:
    print(f"{res[2]} $2 bills")
    
if res[1] == 1:
    print("1 $1 bill")
elif res[1] > 1:
    print(f"{res[1]} $1 bills")
    
if res[50] == 1:
    print("1 50 cent coin")
elif res[50] > 1:
    print(f"{res[50]} 50 cent coins")
    
if res[25] == 1:
    print("1 25 cent coin")
elif res[25] > 1:
    print(f"{res[25]} 25 cent coins")
    
if res[10] == 1:
    print("1 10 cent coin")
elif res[10] > 1:
    print(f"{res[10]} 10 cent coins")
# Print each bill or coins.

bill_sum = res[1] * 1 + res[2] * 2 + res[5] * 5
coin_sum = res[10] * 10 + res[25] * 25 + res[50] * 50
# Calculate the total of bill and the total of coin. 

if bill_sum == 1 and coin_sum == 0:
    print(f"For a total of {bill_sum} dollar")
elif bill_sum > 1 and coin_sum == 0:
    print(f"For a total of {bill_sum} dollars")
elif bill_sum == 1 and coin_sum != 0:
    print(f"For a total of {bill_sum} dollar and {coin_sum} cents")
elif bill_sum > 1 and coin_sum != 0:
    print(f"For a total of {bill_sum} dollars and {coin_sum} cents")
elif bill_sum == 0 and coin_sum != 0:
    print(f"For a total of {coin_sum} cents")
elif bill_sum == 0 and coin_sum == 0:
    print(f"For a total coin {coin_sum} cents")
# Print the total of bill and the total of coin. 


# In[ ]:




