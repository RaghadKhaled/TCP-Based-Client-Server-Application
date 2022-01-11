# first of all import the socket library
import socket
# import AES algorithm from Crypto library
from Crypto.Cipher import AES


def do_encrypt(message):
    """
    take a message, encrypt it using AES algorithm, then return the message after encryption.
    """
    # shared secret key
    key = "This is a key123".encode('utf8')
    # shared IV(Initialization Vector)
    IV = "This is an IV456".encode('utf8')

    # generate the AES cipher object with CBC mode
    obj = AES.new(key, AES.MODE_CBC, IV)

    # encrypt the message
    ciphertextt = obj.encrypt(message.encode('utf8'))
    return ciphertextt


# write the server IP address and the port on which you want to connect
serverName = "192.168.100.8"
serverPort = 12000

# next create a socket object
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


try:
    # connecting to the server
    clientSocket.connect((serverName,serverPort))
    print('Connection Established in Client.')

    option = input("Select one of the options.\n"
                   "1.Open mode(to exchange messages as cleartext).\n"
                   "2.Secure mode(to exchange messages as ciphertext).\n"
                   "3.Quit application(to end the connection).\n")

    while True:

        if option.lower() == "open mode":
            # in open mode, the user will write a word, then the server will capitalize it
            print('\nYou chose open mode.')
            word = input("Input lowercase word:")

            print('Word will capitalize by the Server.')
            print('Sending word to Server...')
            # send the word
            clientSocket.send(word.encode())
            # send the option number to server (1 = cleartext)
            clientSocket.send(str('1').encode())

            # receive the word form server and decoding to get the string
            modifiedSentence = clientSocket.recv(1024).decode()
            print("Received the word from Server after capitalized it: ", modifiedSentence, '.')

            option = input('\nEnter another mode, or quit application to end the connection\n')

        elif option.lower() == "secure mode":
            # in secure mode, the user will write a word of 16 bits, then encrypt it
            # next, the client will send the ciphertext to the server
            # the server will decrypt it and send it back to the client
            # also the server will encrypt it and send it back to server

            print('\nYou chose secure mode.')
            word = input("Input secret word:")

            print('Word will encrypt with AES.')
            ciphertext = do_encrypt(word)
            print('The word is', word, '\nAfter encryption is', ciphertext)

            print('Sending encrypted word to Server...')
            # send the ciphertext
            clientSocket.send(ciphertext)
            # send the option number to server (2 = ciphertext)
            clientSocket.send(str('2').encode())

            # receive the word form the server as cleartext and decoding to get the string
            plaintext = clientSocket.recv(1024).decode()
            print("\nThe first receive: Received the word as cleartext from the Server after decrypted it: ", plaintext)

            # receive the word form the as ciphertext server
            plaintext_after_encrypted = clientSocket.recv(1024)
            print("The second receive: Received the word as ciphertext from the Server after encrypted it: ", plaintext_after_encrypted)

            option = input('\nEnter another mode, or quit application to end the connection\n')

        elif option.lower() == "quit application":
            # in quit mode, the connection end
            print('\nYou chose quit mode, the connection release...')

            # send option '3' to the server to indicate that the client is closed its connection
            clientSocket.send("No data".encode())
            clientSocket.send(str('3').encode())

            clientSocket.close()
            print('Connection End.')

            break
        else:
            print('You write wrong word, try again!')
            option = input('\nEnter another mode, or quit application to end the connection\n')


except:
    # if the client open connection and the server does not run (down)
    # an exception will be though here indicate that the server not running so we can't open connection
    print('Error: Server is down! So we can not establish the connection at the client')
