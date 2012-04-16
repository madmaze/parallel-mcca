def context(sentence):
        length = len(sentence)
        wordlist = {}
        cvector = {}
        for n,x in enumerate(s):
                if x in cvector:
                        wordlist = cvector[x]        
                if n >1:
                        temp = s[n-2]

                        if len(wordlist)==0:
                                wordlist[temp] = 1
                        else:
                                if (temp) in wordlist:
                                        value = wordlist[temp]
                                        value = value + 1
                                        wordlist[temp] = value
                                else:
                                        wordlist[temp] = 1
                if n >0:
                        temp = s[n-1]

                        if len(wordlist)==0:
                                wordlist[temp] = 1
                        else:
                                if (temp) in wordlist:
                                        value = wordlist[temp]
                                        value = value + 1
                                        wordlist[temp] = value
                                else:
                                        wordlist[temp] = 1
                if n < (length-1):
                        temp = s[n+1]

                        if len(wordlist)==0:
                                wordlist[temp] = 1
                        else:
                                if (temp) in wordlist:
                                        value = wordlist[temp]
                                        value = value + 1
                                        wordlist[temp] = value
                                else:
                                        wordlist[temp] = 1
                if n < (length-2):
                        temp = s[n+2]

                        if len(wordlist)==0:
                                wordlist[temp] = 1
                        else:
                                if (temp) in wordlist:
                                        value = wordlist[temp]
                                        value = value + 1
                                        wordlist[temp] = value
                                else:
                                        wordlist[temp] = 1                        
                cvector[x] = wordlist
                wordlist = {}                  
        return cvector
