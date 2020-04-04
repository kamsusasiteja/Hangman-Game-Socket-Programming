import socket 
import pickle

def start_guessing():
    while True:
        print(s.recv(1024).decode())
        s.send(input().encode())
        st = s.recv(1024).decode().split(" ")
        if(st[0]=="Invalid"):
            print("Invalid character")
        elif(st[0]=="Good"):
            print("Good Guess : ",st[1])
        elif(st[0]=="Won"):
            print("Congratulations! you won! Your word: ",st[1]," Score: ",st[2],".")
            break
        elif(st[0]=="Already"):
            print("Oops! You've already guessed the letter: ",st[1])
        elif(st[0]=="Wrong"):
            print("Oops! That letter is not in the word : ",st[1])
        elif(st[0]=="Lose"):
            print("Sorry, you ran out of guesses. Your word: ",st[1]," Score: ",st[2],".") 
            break

def leader_board():
    data = pickle.loads(s.recv(1024))
    print("\n"+"*LeaderBoard*")
    # print("UserName\tScore")
    for d in data.keys():
        print(d+'\t'+str(data[d]))


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
s.connect(('localhost',8000))
print(s.recv(1024).decode())
s.send(input().encode())
print(s.recv(1024).decode())
print(s.recv(1024).decode())
start_guessing()
leader_board()
s.close()