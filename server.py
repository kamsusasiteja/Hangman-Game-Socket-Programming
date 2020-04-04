import random
import string
import socket
import os
import pickle
import operator
import threading

class HangmanServer:

    def __init__(self, IP, port):
        self.scores={}
        self.prevWords = {}
        super().__init__()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP) as self.s:
            self.s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            self.s.bind((IP, port))
            self.s.listen()
            print("TCP server up and listening....")
            while True:
                conn, addr = self.s.accept()
                print("Connected to...",addr)
                thread = threading.Thread(target = self.start_game , args = (conn,))
                thread.start()
                
    def start_game(self,conn):
        """
        starts the game and checks the guessed letters with the secret word and updates the user
        """
        with conn:
            secretWord,user=self.open_game(conn)           
            lettersGuessed = []
            totalguesses=8
            conn.send(("Start!! \n I am thinking of a word that is "+str(len(secretWord))+" letters long.").encode())
            while(totalguesses>0):
                dat = "-----------------------------------------"+"\n"
                dat += "You have "+str(totalguesses)+" guesses left. "+"\n"
                dat+="Available letters: "+self.getAvailableLetters(lettersGuessed)+"\n"+"Please guess a letter: "
                conn.send(dat.encode())
                guess = conn.recv(1024).decode()
                guessinLower = guess.lower().strip()
                if len(guessinLower)!=1 or not guessinLower.isalpha() :
                    conn.send("Invalid".encode())
                    continue
                if (guessinLower in secretWord) and (guessinLower not in lettersGuessed) :
                    lettersGuessed += guessinLower
                    if self.isWordGuessed(secretWord,lettersGuessed):
                        final = self.calculate_score(totalguesses,user,secretWord) 
                        conn.send(("Won "+secretWord+" "+str(final)).encode())
                        break
                    else:
                        conn.send(("Good "+self.getGuessedWord(secretWord,lettersGuessed)).encode())
                elif guessinLower in lettersGuessed:
                    conn.send(("Already "+self.getGuessedWord(secretWord,lettersGuessed)).encode())
                else:
                    lettersGuessed += guessinLower
                    totalguesses-=1
                    if(totalguesses==0):
                        final = self.calculate_score(totalguesses,user,secretWord)
                        conn.send(("Lose "+secretWord+" "+str(final)).encode())
                        break
                    else:
                        conn.send(("Wrong "+self.getGuessedWord(secretWord,lettersGuessed)).encode())
            self.leader_board(conn)
        conn.close()
    
    def calculate_score(self,totalguesses,user,secretWord):
        """
        calculates the score of the user and updates the score to the user data base
        """
        final = (10*len(secretWord)) - ((8-totalguesses)*len(secretWord))
        sc = self.scores[user]+final
        self.scores[user] = sc
        return final

    def leader_board(self,conn):
        """
        sends the updated leaderboard to the user when the game is over
        """
        sorted_d = dict( sorted(self.scores.items(), key=operator.itemgetter(1),reverse=True))
        conn.send(pickle.dumps(sorted_d))
        print("List of prev words for users")
        print(self.prevWords)
    
    def open_game(self,conn):
        """
        starts the game and takes the user details and selects the secret word
        and makes sure that the secret wors is not played by the user previously
        """
        conn.send("Welcome to game Hangman.\nType: [new/old][space][username]".encode())
        data = conn.recv(1024).decode().split(" ")
        print(data)
        user = data[1]
        if ((data[0]=="old") and (user in list(self.scores.keys()))):
            conn.send("Existing user welcome aboard...".encode())
        elif data[0]=="new":
            conn.send("New user created...".encode())
            self.scores[user]=0
            self.prevWords[user]=[]
        elif ((data[0] == "old") and (user not in list(self.scores.keys()))):
            conn.send("Error! user dont exist in database. Creating now...".encode())
            self.scores[user]=0
            self.prevWords[user]=[]
        print("Users in data base")
        print(list(self.scores.keys()))
        wordlist = self.loadWords()
        while True:
            secretWord = self.chooseWord(wordlist).lower()
            if(secretWord not in self.prevWords[user]):
                break
        self.prevWords[user].append(secretWord)
        print(user,secretWord, len(secretWord))  
        return secretWord,user

    def loadWords(self):
        """
        Returns a list of valid words. Words are strings of lowercase letters.    
        """
        print("Loading word list from file...")
        wordlist = open(r'C:\Users\User\Desktop\hangman\words.txt').read().split(" ")
        print("  ", len(wordlist), "words loaded.")
        return wordlist
    
    def chooseWord(self,wordlist):
        """
        Returns a word from wordlist at random
        """
        return random.choice(wordlist).strip()
    
    def isWordGuessed(self,secretWord, lettersGuessed):
        '''
        returns: boolean, True if all the letters of secretWord are in lettersGuessed;
        False otherwise
        '''
        result = False
        for c in secretWord:
            if c in lettersGuessed:
                result = True
            else:
                return False
        return result

    def getGuessedWord(self,secretWord,lettersGuessed):
        '''
        returns String, with letters and underscores that represents what
        letters in secretword have been guessed so far
        '''
        l,i = [],0
        while i<len(secretWord):
            for j in secretWord:
                if j in lettersGuessed:
                    l.insert(i,j)
                else :
                    l.insert(i,'_')
                i+=1
        return ''.join(l)

    def getAvailableLetters(self,lettersGuessed):
        '''
        returns: string, comprised of letters that represents what letters have not
        yet been guessed.
        '''
        availableLetters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        for c in lettersGuessed:
            availableLetters.remove(c)
        availableLettersString = ''
        for e in availableLetters:
            availableLettersString = availableLettersString + e
        return availableLettersString

def main():
    # test harness checks for your web server on the localhost and on port 8888
    # do not change the host and port
    # you can change  the HTTPServer object if you are not following OOP
    HangmanServer('localhost', 8000)

if __name__ == "__main__":
    main()