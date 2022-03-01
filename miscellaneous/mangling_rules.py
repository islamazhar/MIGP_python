def mangling_rules(password, bl_trie=None):
    if bl_trie is None:
        bl_trie = [] 
    new_pass = []
    #deletion
    if len(password) >1:
        result = password[:-1]
        if result not in bl_trie:  
            new_pass.append(result)
    if len(password) >2:
        result = password[:-2]
        if result not in bl_trie:  
            new_pass.append(result)
    result = password[1:]
    if result not in bl_trie:  
        new_pass.append(result)
    #addition
    result = password+str(1)
    if result not in bl_trie:  
        new_pass.append(result)
    result = password+str(12)
    if result not in bl_trie:  
        new_pass.append(result)
    result = password+str(123)
    if result not in bl_trie:  
        new_pass.append(result)
    result = password+str(0)
    if result not in bl_trie:  
        new_pass.append(result)
    #swap first char
    if len(password)>0:
        result = password.capitalize()
        if result == password:
            if result[0].isalpha():
                result = password[:1].lower() + password[1:]
                if result not in bl_trie:  
                    new_pass.append(result)
        else:
            if result not in bl_trie:  
                new_pass.append(result)
    #leet
    for i in leet:
        if (i[0]) in password:
            result = password.replace(i[0],i[1])
            if result not in bl_trie:  
                new_pass.append(result)
        if (i[1]) in password:
            result = password.replace(i[1],i[0])
            if result not in bl_trie:  
                new_pass.append(result)
    result = password+'07'
    if len(new_pass)!=10 and result not in bl_trie:      
        new_pass.append(result)
    result = password+'007'
    if len(new_pass)!=10 and result not in bl_trie:         
        new_pass.append(result)
    result = password+'08'
    if len(new_pass)!=10 and result not in bl_trie: 
        new_pass.append(result)

    # Error checking..
    for pw in new_pass:
        if pw in bl_trie:
            print(" Blocklisted password {} inside the mangling rules..".format(pw))
            exit(1)

    return new_pass