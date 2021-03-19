import optparse

def cracker(msg):

    # loop through keys from 1 to 25
    for key1 in range(1, 25):
        # call our decrypt function
        decrypt(msg, key1)
        # increase key value
        key1 += 1

# Takes in an encrypted message
# and an integer key and decrypts
# using the Caesar cipher approach
def decrypt(message, key):
    
    # define variables
    decryMes = ""

    #loop through each char in msg
    for char in message:

        # check if upper case
        if ( ord(char) >= 65 and ord(char) <= 90):
            # shift each char and add to decryMes
            decryMes += chr((ord(char) - (key) - 65) % 26 + 65)
        
         # check if lower case
        elif ( ord(char) >= 97 and ord(char) <= 122):
            # shift each char and add to decryMes
            decryMes += chr((ord(char) - (key) - 97) % 26 + 97)

        # this is going to decrypt a space
        else:
            #add to decryMes
            decryMes += ' '
            
    # this shows if the message was decrypted properly 
    print(message + " decrypted is: " + decryMes + "with a key value of ")
    print(key)
     

def main():
    parser = optparse.OptionParser("usage%prog "+ "-f <cracker> -m <message>")
    parser.add_option('-f', dest='function', type='string', help='[ cracker ]')
    parser.add_option('-m', dest='msg', type='string',  help='message to decrypt (encrypted)')
    (options, args) = parser.parse_args()
    function = options.function
    if ((function != "cracker") or function == None):
        print('[-] You must specify the function: "cracker"')
        exit(0)
    msg = str(options.msg)
    if (msg == None):
        print('[-] You must specify a message.')
        exit(0)
    if function == "cracker":
        cracker(msg)

if __name__ == '__main__':
    main()


    
