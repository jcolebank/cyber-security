import optparse

# Takes in a plaintext message
# and an integer key and encrypts
# using the Caesar cipher approach
def encrypt(msg, key):
   
    # define variables
    encryMes = ""
    
    # loop through each char in msg
    for char in msg:
        
        # check if upper case
        if ( ord(char) >= 65 and ord(char) <= 90):
            # shift each char and add to encryMes
            encryMes += chr((ord(char) + (key) - 65) % 26 + 65)
        
        # check if lower case
        elif ( ord(char) >= 97 and ord(char) <= 122):
            # shift each char and add to encryMes
            encryMes += chr((ord(char) + (key) - 97) % 26 + 97)

        # shift any other character values and add to encryMes
        else:
            encryMes += ' '

    # this shows the encrypted message
    print(msg + " encrypted is: " + encryMes)
    return encryMes
   

# Takes in an encrypted message
# and an integer key and decrypts
# using the Caesar cipher approach
def decrypt(msg, key):
    
    # define variables
    decryMes = ""

    #loop through each char in msg
    for char in msg:

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
            
    # this shows if the message was decrypted probably
    print(msg + " decrypted is: " + decryMes)
    return decryMes

def main():
    parser = optparse.OptionParser("usage%prog "+ "-f <decrypt | encrypt> -m <message> -k <key>")
    parser.add_option('-f', dest='function', type='string', help='[ decrypt | encrypt ]')
    parser.add_option('-m', dest='msg', type='string',  help='message to encrypt (plaintext) or decrypt (encrypted)')
    parser.add_option('-k', dest='key', type='string', help='cipher key as an integer')
    (options, args) = parser.parse_args()
    function = options.function
    if ((function != "encrypt" and function != "decrypt") or function == None):
        print('[-] You must specify a valid function: "encrypt" or "decrypt"')
        exit(0)
    msg = str(options.msg)
    key = int(options.key)
    if (msg == None) | (key == None):
        print('[-] You must specify a message and key.')
        exit(0)
    if function == "encrypt":
        encrypt(msg, key)
    elif function == "decrypt":
        decrypt(msg, key)

if __name__ == '__main__':
    main()

