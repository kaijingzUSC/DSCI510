#!/usr/bin/env python
# coding: utf-8

# In[ ]:


ten = 1
one = 10
zero = -1
# a). # It will be a list from 0 to (one - 1) i.e. (10 - 1).
list(range(one)) 
# Output: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
# b). # It will be a list from zero(-1) to (one - 1). 
list(range(zero, one)) 
# Output: [-1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
# c). # It will be the element at index zero in a list from zero to (one - 1). 
list(range(zero, one))[zero] 
# Output: 9
# d). # It will be the element from first list and index is the element of second list with index (one - 1). 
list(range(zero, one))[list(range(zero, one))[one - 1]] 
# Output: 7
# e). # It will be a subarray of the list from one to (zero -1) and increment by ten. The subarray is from (ten - zero) to (one + zero - 1). 
list(range(one, ten, zero))[ten - zero : one + zero ]
# Output: [8, 7, 6, 5, 4, 3, 2]


# In[ ]:




