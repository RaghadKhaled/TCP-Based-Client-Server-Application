# first of all import the socket library
import socket
# import AES algorithm from Crypto library
from Crypto.Cipher import AES


def do_decrypt(ciphertext):
    """
    take a ciphertext, decrypt it using AES algorithm, then return the text after decryption.
    """
    # shared secret key
    key = "This is a key123".encode('utf8')
    # shared IV(Initialization Vector)
    IV = "This is an IV456".encode('utf8')

    # generate the AES cipher object with CBC mode
    obj2 = AES.new(key, AES.MODE_CBC, IV)

    # decrypt the message
    message = obj2.decrypt(ciphertext)
    return message


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
serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# bind the IP address and the port number
serverSocket.bind((serverName,serverPort))

# put the socket into listening mode, just listen to connection with one client
serverSocket.listen(1)
print("The server is ready to receive")


while True:

    # Establish connection with client.
    connectionSocket, addr = serverSocket.accept()
    print("Connection Established in Server. Client IP address",addr[0], "Client port number", addr[1])

    while True:
        # receive the word form client
        word = connectionSocket.recv(1024)
        # receive the option number
        option = connectionSocket.recv(1024).decode()

        if option == '1':
            # option = 1 ,the word is clearest
            # in open mode, the server received cleartext from the client
            print("Received word from client:", word.decode())

            # the server will capitalize it and send it back to the client
            print('Word is cleartext, so I will capitalize.')
            capitalizedSentence = word.upper()

            print("Send the word to Client after capitalized it...\n\n")
            # send the capitalized word to the client. encoding to send byte type.
            connectionSocket.send(capitalizedSentence)
        elif option == '2':
            # option = 2 ,the word is ciphertext
            # in secure mode, the server received ciphertext from the client

            print("Received word from client:", word)
            print('The word is encrypted, so I will decrypt.')

            # the server will decrypt it and send it back to the client as a cleartext
            plaintext = do_decrypt(word)
            print('The word after decrypted is:', plaintext.decode())

            print("\nThe first send: send the decrypted word to the Client as cleartext...")
            # send the plaintext to the client. encoding to send byte type.
            connectionSocket.send(plaintext)

            # the server also will encrypt it and send it back to the client as a ciphertext
            ciphertext = do_encrypt(plaintext.decode())
            print("The second send: send the word after encrypted by the Server to the Client as ciphertext...\n\n")
            # send the ciphertext to the client. encoding to send byte type.
            connectionSocket.send(ciphertext)

        elif option == '3':
            # option = 3 , quit application
            print('The client ended its connection, I will end the connection as well..')
            # Close the connection with the client
            connectionSocket.close()
            print('Connection End.')
            # Breaking once connection closed
            break
    break