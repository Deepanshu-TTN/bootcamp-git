#1. Given string my_string = ‘Hello Python!’, Reverse the string using slicing, print ’!’ using indexing
def q1():
    my_string = "Hello Python!"
    print(my_string[::-1]+"\n"+my_string[-1])

#2. Use slicing to get word “frain” from “information”.
def q2():
    word = "Information"
    print(word[2::2])

#3. Using examples explain string.format and f-strings
def q3():
    '''Basic Usage'''
    name = "Deepanshu"
    age = 21
    print("Hi! I'm {} and I'm {} years old".format(name,age)) #string.format
    print(f"Hi! I'm {name} and I'm {age} years old") #f-string

    '''Positional Arguments and Number Formatting'''
    lit = "pi"
    val = 3.14159
    print("The value of {1} is {0:0.2f}".format(val, lit)) #string.format
    print(f"The value of {lit} is {val:0.2f}") #f-string

    '''Dictionaries and Named Arguments'''
    dic = {"name":"Deepanshu", "score":10}
    print("{name} scored {score} in Python".format(**dic)) #string.format
    print(f"{dic['name']} scored {dic['score']} in Python") #f-string

    #Expression evaluation
    a,b = 10,2
    print(f"{a} x {b} = {a*b}")


#4. Can we sort a dictionary? Why or why not?
def q4():
    # well no, but we can sort either of the ordered key value pair and store it in a new data structure
    dic = {"banana":3, "apple":1, "cranberry":2}
    sorted_list_using_keys = sorted(dic.items())
    sorted_list_using_values = sorted(dic.items(), key = lambda item: item[1])

    #or we can create new dictionaries in sorted order of keys/values
    sorted_dic_using_keys = {k:dic[k] for k in sorted(dic)}
    sorted_dic_using_values = {k:v for k,v in sorted(dic.items(), key = lambda item: item[1])}
    print(sorted_list_using_keys)
    print(sorted_list_using_values)
    print(sorted_dic_using_keys)
    print(sorted_dic_using_values)


def q5():
    d = {'simple_key':'hello'}
    print(d['simple_key'])
    d = {'k1':{'k2':'hello'}}
    print(d['k1']['k2'])
    d = {'k1':[{'nest_key':['this is deep',['hello']]}]}
    print(d['k1'][0]['nest_key'][1][0])
    d = {'k1':[1,2,{'k2':['this is tricky',{'tough':[1,2,['hello']]}]}]}
    print(d['k1'][2]['k2'][1]['tough'][2][0])


def q6():
    list3 = [1,2,[3,4,'hello']]
    list3[2][2] = "goodbye"
    print(list3)


def q7():
    list5 = [1,2,2,33,4,4,11,22,3,3,2]
    set5 = set(list5)
    print(set5)


def q8():
    str1 = "information"
    print(f"using count() {str1.count('i')}")

    ct = 0
    for char in str1:
        if char=='i':
            ct+=1
    print(f"using for loop {ct}")

    print(f"using generator expression {sum(1 for char in str1 if char == 'i')}") 

