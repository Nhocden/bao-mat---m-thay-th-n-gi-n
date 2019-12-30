# Simple Substitution Cipher
  # ttps://www.nostarch.com/crackingcodes/ (BSD Licensed)
 
import pyperclip, sys, random
 
 
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
 
def main():
     myMessage =' BTS (Bangtan Sonyeondan), also known as the Bangtan Boys, is a seven-member South Korean boy band formed in Seoul in 2013. The septet co-writes and produces much of their output. Originally a hip hop group, their musical style has evolved to include a wide range of genres. Their lyrics, often focused on personal and social commentary, touch on the themes of mental health, troubles of school-age youth, loss, the journey towards loving oneself, and individualism. Their work features references to literature and psychological concepts and includes an alternative universe storyline. The group have staged several world tours. '
     myKey = 'LFWOAYUISVKMNXPBDCRJTQEGHZ'
     myMode = 'encrypt' # Set to 'encrypt' or 'decrypt'.
     
    #  if keyIsValid(myKey):
    #      sys.exit('There is an error in the key or symbol set.')
     if myMode == 'encrypt':
         translated = encryptMessage(myKey, myMessage)
     elif myMode == 'decrypt':
         translated = decryptMessage(myKey, myMessage)
     print('\n')
     print('Using key %s' % (myKey))
     print('\n------------>>>\n')
     print('the mesage:\n')
     print(myMessage)
     print('\n------------>>>\n')
     print('The %sed message is:' % (myMode) )     
     print(translated)
     # pyperclip.copy(translated)
     print('\n')
     


def keyIsValid(key):
     keyList = list(key)
     lettersList = list(LETTERS)
     keyList.sort()
     lettersList.sort()

     return keyList == lettersList


def encryptMessage(key, message):
     return translateMessage(key, message, 'encrypt')


def decryptMessage(key, message):
     return translateMessage(key, message, 'decrypt')


def translateMessage(key, message, mode):
     translated = ''
     charsA = LETTERS
     charsB = key
     if mode == 'decrypt':
         # For decrypting, we can use the same code as encrypting. We
         # just need to swap where the key and LETTERS strings are used.
         charsA, charsB = charsB, charsA
     # Loop through each symbol in the message:
     for symbol in message:
         if symbol.upper() in charsA:
            # Encrypt/decrypt the symbol:
            symIndex = charsA.find(symbol.upper())
            if symbol.isupper():
                 translated += charsB[symIndex].upper()
            else:
                 translated += charsB[symIndex].lower()
         else:
             # Symbol is not in LETTERS; just add it:
             translated += symbol

     return translated


def getRandomKey():
     key = list(LETTERS)
     random.shuffle(key)
     return ''.join(key)


if __name__ == '__main__':
     main()