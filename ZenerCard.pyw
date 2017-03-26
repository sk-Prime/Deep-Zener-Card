#python 3.4.4 
import os
os.sys.path.append(os.getcwd())
secret=0
try:
    import secrets
    secret=1
except:
    import random
import tkinter as tk
from tkinter import scrolledtext

path=os.getcwd()+"\\randomChar.txt"
if not os.path.exists(path):
    fileo=open(path,'w')
    fileo.close()
class gui(object):
    def __init__(self,master):
        #operational variables
        self.correct=0 #for showing in label
        self.incorrect=0
        self.ranChar="" #computer generate
        self.userChar="" #human input
        self.char=["A","S","D","F","G"]
        #first random guess, before user
        self.guess=0
        self.check=tk.IntVar()
        self.check.set(1)
        if secret==0:
            self.guess=self.char[random.randint(0,4)]
        else:
            self.guess=self.char[secrets.randbelow(5)]
        #----------------------------------------
        
        #gui
        self.master=master
        self.master.title("Deep Zener Card")
        
        tk.Grid.rowconfigure(master, 0, weight=1)
        tk.Grid.columnconfigure(master, 0, weight=1)      
        
        self.preview=tk.Label(master, text="",font="consolas 30",relief="ridge",width=2)
        self.preview.pack()
        
        infoFrame=tk.LabelFrame(master, text="Cards")
        infoFrame.pack(fill='both',padx=5,pady=5)
        self.infoLabel=tk.Label(infoFrame,text="Correct=0 - Wrong=0 - Total=0\nCorrect=0%")
        self.infoLabel.pack(side='top')
        
        self.aButton=tk.Button(infoFrame,text='A',command=lambda: self.Action("A"),width=2)
        self.aButton.pack(side="left",pady=5,expand="yes")
        self.master.bind("a", lambda x: self.Action("A"))
        
        self.sButton=tk.Button(infoFrame,text='S',command=lambda: self.Action("S"),width=2)
        self.sButton.pack(side="left",pady=5,expand="yes")
        self.master.bind("s", lambda x: self.Action("S"))
        
        self.dButton=tk.Button(infoFrame,text='D',command=lambda: self.Action("D"),width=2)
        self.dButton.pack(side="left",pady=5,expand="yes")
        self.master.bind("d", lambda x: self.Action("D"))     
        
        self.fButton=tk.Button(infoFrame,text='F',command=lambda: self.Action("F"),width=2)
        self.fButton.pack(side="left",pady=5,expand="yes")
        self.master.bind("f", lambda x: self.Action("F"))
        
        self.fButton=tk.Button(infoFrame,text='G',command=lambda: self.Action("G"),width=2)
        self.fButton.pack(side="left",pady=5,expand="yes")
        self.master.bind("g", lambda x: self.Action("G"))
        
        self.cButton=tk.Button(infoFrame,text='Calculation',command=lambda: self.calculation())
        self.cButton.pack(side="left",pady=5,expand="yes")
        self.master.bind("<Return>", lambda x: self.calculation())
        
        self.checkbtn=tk.Checkbutton(infoFrame,text="write",variable=self.check)
        self.checkbtn.pack(side="left",pady=5,expand="yes")
        
        self.iButton=tk.Button(infoFrame,bitmap="info",relief="flat",command=self.info)
        self.iButton.pack(side="left",pady=0,expand="yes")
        self.master.bind("<F1>", lambda x: self.info)         
        
        
        self.st=scrolledtext.ScrolledText(master,width=40,height=24,font="consolas 8")
        self.st.insert('end',">> What will be the next card\n...Press that button\n")
        self.st.tag_config('blue',foreground="blue")
        self.st.tag_config('red',foreground="red")
        self.st.tag_config('center',justify="center")
        self.st.pack(pady=5,padx=5,fill='both',expand="yes")
    #gui end--------------------------------------------------------------
     
    #call back------------------------------------------------------------
    #info button
    def info(self):
        self.st.insert('end',"\n________________________________________\nDeep Zener Card\nVersion: 1.0\nAuthor: SK Salim\n________________________________________\n","blue")
        self.st.yview_pickplace('end')
    #-------------
    
    
    #ASDFG button action
    def Action(self,a=0):
        guessnumber=self.guess
        self.preview.config(text=guessnumber)
        self.ranChar+=guessnumber #storing all guessnumber of computer for further calculation. in calculation we use it for occurance frequency etc
        self.userChar+=a #storinng all human input for further calculation. mainly summary same as ranchar
        if(a==guessnumber):
            #if guess number correct and change the label value and insert text in text box
            self.st.insert("end",">> You Choose:%s -Correct\n"%a,'blue')
            self.correct+=1
            self.infoLabel.config(text="Correct=%d - Wrong=%d - Total=%d\nCorrect=%.4f%%"%(self.correct,self.incorrect,self.correct+self.incorrect,100.00*self.correct/(self.correct+self.incorrect)))
        else:
            #if not it wrong chang label and value
            self.st.insert("end",">> %s-Incorrect | Correct-%s\n"%(a,guessnumber))
            self.incorrect+=1
            self.infoLabel.config(text="Correct=%d - Wrong=%d - Total=%d\nCorrect=%.4f%%"%(self.correct,self.incorrect,self.correct+self.incorrect,100.00*self.correct/(self.correct+self.incorrect)))
        #calculating random number before the user guess
        if secret==1:
            self.guess=self.char[secrets.randbelow(5)]
        else:
            self.guess=self.char[random.randint(0,4)]
        self.st.yview_pickplace('end')
    #end------------------------------------------
    
    #calculation, statistics---------------------------------
    def calculation(self):
        charset="ASDFG" #for looping usage
        randomChar=self.ranChar #copy of computer generated radom char through the play time
        userChar=self.userChar  #copy of user inputed radom char through the play time
        sAvrgFreq=[] #first five for computer last five user. summary
        stimes=[] #first five computer last five user. summary usage
        sMostOccur=[] #for summary making
        
        if self.check.get()==1:
            fileo=open(path,'a')
            fileo.write(randomChar) #writing random char in txt file
            fileo.close()        
        
        def frequency_calc(char,text):
            #calculate a char index, frequency, count in text string
            indexlist=[] #all index of that char in text string
            difflist=[] #contain first index minus nearest index= index difference. for calculating frequency. how many time it occur. first occurence - second occurance
            collectiveDiff=0 #sum of all difflist item to calculate frequency
            times=text.count(char) #count
            avrgFrequency=0 #frequency of char difflist/len(difflist) so the average frequency
            if (times>0):
                start=0
                for i in range(times):
                    #getting index
                    index=text.find(char,start)
                    start=index+1 #finding from start index to last
                    indexlist.append(index)
                for c in range(times-1):
                    #frequency
                    diff=indexlist[c+1]-indexlist[c] #first apperance - near apperance is the difference, when it occur again
                    difflist.append(diff) #appending for statistic view
                    collectiveDiff+=diff #adding to make collective/sum of difference to make average
            if collectiveDiff>0:
                #avoid zero division error
                avrgFrequency=float(collectiveDiff)/(times-1)
            sAvrgFreq.append(avrgFrequency) #list of all avrfrequency to make summary
            stimes.append(times) #all times to make summary
            return(indexlist,times,difflist,avrgFrequency)
        
        self.st.insert('end','----------------------------------------\n','center red')
        self.st.insert('end',"Computer\n",'center red') #computer brief stat
        self.st.insert('end','----------------------------------------\n','center red')
        for i in charset:
            indexList,times,Appear,avrgFrequency=frequency_calc(i,randomChar) #slicing return to individual variable, here randomchar is computer
            self.st.insert('end',"\nLetter %s:"%i,'blue') #to distinguis color, making letter blue
            self.st.insert('end'," %d Times AvrgFrequency: %.2f\n"%(times,avrgFrequency)) #adding with letter and first line of letter times and average frequency
            self.st.insert('end',"Frequency: "+" ".join(str(c) for c in Appear)) #frequency is long line so it in new line same as index
            self.st.insert('end',"\nIndex: "+" ".join(str(c) for c in indexList)+"\n")
        self.st.yview_pickplace('end')
        
        self.st.insert('end','----------------------------------------\n','center red')
        self.st.insert('end',"User\n",'center red') #user brief stat
        self.st.insert('end','----------------------------------------\n','center red')
        for i in charset:
            indexList,times,Appear,avrgFrequency=frequency_calc(i,userChar) #changing variable for user stat
            self.st.insert('end',"\nLetter %s:"%i,'blue')
            self.st.insert('end'," %d Times AvrgFrequency: %.2f\n"%(times,avrgFrequency))
            self.st.insert('end',"Frequency: "+" ".join(str(c) for c in Appear))
            self.st.insert('end',"\nIndex: "+" ".join(str(c) for c in indexList)+"\n")
        self.st.yview_pickplace('end')
        self.st.insert('end','----------------------------------------\n','center red')
        self.st.insert('end',"Comp : ",'blue')
        self.st.insert('end',"%s"%randomChar)
        self.st.insert('end',"\nUser : ",'blue')
        self.st.insert('end',"%s\n"%userChar)   
        
        #sequence of generating random number
        if self.check.get()==1:
            self.st.insert('end','----------------------------------------\n','center red')
            self.st.insert('end',"Repeating Combination\n",'center red')
            self.st.insert('end','----------------------------------------\n','center red')    
            
            fileo=open(path,'r') #opening random text
            text=fileo.readline()
            fileo.close() #close
            for i in range (5):
                mostOccur=""  #contain letter of combination which most occur, ex: AG or AF most occur in random generation. Most time G comes after A appear
                mostOccurNum=0 #how many times
                char1=charset[i] #first char like A
                for x in range (5):
                    char2=charset[x] #second charecter to make double letter word for calculating which letter come next most
                    findSet=char1+char2
                    count=text.count(findSet)# counting how many of them
                    if count>mostOccurNum:
                        mostOccurNum=count
                        mostOccur=findSet
                    self.st.insert('end',findSet+": ")
                    self.st.insert("end","%-4s"%str(count),"blue")    
                self.st.insert("end","\n")
                sMostOccur.append(mostOccur) #appendig to list to make summary
                sMostOccur.append(mostOccurNum)
        
        
        self.st.insert('end','----------------------------------------\n','center red')
        self.st.insert('end',"Summary\n",'center red')
        self.st.insert('end','----------------------------------------\n','center red')
        userfreq=sAvrgFreq[5:]
        computerFreq=sAvrgFreq[0:5]
        userTimes=stimes[5:]
        computerTimes=stimes[0:5]
        
        self.st.insert('end',"Average Frequency\n",'blue')
        self.st.insert('end',"%-15s"%"Letter"+"%-15s"%"User"+"%s"%"Computer\n")
        for i in range(5):
            letter=charset[i] 
            self.st.insert('end',"%-15s"%letter+"%-15.2f"%sAvrgFreq[i+5]+"%.2f"%sAvrgFreq[i]+"\n") #geting value from savrgfreq. first five is computer's last five user

        self.st.insert('end',"\nTimes\n",'blue')
        self.st.insert('end',"%-15s"%"Letter"+"%-15s"%"User"+"%s"%"Computer\n")
        for i in range(5):
            letter=charset[i]
            self.st.insert('end',"%-15s"%letter+"%-15d"%stimes[i+5]+"%d"%stimes[i]+"\n")   #stimes slicing
        
        #which cobmination of two letter occur most. if write enable this will show
        if self.check.get()==1:
            self.st.insert('end',"\nMost Common Combination\nFrom RandomChar.txt\n",'blue')
            for i in range(0,len(sMostOccur),2):#because it contain mostoccur combination and times. first is char second is times. like ["AG",2,"SF",3] so pick first then for i+1 is second.
                self.st.insert('end',sMostOccur[i]+": ")
                self.st.insert('end',""+str(sMostOccur[i+1])+"%-1s"%" ","blue")
            self.st.insert("end","\n")
            
            
        self.st.insert('end','----------------------------------------\n','center red')
        self.st.yview_pickplace('end')

        
root=tk.Tk()
app=gui(root)
root.mainloop()
        
