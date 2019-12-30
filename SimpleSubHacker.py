# Simple Substitution Cipher Hacker
 # https://www.nostarch.com/crackingcodes/ (BSD Licensed)

import os, re, copy, pyperclip, simpleSubCipher, wordPatterns,makeWordPatterns
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
nonLettersOrSpacePattern = re.compile('[^A-Z\s]')

def main():
    message = 'FJR (Flxujlx Rpxhapxolx), lmrp kxpex lr jia Flxujlx Fphr, sr l raqax-nanfac Rptji Kpcalx fph flxo ypcnao sx Raptm sx 2013. Jia rabjaj wp-ecsjar lxo bcpotwar ntwi py jiasc ptjbtj. Pcsusxlmmh l isb ipb ucptb, jiasc ntrswlm rjhma ilr aqpmqao jp sxwmtoa l esoa clxua py uaxcar. Jiasc mhcswr, pyjax ypwtrao px bacrpxlm lxo rpwslm wpnnaxjlch, jptwi px jia jianar py naxjlm ialmji, jcptfmar py rwippm-lua hptji, mprr, jia vptcxah jpelcor mpqsxu pxaramy, lxo sxosqsotlmsrn. Jiasc epck yaljtcar cayacaxwar jp msjacljtca lxo brhwipmpuswlm wpxwabjr lxo sxwmtoar lx lmjacxljsqa txsqacra rjpchmsxa. Jia ucptb ilqa rjluao raqaclm epcmo jptcr. '

   # Determine the possible valid ciphertext translations:
    print('\n')
    print('Hacking...')
    letterMapping = hackSimpleSub(message)
    # tao 1 bang 

   # Display the results to the user:
    print('\n')
    print('Mapping:')
    print(letterMapping)
    print('\n------------>>>')
    print('Original ciphertext:')
    print('\n')
    print(message)
    print('\n------------>>>')
    print('hacked message:')
    print('\n')
    hackedMessage = decryptWithCipherletterMapping(message, letterMapping)
    pyperclip.copy(hackedMessage)
    print(hackedMessage)
    print('\n')

def getBlankCipherletterMapping():
    # Returns a dictionary value that is a blank cipherletter mapping:
    return {'A': [], 'B': [], 'C': [], 'D': [], 'E': [], 'F': [], 'G': [],
           'H': [], 'I': [], 'J': [], 'K': [], 'L': [], 'M': [], 'N': [],
           'O': [], 'P': [], 'Q': [], 'R': [], 'S': [], 'T': [], 'U': [],
           'V': [], 'W': [], 'X': [], 'Y': [], 'Z': []}

def addLettersToMapping(letterMapping, cipherword, candidate):
    # The letterMapping parameter takes a dictionary value that
    # stores a cipherletter mapping, which is copied by the function.
    # The cipherword parameter is a string value of the ciphertext word.
    # The candidate parameter is a possible English word that the
    # cipherword could decrypt to.

    # This function adds the letters in the candidate as potential
    # decryption letters for the cipherletters in the cipherletter
    # mapping.
 
    for i in range(len(cipherword)):
       if candidate[i] not in letterMapping[cipherword[i]]:
            letterMapping[cipherword[i]].append(candidate[i])
 
def intersectMappings(mapA, mapB):
    # To intersect two maps, create a blank map and then add only the
    # potential decryption letters if they exist in BOTH maps:
    intersectedMapping = getBlankCipherletterMapping()
    for letter in LETTERS:

        # An empty list means "any letter is possible". In this case just
        # copy the other map entirely:
        if mapA[letter] == []:
           intersectedMapping[letter] = copy.deepcopy(mapB[letter])
        elif mapB[letter] == []:
           intersectedMapping[letter] = copy.deepcopy(mapA[letter])
        else:
           # If a letter in mapA[letter] exists in mapB[letter],
           # add that letter to intersectedMapping[letter]:
            for mappedLetter in mapA[letter]:
              if mappedLetter in mapB[letter]:
                intersectedMapping[letter].append(mappedLetter)

    return intersectedMapping

def removeSolvedLettersFromMapping(letterMapping):
    # Cipherletters in the mapping that map to only one letter are
    # "solved" and can be removed from the other letters.
    # For example, if 'A' maps to potential letters ['M', 'N'], and 'B'
    # maps to ['N'], then we know that 'B' must map to 'N', so we can
    # remove 'N' from the list of what 'A' could map to. So 'A' then maps
    # to ['M']. Note that now that 'A' maps to only one letter, we can
    # remove 'M' from the list of letters for every other letter.
    # (This is why there is a loop that keeps reducing the map.)

    loopAgain = True
    while loopAgain:
        # First assume that we will not loop again:
        loopAgain = False

        # solvedLetters will be a list of uppercase letters that have one
        # and only one possible mapping in letterMapping:
        solvedLetters = []
        for cipherletter in LETTERS:
            if len(letterMapping[cipherletter]) == 1:
                solvedLetters.append(letterMapping[cipherletter][0])

        # If a letter is solved, then it cannot possibly be a potential
        # decryption letter for a different ciphertext letter, so we
        # should remove it from those other lists:
        for cipherletter in LETTERS:
            for s in solvedLetters:
                if len(letterMapping[cipherletter]) != 1 and s in letterMapping[cipherletter]:
                    letterMapping[cipherletter].remove(s)
                    if len(letterMapping[cipherletter]) == 1:
                        # A new letter is now solved, so loop again:
                        loopAgain = True
    return letterMapping

def hackSimpleSub(message):
    intersectedMap = getBlankCipherletterMapping()
    # tao 1 ban anh xa moi
    cipherwordList = nonLettersOrSpacePattern.sub('',
           message.upper()).split() 
        #  xoa cac ki tu khong phai la chu
    for cipherword in cipherwordList:
        # Get a new cipherletter mapping for each ciphertext word:
        candidateMap = getBlankCipherletterMapping()

        wordPattern = makeWordPatterns.getWordPattern(cipherword)
        if wordPattern not in wordPatterns.allPatterns:
            continue # This word was not in our dictionary, so continue.

        # Add the letters of each candidate to the mapping:
        for candidate in wordPatterns.allPatterns[wordPattern]:
            addLettersToMapping(candidateMap, cipherword, candidate)

        # Intersect the new mapping with the existing intersected mapping:
        intersectedMap = intersectMappings(intersectedMap, candidateMap)

    # Remove any solved letters from the other lists:
    return removeSolvedLettersFromMapping(intersectedMap)


def decryptWithCipherletterMapping(ciphertext, letterMapping): 
    # tham so la mes va bang da map tao ra  1 chuoi khoa
    # Return a string of the ciphertext decrypted with the letter mapping,
    # with any ambiguous decrypted letters replaced with an underscore.

    # First create a simple sub key from the letterMapping mapping:
    key = ['x'] * len(LETTERS)
    for cipherletter in LETTERS:
        if len(letterMapping[cipherletter]) == 1:
            # If there's only one letter, add it to the key:
            keyIndex = LETTERS.find(letterMapping[cipherletter][0])
            key[keyIndex] = cipherletter
        else:
            ciphertext = ciphertext.replace(cipherletter.lower(), '_')
            ciphertext = ciphertext.replace(cipherletter.upper(), '_')
    key = ''.join(key)

    # With the key we've created, decrypt the ciphertext:
    return simpleSubCipher.decryptMessage(key, ciphertext)
    # tao ra ban ro


if __name__ == '__main__':
    main()