#Importing tkinter under an alias (a much shorter name) called tk
import tkinter as tk                
from tkinter import font as tkfont  
import random
from tkinter import messagebox, PhotoImage,Menu,ttk
import time
import pygame


class InitializeGame(tk.Tk): 

    def __init__(self, *args, **kwargs): 
        tk.Tk.__init__(self, *args, **kwargs)
        #We are calling the init function of the Tk class (explicit declaration to create a root window)
        #Tk class helps us to create a root window
        #Implicit way of declaring would be : root = tk.Tk() - this would automatically create a root window
        #because instantiating an object of a class, leads to immediate execution of the init function of the class
        #Instead we are showing explicitly the init function call by passing it in the class InitializeGame 
        self.geometry("2000x2000")
        self.title_font = tkfont.Font(font=('Georgia',33)) 
        container = tk.Frame(self)
        container.pack(side="top",fill="both",expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        for F in (GameMenu, LevelOne, LevelTwo):
            #__name__ is a built-in variable which evaluates to the name of the current module
            #When running the code __name__ sets to __main__, when some moddule is being imported, __name__ sets to the module name
            #Every class is assigned to a variable named page_name in every iteration of the for loop 
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("GameMenu")

    def show_frame(self, page_name):                    #adds appropriate message as per the level
        frame = self.frames[page_name]
        if(page_name == "LevelOne"):
            messagebox.showinfo("General instructions","You have 8 pairs of images, match them within 90 seconds to reach level 2.")
        elif(page_name == "LevelTwo"):
            messagebox.showinfo("General instructions","You have 8 images of one kind and 8 corresponding images which you have to match them with.\n Testing your GK!!\n time limit: 120 secs")
        frame.tkraise()


class GameMenu(tk.Frame):

    def __init__(self, parent, controller):
        #The __init__ function of the Frame class of tkinter is called
        tk.Frame.__init__(self, parent, bg="papaya whip")
        self.controller = controller
        label = tk.Label(self, text="TileDuo : Select Level", font=controller.title_font, bg="papaya whip")
        label.pack(side="top", fill="x", pady=10)
        button1 = tk.Button(self, text="Play Level 1",
                            command=lambda: controller.show_frame("LevelOne"), bg="lemon chiffon")
        button2 = tk.Button(self, text="Play Level 2",
                            command=lambda: controller.show_frame("LevelTwo"), bg="lemon chiffon")
        button1.pack()
        button2.pack()
        #pygame mixer is used for playing songs
        pygame.mixer.init()
        def play():
            pygame.mixer.music.load("Music.ogg")
            pygame.mixer.music.play(loops = 100) 
        B = tk.Button(self,text = "Click me for BGM during the game",font = ("Georgia",10), command = play, bg = "lemon chiffon")
        B.pack(pady = 20)





class LevelOne(tk.Frame):


    def __init__(self, parent, controller):
        
        self.winner = 0
        self.count = 0
        self.checker_list = []
        self.checker_dict = {}
        self.tilesopened = 0
        self.scoreboard=0
        self.timer=90  
        self.bonus_pair_list = []
        self.accuracy=0                                 #added timer and score board
        photo0 = PhotoImage(file = r"bomb_tile.png")
        photo1 = PhotoImage(file = r"ChocolateFrog.png")
        photo2 = PhotoImage(file = r"HogwartsEmblem.png")
        photo3 = PhotoImage(file = r"Snitch.png")
        photo4 = PhotoImage(file = r"Platform.png")
        photo5 = PhotoImage(file = r"Hedwig.png")
        photo6 = PhotoImage(file = r"TimeTurner.png")
        photo7 = PhotoImage(file = r"HarryRonHermione.png")
        photo8 = PhotoImage(file = r"bonus_tile.png")
    
        photoimage0 = photo0.subsample(5,5) 
        photoimage1 = photo1.subsample(5,5)
        photoimage2 = photo2.subsample(5,5)
        photoimage3 = photo3.subsample(5,5)
        photoimage4 = photo4.subsample(5,5)
        photoimage5 = photo5.subsample(5,5)
        photoimage6 = photo6.subsample(5,5)
        photoimage7 = photo7.subsample(5,5)
        photoimage8 = photo8.subsample(5,5)
        
        #image_dict is a dictionary with keys from 0 to 7 and values being the images under the tiles
        self.image_dict1 = {0:photoimage1,1:photoimage2,2:photoimage3,3:photoimage4,4:photoimage5,5:photoimage6,6:photoimage7}
        self.image_dict2 = {7:photoimage0,8:photoimage8} #dict containing features tiles 
        self.image_array_numbers = list(self.image_dict1.keys()) + list(self.image_dict1.keys()) + list(self.image_dict2.keys())
        #The list elements are shuffled randomly using the shuffle method of the random module
        random.shuffle(self.image_array_numbers)
        
        self.number_to_number_dict = {}
        for i in range(len(self.image_array_numbers)):
            self.number_to_number_dict[i] = self.image_array_numbers[i]


        def giveup():
            self.winner = 0

            self.image_array_numbers = list(self.image_dict1.keys()) + list(self.image_dict1.keys()) + list(self.image_dict2.keys())            
            random.shuffle(self.image_array_numbers)
            my_label.config(text="You gave up. You lost",bg="papaya whip")
            self.scoreboard=0
            self.timer=90
            timerlabel.config(text="Time remaining:"+str(self.timer))
            scorelabel.config(text="Score: "+str(self.scoreboard))
            for i in range(len(self.image_array_numbers)):
                self.number_to_number_dict[i]=self.image_array_numbers[i]

            tile_list = [b0,b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11,b12,b13,b14,b15]
            number=0
            for tile in tile_list:
                
                if self.number_to_number_dict[number] == 7 or self.number_to_number_dict[number] == 8 :
                    tile["image"] = self.image_dict2[self.number_to_number_dict[number]]
                else :
                    tile["image"] = self.image_dict1[self.number_to_number_dict[number]]
                number+=1
                tile.config(text="",bg="AntiqueWhite3",state="normal")

        def reset():
            
            b0 = tk.Button(self, text=' ', font=("Georgia", 20), height=4, width=4, bg="AntiqueWhite3", command= lambda: checktime(b0, 0), relief="groove")
            b1 = tk.Button(self, text=' ', font=("Georgia", 20), height=4, width=4, bg="AntiqueWhite3", command= lambda: checktime(b1, 1), relief="groove")
            b2 = tk.Button(self, text=' ', font=("Georgia", 20), height=4, width=4, bg="AntiqueWhite3", command= lambda: checktime(b2, 2), relief="groove")
            b3 = tk.Button(self, text=' ', font=("Georgia", 20), height=4, width=4, bg="AntiqueWhite3", command= lambda: checktime(b3, 3), relief="groove")
            b4 = tk.Button(self, text=' ', font=("Georgia", 20), height=4, width=4, bg="AntiqueWhite3", command= lambda: checktime(b4, 4), relief="groove")
            b5 = tk.Button(self, text=' ', font=("Georgia", 20), height=4, width=4, bg="AntiqueWhite3", command= lambda: checktime(b5, 5), relief="groove")
            b6 = tk.Button(self, text=' ', font=("Georgia", 20), height=4, width=4, bg="AntiqueWhite3", command= lambda: checktime(b6, 6), relief="groove")
            b7 = tk.Button(self, text=' ', font=("Georgia", 20), height=4, width=4, bg="AntiqueWhite3", command= lambda: checktime(b7, 7), relief="groove")
            b8 = tk.Button(self, text=' ', font=("Georgia", 20), height=4, width=4, bg="AntiqueWhite3", command= lambda: checktime(b8, 8), relief="groove")
            b9 = tk.Button(self, text=' ', font=("Georgia", 20), height=4, width=4, bg="AntiqueWhite3", command= lambda: checktime(b9, 9), relief="groove")
            b10 = tk.Button(self, text=' ', font=("Georgia", 20), height=4, width=4, bg="AntiqueWhite3", command= lambda: checktime(b10, 10), relief="groove")
            b11 = tk.Button(self, text=' ', font=("Georgia", 20), height=4, width=4, bg="AntiqueWhite3", command= lambda: checktime(b11, 11), relief="groove")
            b12 = tk.Button(self, text=' ', font=("Georgia", 20), height=4, width=4, bg="AntiqueWhite3", command= lambda: checktime(b12, 12), relief="groove")
            b13 = tk.Button(self, text=' ', font=("Georgia", 20), height=4, width=4, bg="AntiqueWhite3", command= lambda: checktime(b13, 13), relief="groove")
            b14 = tk.Button(self, text=' ', font=("Georgia", 20), height=4, width=4, bg="AntiqueWhite3", command= lambda: checktime(b14, 14), relief="groove")
            b15 = tk.Button(self, text=' ', font=("Georgia", 20), height=4, width=4, bg="AntiqueWhite3", command= lambda: checktime(b15, 15), relief="groove")

            b0.grid(row=1, column=0, sticky='nsew')
            b1.grid(row=1, column=1, sticky='nsew')
            b2.grid(row=1, column=2, sticky='nsew')
            b3.grid(row=1, column=3, sticky='nsew')
            b4.grid(row=2, column=0, sticky='nsew')
            b5.grid(row=2, column=1, sticky='nsew')
            b6.grid(row=2, column=2, sticky='nsew')
            b7.grid(row=2, column=3, sticky='nsew')
            b8.grid(row=3, column=0, sticky='nsew')
            b9.grid(row=3, column=1, sticky='nsew')
            b10.grid(row=3, column=2, sticky='nsew')
            b11.grid(row=3, column=3, sticky='nsew')
            b12.grid(row=4, column=0, sticky='nsew')
            b13.grid(row=4, column=1, sticky='nsew')
            b14.grid(row=4, column=2, sticky='nsew')
            b15.grid(row=4, column=3, sticky='nsew')

            self.scoreboard=0
            self.timer=90
            self.accuracy=0
            acclabel.config(text="accuracy: "+str(self.accuracy))
            self.tilesopened=0
            tilelabel.config(text = "No of tiles flipped : "+str(self.tilesopened), bg="papaya whip")
            timerlabel.config(text="Time remaining: "+str(self.timer))
            scorelabel.config(text="Score: "+str(self.scoreboard))




        def matched():                                  #game ends with updated scoreboard and timer and controls moves to level 2
            
            my_label.config(text="You WON! Congratulations!",bg="papaya whip")
            tile_list = [b0,b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11,b12,b13,b14,b15]
            for tile in tile_list:
                tile.config(bg="lavender")
            messagebox.showinfo("Game summary","You have finished level 1, taking you to Level 2")
            controller.show_frame("LevelTwo")

        def checktime(b,number):                            #game begins by setting timer
            if(self.timer<=0):
                messagebox.showinfo("Game finished","OOPS! You exceeded time limit. Try again!")
                controller.show_frame("GameMenu")
            else:
                tile_select(b,number)
        

        #The method tile_select takes a button and a number corresponding to the button clicked (b0 button indicates number = 0)
        def tile_select(b, number):

            if(self.tilesopened==0):
                self.start_time=time.monotonic()

            my_label.config(text="")
            if b["text"] == ' ' and self.count < 2:
                self.tilesopened += 1
                tilelabel.config(text = "No of tiles flipped : "+str(self.tilesopened), bg="papaya whip")
                b["text"] = self.number_to_number_dict[number]
                if self.number_to_number_dict[number] == 7 or self.number_to_number_dict[number] == 8 :
                    b["image"] = self.image_dict2[self.number_to_number_dict[number]]
                else :
                    b["image"] = self.image_dict1[self.number_to_number_dict[number]]
                self.checker_list.append(self.number_to_number_dict[number])
                self.checker_dict[b] = self.number_to_number_dict[number]
                self.count += 1

            
            
            if (len(self.checker_list) == 1 and self.checker_list[0] == 7) :                                             # Penalty tile code
                my_label.config(text="Penalty Tile",bg="papaya whip")
                tk.messagebox.showinfo("Oops!", "Penalty Tile chosen: PRESS ENTER")
                for tile in self.checker_dict:
                    tile["text"] = " "
                    tile["image"] = ""

                self.count = 0
                self.checker_list = []
                self.checker_dict = {}               
                self.start_time = self.start_time - 5
                self.scoreboard -= round((90-time.monotonic()+self.start_time-5)*2,0)
                '''if self.winner == 7:
                    self.winner += 1'''
                if self.winner == 7:
                    self.scoreboard += self.timer
                    self.timer = 0
                    timerlabel.config(text="Time remaining: "+str(self.timer),bg="papaya whip")
                    scorelabel.config(text="Final score: "+str(self.scoreboard),bg="papaya whip")
                    matched()
            
            if (len(self.checker_list) == 1 and self.checker_list[0] == 8) :                                               #Bonus Tile Code
                my_label.config(text="Bonus Tile",bg="papaya whip")
                tk.messagebox.showinfo("Bonanza!", "Bonus Tile chosen: PRESS ENTER")
                for tile in self.checker_dict:
                    tile["text"] = " "
                    tile["image"] = ""
                    tile['bg'] = "peach puff"
                for tile_num in self.checker_dict:
                    tile_num["state"] = "disabled"
                self.count = 0
                self.checker_list = []
                self.checker_dict = {}
                self.start_time = self.start_time + 5
                self.scoreboard += round((90-time.monotonic()+self.start_time+5)*2,0)
                '''if self.winner == 7:
                    self.winner += 1'''
                if self.winner == 7:
                    self.scoreboard += self.timer
                    self.timer = 0
                    timerlabel.config(text="Time remaining: "+str(self.timer),bg="papaya whip")
                    scorelabel.config(text="Final score: "+str(self.scoreboard),bg="papaya whip")
                    matched()

            if len(self.checker_list) == 2:
                
                if (self.checker_list[1] == 7) :                                                                                         #penalty tile code
                    my_label.config(text="Penalty Tile",bg="papaya whip")
                    tk.messagebox.showinfo("Oops!", "Penalty Tile chosen: PRESS ENTER")
                    for tile in self.checker_dict:
                        tile["text"] = " "
                        tile["image"] = ""
                    
                    self.count = 0
                    self.checker_list = []
                    self.checker_dict = {}
                    
                    self.start_time = self.start_time - 5
                    self.scoreboard -= round((90-time.monotonic()+self.start_time-5)*2,0)
                    '''if self.winner == 7:
                        self.winner += 1'''
                    if self.winner == 7:
                        self.scoreboard += self.timer
                        self.timer = 0
                        timerlabel.config(text="Time remaining: "+str(self.timer),bg="papaya whip")
                        scorelabel.config(text="Final score: "+str(self.scoreboard),bg="papaya whip")
                        matched()
                
                elif (self.checker_list[1] == 8) :                                                                                     #Bonus Tile Code
                    my_label.config(text="Bonus Tile",bg="papaya whip")
                    tk.messagebox.showinfo("Bonanza!", "Bonus Tile chosen: PRESS ENTER")
                    for tile in self.checker_dict:
                        if tile["text"] == 8:
                            tile["text"] = " "
                            tile["image"] = ""
                            tile["bg"] = "peach puff"
                            tile["state"] = "disabled"
                        else :
                            tile["text"] = " "
                            tile["image"] = "" 
                    
                    self.count = 0
                    self.checker_list = []
                    self.checker_dict = {}
                    
                    self.start_time = self.start_time + 5
                    self.scoreboard += round((90-time.monotonic()+self.start_time+5)*2,0)
                    '''if self.winner == 7:
                        self.winner += 1'''
                    if self.winner == 7:
                        self.scoreboard += self.timer
                        self.timer = 0
                        timerlabel.config(text="Time remaining: "+str(self.timer),bg="papaya whip")
                        scorelabel.config(text="Final score: "+str(self.scoreboard),bg="papaya whip")
                        matched()

                elif self.checker_list[0]==self.checker_list[1]:
                    my_label.config(text="Tile duo found!",bg="papaya whip")
                    tk.messagebox.showinfo("Correct!", "Correct: PRESS ENTER")
                    for tile in self.checker_dict:
                        tile["text"] = " "
                        tile["image"] = ""
                        tile['bg'] = "peach puff"
                    for tile_num in self.checker_dict:
                        tile_num["state"] = "disabled"
                    self.count = 0
                    self.accuracy += 1
                    self.checker_list = []
                    self.checker_dict = {}
                    self.winner += 1
                    self.scoreboard += round((90-time.monotonic()+self.start_time)*2,0)
                    if self.winner == 7:
                        self.scoreboard += self.timer
                        self.timer = 0
                        timerlabel.config(text="Time remaining: "+str(self.timer),bg="papaya whip")
                        scorelabel.config(text="Final score: "+str(self.scoreboard),bg="papaya whip")
                        matched()
    
                else:
                    
                    self.count = 0
                    self.checker_list = []
                    my_label.config(text="Incorrect! Not a match!", bg= "papaya whip")
                    tk.messagebox.showinfo("Incorrect!", "Incorrect: PRESS ENTER")
                    for tile in self.checker_dict:
                        tile["text"] = " "
                        tile["image"] = ""
                    self.checker_dict = {}
            scorelabel.config(text="Score: "+str(self.scoreboard), bg="papaya whip")
            self.timer = 90 + self.start_time-time.monotonic()
            self.timer = round(self.timer,0)
            timerlabel.config(text="Time remaining: " + str(self.timer), bg="papaya whip")
            accurate=self.accuracy*200//self.tilesopened
            print(accurate)
            acclabel.config(text="Accuracy : "+str(accurate) + "%", bg = "papaya whip")

        tk.Frame.__init__(self, parent, bg="papaya whip")
        self.controller = controller
        label = tk.Label(self, text="Level 1", font=controller.title_font, bg="papaya whip")
        label.grid(row=0,column=0)
        button = tk.Button(self, text="Show all tiles ",command = giveup , bg="papaya whip")
        reset = tk.Button(self,text="Reset",command=reset,bg="papaya whip")

        b0 = tk.Button(self, text=' ', font=("Georgia", 20), height=4, width=4, bg="AntiqueWhite3", command= lambda: checktime(b0, 0), relief="groove")
        b1 = tk.Button(self, text=' ', font=("Georgia", 20), height=4, width=4, bg="AntiqueWhite3", command= lambda: checktime(b1, 1), relief="groove")
        b2 = tk.Button(self, text=' ', font=("Georgia", 20), height=4, width=4, bg="AntiqueWhite3", command= lambda: checktime(b2, 2), relief="groove")
        b3 = tk.Button(self, text=' ', font=("Georgia", 20), height=4, width=4, bg="AntiqueWhite3", command= lambda: checktime(b3, 3), relief="groove")
        b4 = tk.Button(self, text=' ', font=("Georgia", 20), height=4, width=4, bg="AntiqueWhite3", command= lambda: checktime(b4, 4), relief="groove")
        b5 = tk.Button(self, text=' ', font=("Georgia", 20), height=4, width=4, bg="AntiqueWhite3", command= lambda: checktime(b5, 5), relief="groove")
        b6 = tk.Button(self, text=' ', font=("Georgia", 20), height=4, width=4, bg="AntiqueWhite3", command= lambda: checktime(b6, 6), relief="groove")
        b7 = tk.Button(self, text=' ', font=("Georgia", 20), height=4, width=4, bg="AntiqueWhite3", command= lambda: checktime(b7, 7), relief="groove")
        b8 = tk.Button(self, text=' ', font=("Georgia", 20), height=4, width=4, bg="AntiqueWhite3", command= lambda: checktime(b8, 8), relief="groove")
        b9 = tk.Button(self, text=' ', font=("Georgia", 20), height=4, width=4, bg="AntiqueWhite3", command= lambda: checktime(b9, 9), relief="groove")
        b10 = tk.Button(self, text=' ', font=("Georgia", 20), height=4, width=4, bg="AntiqueWhite3", command= lambda: checktime(b10, 10), relief="groove")
        b11 = tk.Button(self, text=' ', font=("Georgia", 20), height=4, width=4, bg="AntiqueWhite3", command= lambda: checktime(b11, 11), relief="groove")
        b12 = tk.Button(self, text=' ', font=("Georgia", 20), height=4, width=4, bg="AntiqueWhite3", command= lambda: checktime(b12, 12), relief="groove")
        b13 = tk.Button(self, text=' ', font=("Georgia", 20), height=4, width=4, bg="AntiqueWhite3", command= lambda: checktime(b13, 13), relief="groove")
        b14 = tk.Button(self, text=' ', font=("Georgia", 20), height=4, width=4, bg="AntiqueWhite3", command= lambda: checktime(b14, 14), relief="groove")
        b15 = tk.Button(self, text=' ', font=("Georgia", 20), height=4, width=4, bg="AntiqueWhite3", command= lambda: checktime(b15, 15), relief="groove")

        self.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6,7), weight=1)

        right_frame = tk.Frame(self,bg="papaya whip", width="700")

        scorelabel= tk.Label(self,font = controller.title_font, text= "Score: 0",bg="papaya whip")
        acclabel= tk.Label(self,font = controller.title_font, text= "Accuracy: 0",bg="papaya whip")
        tilelabel = tk.Label(self,font= controller.title_font, text = "No of tiles flipped : 0",bg="papaya whip")           #adds label for scoreboard and timer
        tilelabel.grid(row = 4, column = 4)
        scorelabel.grid(row=1,column=4)
        acclabel.grid(row=3,column=4)
        
        
        timerlabel = tk.Label(self, font= controller.title_font, text="time remaining: "+str(self.timer),bg="papaya whip")
        timerlabel.grid(row=2, column=4)

        b0.grid(row=1, column=0, sticky='nsew')
        b1.grid(row=1, column=1, sticky='nsew')
        b2.grid(row=1, column=2, sticky='nsew')
        b3.grid(row=1, column=3, sticky='nsew')
        b4.grid(row=2, column=0, sticky='nsew')
        b5.grid(row=2, column=1, sticky='nsew')
        b6.grid(row=2, column=2, sticky='nsew')
        b7.grid(row=2, column=3, sticky='nsew')
        b8.grid(row=3, column=0, sticky='nsew')
        b9.grid(row=3, column=1, sticky='nsew')
        b10.grid(row=3, column=2, sticky='nsew')
        b11.grid(row=3, column=3, sticky='nsew')
        b12.grid(row=4, column=0, sticky='nsew')
        b13.grid(row=4, column=1, sticky='nsew')
        b14.grid(row=4, column=2, sticky='nsew')
        b15.grid(row=4, column=3, sticky='nsew')

        right_frame.grid(row=0, column=4)
        my_label = tk.Label(self, text="")
        button.grid(row=7, column=1, columnspan=2)
        reset.grid(row=7, column=3, columnspan=2)
        my_label.grid(row=6, column=1, columnspan=2)

class LevelTwo(tk.Frame):

    def __init__(self, parent, controller):
        
        self.winner = 0
        self.count = 0
        self.accuracy=0
        self.checker_list = []
        self.checker_dict = {}
        self.tilesopened = 0
        self.scoreboard=0
        self.timer = 120
        
        photo0 = PhotoImage(file = r"CristianoRonaldo.png")
        photo1 = PhotoImage(file = r"Football.png")
        photo2 = PhotoImage(file = r"Einstein.png")
        photo3 = PhotoImage(file = r"e=mc2.png")
        photo4 = PhotoImage(file = r"EmmaWatson.png")
        photo5 = PhotoImage(file = r"MovieClapperboard.png")
        photo6 = PhotoImage(file = r"EllenDegeneres.png")
        photo7 = PhotoImage(file = r"Laughs.png")
        photo8 = PhotoImage(file = r"JackieChan.png")
        photo9 = PhotoImage(file = r"Fight.png")
        photo10 = PhotoImage(file = r"KalpanaChawla.png")
        photo11 = PhotoImage(file = r"Space.png")
        photo14 = PhotoImage(file = r"bomb_tile.png")
        photo15 = PhotoImage(file = r"bonus_tile.png")
        photo12 = PhotoImage(file = r"TaylorSwift.png")
        photo13 = PhotoImage(file = r"Mic.png")
    
        photoimage0 = photo0.subsample(5,5)
        photoimage1 = photo1.subsample(5,5)
        photoimage2 = photo2.subsample(5,5)
        photoimage3 = photo3.subsample(5,5)
        photoimage4 = photo4.subsample(5,5)
        photoimage5 = photo5.subsample(5,5)
        photoimage6 = photo6.subsample(5,5)
        photoimage7 = photo7.subsample(5,5)
        photoimage8 = photo8.subsample(5,5)
        photoimage9 = photo9.subsample(5,5)
        photoimage10 = photo10.subsample(5,5)
        photoimage11 = photo11.subsample(5,5)
        photoimage12 = photo12.subsample(5,5)
        photoimage13 = photo13.subsample(5,5)
        photoimage14 = photo14.subsample(5,5)
        photoimage15 = photo15.subsample(5,5)

        self.image_dict1 = {0:photoimage0,1:photoimage1,2:photoimage2,3:photoimage3,4:photoimage4,5:photoimage5,6:photoimage6,7:photoimage7,
        8:photoimage8,9:photoimage9,10:photoimage10,11:photoimage11,12:photoimage12,13:photoimage13}
        self.image_dict2 = {14:photoimage14,15:photoimage15}
        #imagenum_to_imagenum is a dictionary which contains match combinations (two ways for each pair of images)
        self.imagenum_to_imagenum = {0:1,1:0,2:3,3:2,4:5,5:4,6:7,7:6,8:9,9:8,10:11,11:10,12:13,13:12}
        self.image_array_numbers = list(self.image_dict1.keys()) + list(self.image_dict2.keys())
        random.shuffle(self.image_array_numbers)
        self.number_to_number_dict = {}
        for i in range(len(self.image_array_numbers)):
            self.number_to_number_dict[i] = self.image_array_numbers[i]

        def giveup():
            self.winner = 0

            self.image_array_numbers = list(self.image_dict1.keys()) + list(self.image_dict1.keys()) + list(self.image_dict2.keys())            
            random.shuffle(self.image_array_numbers)
            my_label.config(text="You gave up. You lost",bg="papaya whip")
            self.scoreboard=0
            self.timer=90
            timerlabel.config(text="Time remaining:"+str(self.timer))
            scorelabel.config(text="Score: "+str(self.scoreboard))
            for i in range(len(self.image_array_numbers)):
                self.number_to_number_dict[i]=self.image_array_numbers[i]

            tile_list = [b0,b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11,b12,b13,b14,b15]
            number=0
            for tile in tile_list:
                
                if self.number_to_number_dict[number] == 7 or self.number_to_number_dict[number] == 8 :
                    tile["image"] = self.image_dict2[self.number_to_number_dict[number]]
                else :
                    tile["image"] = self.image_dict1[self.number_to_number_dict[number]]
                number+=1
                tile.config(text="",bg="AntiqueWhite3",state="normal")

        def reset():
            
            b0 = tk.Button(self, text=' ', font=("Georgia", 20), height=4, width=4, bg="AntiqueWhite3", command= lambda: checktime(b0, 0), relief="groove")
            b1 = tk.Button(self, text=' ', font=("Georgia", 20), height=4, width=4, bg="AntiqueWhite3", command= lambda: checktime(b1, 1), relief="groove")
            b2 = tk.Button(self, text=' ', font=("Georgia", 20), height=4, width=4, bg="AntiqueWhite3", command= lambda: checktime(b2, 2), relief="groove")
            b3 = tk.Button(self, text=' ', font=("Georgia", 20), height=4, width=4, bg="AntiqueWhite3", command= lambda: checktime(b3, 3), relief="groove")
            b4 = tk.Button(self, text=' ', font=("Georgia", 20), height=4, width=4, bg="AntiqueWhite3", command= lambda: checktime(b4, 4), relief="groove")
            b5 = tk.Button(self, text=' ', font=("Georgia", 20), height=4, width=4, bg="AntiqueWhite3", command= lambda: checktime(b5, 5), relief="groove")
            b6 = tk.Button(self, text=' ', font=("Georgia", 20), height=4, width=4, bg="AntiqueWhite3", command= lambda: checktime(b6, 6), relief="groove")
            b7 = tk.Button(self, text=' ', font=("Georgia", 20), height=4, width=4, bg="AntiqueWhite3", command= lambda: checktime(b7, 7), relief="groove")
            b8 = tk.Button(self, text=' ', font=("Georgia", 20), height=4, width=4, bg="AntiqueWhite3", command= lambda: checktime(b8, 8), relief="groove")
            b9 = tk.Button(self, text=' ', font=("Georgia", 20), height=4, width=4, bg="AntiqueWhite3", command= lambda: checktime(b9, 9), relief="groove")
            b10 = tk.Button(self, text=' ', font=("Georgia", 20), height=4, width=4, bg="AntiqueWhite3", command= lambda: checktime(b10, 10), relief="groove")
            b11 = tk.Button(self, text=' ', font=("Georgia", 20), height=4, width=4, bg="AntiqueWhite3", command= lambda: checktime(b11, 11), relief="groove")
            b12 = tk.Button(self, text=' ', font=("Georgia", 20), height=4, width=4, bg="AntiqueWhite3", command= lambda: checktime(b12, 12), relief="groove")
            b13 = tk.Button(self, text=' ', font=("Georgia", 20), height=4, width=4, bg="AntiqueWhite3", command= lambda: checktime(b13, 13), relief="groove")
            b14 = tk.Button(self, text=' ', font=("Georgia", 20), height=4, width=4, bg="AntiqueWhite3", command= lambda: checktime(b14, 14), relief="groove")
            b15 = tk.Button(self, text=' ', font=("Georgia", 20), height=4, width=4, bg="AntiqueWhite3", command= lambda: checktime(b15, 15), relief="groove")

            b0.grid(row=1, column=0, sticky='nsew')
            b1.grid(row=1, column=1, sticky='nsew')
            b2.grid(row=1, column=2, sticky='nsew')
            b3.grid(row=1, column=3, sticky='nsew')
            b4.grid(row=2, column=0, sticky='nsew')
            b5.grid(row=2, column=1, sticky='nsew')
            b6.grid(row=2, column=2, sticky='nsew')
            b7.grid(row=2, column=3, sticky='nsew')
            b8.grid(row=3, column=0, sticky='nsew')
            b9.grid(row=3, column=1, sticky='nsew')
            b10.grid(row=3, column=2, sticky='nsew')
            b11.grid(row=3, column=3, sticky='nsew')
            b12.grid(row=4, column=0, sticky='nsew')
            b13.grid(row=4, column=1, sticky='nsew')
            b14.grid(row=4, column=2, sticky='nsew')
            b15.grid(row=4, column=3, sticky='nsew')

            self.scoreboard=0
            self.timer=90
            self.tilesopened=0
            self.accuracy=0
            acclabel.config(text="accuracy: "+str(self.accuracy))
            tilelabel.config(text = "No of tiles flipped : "+str(self.tilesopened), bg="papaya whip")
            timerlabel.config(text="Time remaining: "+str(self.timer))
            scorelabel.config(text="Score: "+str(self.scoreboard))

        def matched():
            
            my_label.config(text="You WON! Congratulations!")
            tile_list = [b0,b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11,b12,b13,b14,b15]
            for tile in tile_list:
                tile.config(bg="lavender")
            
            messagebox.showinfo("GAME OVER","You have successfully completed the game!!")
            controller.show_frame("GameMenu")

        def checktime(b,number):
            if(self.timer<0):
                scorelabel.config(text="Final Score: "+str(self.scoreboard))
                messagebox.showinfo("GAME OVER" ," YOU HAVE EXCEEDED TIME LIMIT. TRY AGAIN!")
                controller.show_frame("GameMenu")
            else:
                tile_select(b,number)
            

        def tile_select(b, number):
            
            my_label.config(text="")
            if(self.tilesopened==0):
                self.start_time=time.monotonic()
                
            if b["text"] == ' ' and self.count < 2:
                self.tilesopened += 1
                tilelabel.config(text = "No of tiles flipped : "+str(self.tilesopened),bg="papaya whip")
                b["text"] = self.number_to_number_dict[number]
                if self.number_to_number_dict[number] == 14 or self.number_to_number_dict[number] == 15 :
                    b["image"] = self.image_dict2[self.number_to_number_dict[number]]
                else :
                    b["image"] = self.image_dict1[self.number_to_number_dict[number]]                             
                self.checker_list.append(self.number_to_number_dict[number])                
                self.checker_dict[b] = self.number_to_number_dict[number]
                self.count += 1

            if (len(self.checker_list) == 1 and self.checker_list[0] == 14) :                                             # Penalty tile code
                my_label.config(text="Penalty Tile",bg="papaya whip")
                tk.messagebox.showinfo("Oops!", "Penalty Tile chosen: PRESS ENTER")
                for tile in self.checker_dict:
                    tile["text"] = " "
                    tile["image"] = ""             
                self.count = 0
                self.checker_list = []
                self.checker_dict = {}
                
                self.start_time = self.start_time - 5
                self.scoreboard -= round((120-time.monotonic()+self.start_time-5)*2,0)
                if self.winner == 7:
                    self.winner += 1
                if self.winner == 8:
                    self.scoreboard += self.timer
                    self.timer = 0
                    timerlabel.config(text="Time remaining: "+str(self.timer),bg="papaya whip")
                    scorelabel.config(text="Final score: "+str(self.scoreboard),bg="papaya whip")
                    matched()

            if (len(self.checker_list) == 1 and self.checker_list[0] == 15) :                                               #Bonus Tile Code
                my_label.config(text="Bonus Tile",bg="papaya whip")
                tk.messagebox.showinfo("Bonanza!", "Bonus Tile chosen: PRESS ENTER")
                for tile in self.checker_dict:
                    tile["text"] = " "
                    tile["image"] = ""
                    tile['bg'] = "peach puff"
                for tile_num in self.checker_dict:
                    tile_num["state"] = "disabled"  
                self.count = 0
                self.checker_list = []
                self.checker_dict = {}
                
                self.start_time = self.start_time + 5
                self.scoreboard += round((120-time.monotonic()+self.start_time+5)*2,0)
                '''if self.winner == 7:
                    self.winner += 1'''
                if self.winner == 7:
                    self.scoreboard += self.timer
                    self.timer = 0
                    timerlabel.config(text="Time remaining: "+str(self.timer),bg="papaya whip")
                    scorelabel.config(text="Final score: "+str(self.scoreboard),bg="papaya whip")
                    matched()                    
            
            if len(self.checker_list) == 2:
                
                if (self.checker_list[1] == 14) :                                                                                         #penalty tile code
                    my_label.config(text="Penalty Tile",bg="papaya whip")
                    tk.messagebox.showinfo("Oops!", "Penalty Tile chosen: PRESS ENTER")
                    for tile in self.checker_dict:
                        tile["text"] = " "
                        tile["image"] = ""
                    
                    self.count = 0
                    self.checker_list = []
                    self.checker_dict = {}
                    
                    self.start_time = self.start_time - 5
                    self.scoreboard -= round((120-time.monotonic()+self.start_time-5)*2,0)
                    '''if self.winner == 7:
                        self.winner += 1'''
                    if self.winner == 7:
                        self.scoreboard += self.timer
                        self.timer = 0
                        timerlabel.config(text="Time remaining: "+str(self.timer),bg="papaya whip")
                        scorelabel.config(text="Final score: "+str(self.scoreboard),bg="papaya whip")
                        matched()
                
                elif (self.checker_list[1] == 15) :                                                                                     #Bonus Tile Code
                    my_label.config(text="Bonus Tile",bg="papaya whip")
                    tk.messagebox.showinfo("Bonanza!", "Bonus Tile chosen: PRESS ENTER")
                    for tile in self.checker_dict:
                        if tile["text"] == 15:
                            tile["text"] = " "
                            tile["image"] = ""
                            tile["bg"] = "peach puff"
                            tile["state"] = "disabled"
                        else :
                            tile["text"] = " "
                            tile["image"] = "" 
            
                    self.count = 0
                    self.checker_list = []
                    self.checker_dict = {}
                    
                    self.start_time = self.start_time + 5
                    self.scoreboard += round((120-time.monotonic()+self.start_time+5)*2,0)
                    '''if self.winner == 7:
                        self.winner += 1'''
                    if self.winner == 7:
                        self.scoreboard += self.timer
                        self.timer = 0
                        timerlabel.config(text="Time remaining: "+str(self.timer),bg="papaya whip")
                        scorelabel.config(text="Final score: "+str(self.scoreboard),bg="papaya whip")
                        matched()

                elif self.imagenum_to_imagenum[self.checker_list[0]] == self.checker_list[1] :
        
                    my_label.config(text="Tile duo found!")
                    tk.messagebox.showinfo("Correct!", "Correct: PRESS ENTER")
                    for tile in self.checker_dict:
                        tile["text"] = " "
                        tile["image"] = ""
                        tile['bg'] = "peach puff"
                    for tile_num in self.checker_dict:
                        tile_num["state"] = "disabled"
                    self.count = 0
                    self.accuracy += 1
                    self.checker_list = []
                    self.checker_dict = {}
                    self.winner += 1
                    self.scoreboard += round((120-time.monotonic()+self.start_time)*2,0)
                    if self.winner == 7:
                        self.scoreboard += self.timer
                        self.timer = 0
                        timerlabel.config(text="Time remaining: "+str(self.timer),bg="papaya whip")
                        scorelabel.config(text="Final score: "+str(self.scoreboard),bg="papaya whip")
                        matched()
                
                else:
                    
                    self.count = 0
                    self.checker_list = []
                    my_label.config(text="Incorrect! Not a match!")
                    tk.messagebox.showinfo("Incorrect!", "Incorrect: PRESS ENTER")
                    for tile in self.checker_dict:
                        tile["text"] = " "
                        tile["image"] = ""
                    self.checker_dict = {}
            scorelabel.config(text="Score : "+str(self.scoreboard))
            self.timer = 120 + self.start_time - time.monotonic()
            self.timer = round(self.timer,0)
            timerlabel.config(text="Time remaining: "+str(self.timer))
            accurate=self.accuracy*200//self.tilesopened
            acclabel.config(text= "Accuracy: "+str(accurate)+"%")

        tk.Frame.__init__(self, parent, bg="papaya whip")
        self.controller = controller
        label = tk.Label(self, text="Level 2", font=controller.title_font, bg="papaya whip")
        label.grid(row=0,column=0)


        button = tk.Button(self, text="Show all tiles ",command = giveup , bg="papaya whip")
        reset = tk.Button(self,text="Reset",command=reset,bg="papaya whip")

        b0 = tk.Button(self, text=' ', font=("Georgia", 20), height=4, width=4, bg="AntiqueWhite3", command= lambda: checktime(b0, 0), relief="groove")
        b1 = tk.Button(self, text=' ', font=("Georgia", 20), height=4, width=4, bg="AntiqueWhite3", command= lambda: checktime(b1, 1), relief="groove")
        b2 = tk.Button(self, text=' ', font=("Georgia", 20), height=4, width=4, bg="AntiqueWhite3", command= lambda: checktime(b2, 2), relief="groove")
        b3 = tk.Button(self, text=' ', font=("Georgia", 20), height=4, width=4, bg="AntiqueWhite3", command= lambda: checktime(b3, 3), relief="groove")
        b4 = tk.Button(self, text=' ', font=("Georgia", 20), height=4, width=4, bg="AntiqueWhite3", command= lambda: checktime(b4, 4), relief="groove")
        b5 = tk.Button(self, text=' ', font=("Georgia", 20), height=4, width=4, bg="AntiqueWhite3", command= lambda: checktime(b5, 5), relief="groove")
        b6 = tk.Button(self, text=' ', font=("Georgia", 20), height=4, width=4, bg="AntiqueWhite3", command= lambda: checktime(b6, 6), relief="groove")
        b7 = tk.Button(self, text=' ', font=("Georgia", 20), height=4, width=4, bg="AntiqueWhite3", command= lambda: checktime(b7, 7), relief="groove")
        b8 = tk.Button(self, text=' ', font=("Georgia", 20), height=4, width=4, bg="AntiqueWhite3", command= lambda: checktime(b8, 8), relief="groove")
        b9 = tk.Button(self, text=' ', font=("Georgia", 20), height=4, width=4, bg="AntiqueWhite3", command= lambda: checktime(b9, 9), relief="groove")
        b10 = tk.Button(self, text=' ', font=("Georgia", 20), height=4, width=4, bg="AntiqueWhite3", command= lambda: checktime(b10, 10), relief="groove")
        b11 = tk.Button(self, text=' ', font=("Georgia", 20), height=4, width=4, bg="AntiqueWhite3", command= lambda: checktime(b11, 11), relief="groove")
        b12 = tk.Button(self, text=' ', font=("Georgia", 20), height=4, width=4, bg="AntiqueWhite3", command= lambda: checktime(b12, 12), relief="groove")
        b13 = tk.Button(self, text=' ', font=("Georgia", 20), height=4, width=4, bg="AntiqueWhite3", command= lambda: checktime(b13, 13), relief="groove")
        b14 = tk.Button(self, text=' ', font=("Georgia", 20), height=4, width=4, bg="AntiqueWhite3", command= lambda: checktime(b14, 14), relief="groove")
        b15 = tk.Button(self, text=' ', font=("Georgia", 20), height=4, width=4, bg="AntiqueWhite3", command= lambda: checktime(b15, 15), relief="groove")

        self.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6,7), weight=1)

        right_frame = tk.Frame(self,bg="papaya whip", width="700")

        scorelabel = tk.Label(self,font= controller.title_font, text= "Score : 0", bg= "papaya whip")
        tilelabel = tk.Label(self,font= controller.title_font, text = "No of tiles flipped : 0", bg="papaya whip")
        tilelabel.grid(row = 4, column = 4)
        scorelabel.grid(row =1, column = 4)
        timerlabel = tk.Label(self,font=controller.title_font, text = "time remaining: " +str(self.timer),bg="papaya whip")
        timerlabel.grid(row=2, column=4)
        acclabel = tk.Label(self,font = controller.title_font, text = "Accuracy: 0", bg ="papaya whip")
        acclabel.grid(row=3, column= 4)

        b0.grid(row=1, column=0, sticky='nsew')
        b1.grid(row=1, column=1, sticky='nsew')
        b2.grid(row=1, column=2, sticky='nsew')
        b3.grid(row=1, column=3, sticky='nsew')
        b4.grid(row=2, column=0, sticky='nsew')
        b5.grid(row=2, column=1, sticky='nsew')
        b6.grid(row=2, column=2, sticky='nsew')
        b7.grid(row=2, column=3, sticky='nsew')
        b8.grid(row=3, column=0, sticky='nsew')
        b9.grid(row=3, column=1, sticky='nsew')
        b10.grid(row=3, column=2, sticky='nsew')
        b11.grid(row=3, column=3, sticky='nsew')
        b12.grid(row=4, column=0, sticky='nsew')
        b13.grid(row=4, column=1, sticky='nsew')
        b14.grid(row=4, column=2, sticky='nsew')
        b15.grid(row=4, column=3, sticky='nsew')

        right_frame.grid(row=0, column=4)
        my_label = tk.Label(self, text="")
        button.grid(row=7, column=1, columnspan=2)
        reset.grid(row=7, column=3, columnspan=2)
        my_label.grid(row=6, column=1, columnspan=2)


app = InitializeGame()


app.mainloop()