#!/usr/bin/env python
# coding: utf-8

# In[1]:


def question2(input1):
    output = list() # Create a empty list as output
    for item in input1:
        if type(item) == int or type(item) == float: 
            output.append(abs(item))
            # If the element is a numeric value, then add its absolut value to list. 
        else:
            try:
                convert = int(item)
                # If it's a non-numeric value, then try to convert it to integer.
                output.append(abs(convert))
                # If succeed, add it to list. 
            except ValueError:
                try:
                    convert = float(item)
                    # If fail, try to convert it to float
                    output.append(abs(convert))
                    # If succeed for second try, add it to list.
                except ValueError:
                    # If fail agian, then means it cannot be coverted to a numeric value. 
                    continue
                continue
    return output


# In[2]:


question2(['DSCI-510', -1, 0.1, 2, 'US', '0.0', '-1', "-10", "asda", "111"] )


# In[ ]:




