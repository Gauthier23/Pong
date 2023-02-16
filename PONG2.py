# -*- coding: utf-8 -*-
"""
Created on Sat Feb 11 20:09:42 2023

@author: gauth
"""

import tkinter as tk
import random
from math import*

class PongGame(tk.Tk):
    def __init__(self, *args, **kwargs):
        ###---Fenêtre de base---###
        tk.Tk.__init__(self)
        self.resizable(False, False)    #empêcher le changement de géométrie
        self.title("PONG")              #titre fenêtre
        
        ###---Proportions du canevas principal---###
        self.coef = 1.5
        self.WIDTH = 650*self.coef
        self.HEIGHT = 480*self.coef
        
        ###---Graphismes statiques---###
        self.canvas = tk.Canvas(self, width=self.WIDTH, height=self.HEIGHT, bg="black")
        self.canvas.pack()
        
        self.canvas.create_line(self.WIDTH/2, 0, self.WIDTH/2, self.HEIGHT, dash = 5, fill = "white")
        
        ###---Graphismes interactifs---###
        self.ball = self.canvas.create_rectangle(self.WIDTH/2 - 5, self.HEIGHT/2 - 5, self.WIDTH/2 + 5, self.HEIGHT/2 + 5, fill="white")
        self.paddle_left = self.canvas.create_rectangle(10, self.HEIGHT/2 - 40, 20, self.HEIGHT/2 + 40, fill="white")
        self.paddle_right = self.canvas.create_rectangle(self.WIDTH - 20, self.HEIGHT/2 - 40, self.WIDTH - 10, self.HEIGHT/2 + 40, fill="white")

        ##--Score--##
        self.left_score = 0
        self.right_score = 0
        self.left_score_text = self.canvas.create_text(self.WIDTH/4, 30, text=f"Score : {self.left_score}", fill="white", font=("ArcadeClassic", 40))
        self.right_score_text = self.canvas.create_text(3*self.WIDTH/4, 30, text=f"Score : {self.right_score}", fill="white", font=("ArcadeClassic", 40))
        
        ###---Touches interactives---###
        self.numberofplayer = None
               
        
        
        
        
        
        self.canvas.focus_set()
        
        ###---Déplacement balle---###
        self.alpha = random.randint(20,160)
        self.speed = 5
        self.y_speed = -cos(self.alpha)*self.speed
        self.x_speed = sqrt(self.speed**2-self.y_speed)
        
        
        
        
        
        self.etat = "actif"
        
        #self.HEIGHT/2self.WIDTH
        #width = 30, height = 80,
        #self.canvas.create_window(0, 0, window=self.button1)
        
        
        #self.button1.place(x = 0, y = 0)

        self.intro()

        
    def intro(self):
        self.button1 = tk.Button(self, text="1 PLAYER", bg="black", fg="white", bd=0, font="ArcadeClassic",  command = self.oneplayer)
        self.button1.pack(side = tk.LEFT, expand=True, fill="both")
        
        self.button2 = tk.Button(self, text="2 PLAYERS", bg="black", fg="white", bd=0, font="ArcadeClassic", command = self.twoplayers)
        self.button2.pack(side = tk.RIGHT, expand=True, fill="both")
        
        
    def oneplayer(self):
        self.numberofplayer = 1
        self.canvas.bind_all("<KeyPress-w>", self.move_up_right)        
        self.canvas.bind_all("<KeyPress-s>", self.move_down_right)
        self.play()
        
    def twoplayers(self):
        self.numberofplayer = 2
        self.canvas.bind_all("<KeyPress-Up>", self.move_up_left)        
        self.canvas.bind_all("<KeyPress-Down>", self.move_down_left)
        self.play()
        
        
    def initialise(self):
        
        self.canvas.coords(self.ball, self.WIDTH/2 - 5, self.HEIGHT/2 - 5, self.WIDTH/2 + 5, self.HEIGHT/2 + 5)
        self.canvas.coords(self.paddle_left, 10, self.HEIGHT/2 - 40, 20, self.HEIGHT/2 + 40)
        self.canvas.coords(self.paddle_right, self.WIDTH - 20, self.HEIGHT/2 - 40, self.WIDTH - 10, self.HEIGHT/2 + 40)
        
        ###---Déplacement balle---###
        self.alpha = random.choice(list(range(20,70+1))+list(range(100,160+1)))
            
        self.speed = 5
        self.y_speed = -cos(self.alpha)*self.speed
        self.x_speed = sqrt(self.speed**2-self.y_speed)
        
        self.etat = "actif"

        
    def move_up_left(self, event):
        y = self.canvas.coords(self.paddle_left)[1]
        if y > 0:
            self.canvas.move(self.paddle_left, 0, -10)
        
    def move_down_left(self, event):
        y = self.canvas.coords(self.paddle_left)[1]
        if y < self.HEIGHT - 80:
            self.canvas.move(self.paddle_left, 0, +10)
        
    def move_up_right(self, event):
        y = self.canvas.coords(self.paddle_right)[1]
        if y > 0:
            self.canvas.move(self.paddle_right, 0, -10)
        
    def move_down_right(self, event):
        y = self.canvas.coords(self.paddle_right)[1]
        if y < self.HEIGHT - 80:
            self.canvas.move(self.paddle_right, 0, +10)


    def play(self):
        
        time = 25 #(ms)
        #ball_x = random.uniform(-5,5)
        #ball_y = random.uniform(-5,5)
        while self.etat == "actif":
            self.canvas.move(self.ball, self.x_speed, self.y_speed)
            pos = self.canvas.coords(self.ball)
            
            ###---Mur supérieur et inférieur---###
            if pos[1] <= 0:             #Y1#
                self.y_speed = -self.y_speed
                
            if pos[3] >= self.HEIGHT:   #Y2#
                self.y_speed = -self.y_speed
                
            ###---Interactions palettes et balle---###
            
            ##--Palette gauche--##
            if 10 <= pos[0] <= 20 and self.canvas.coords(self.paddle_left)[3] + 10 > pos[1] > self.canvas.coords(self.paddle_left)[3] - 90:
                #-Reprise du point de contact (0-100)-#
                contact = pos[1] - (self.canvas.coords(self.paddle_left)[3] - 90)   #attention, parenthèses obligatoires -> "x-y-z =! x-(y-z)"
                
                
                self.x_speed = -self.x_speed*1.1
                self.y_speed = self.y_speed*1.1
                
            if self.WIDTH - 20 <= pos[2] <= self.WIDTH - 10 and self.canvas.coords(self.paddle_right)[1] - 10 < pos[3] < self.canvas.coords(self.paddle_right)[1] + 90:
                #-Reprise du point de contact-#
                
                
               self.x_speed = -self.x_speed*1.1
               self.y_speed = self.y_speed*1.1
                
            ###---Balle en contact avec murs côtés---###
            ##--Gauche--##
            if pos[2] < -20:
                self.right_score += 1
                self.canvas.itemconfig(self.right_score_text, text=f"Score : {self.right_score}")
                self.etat = "arret"
                self.initialise()
              
            ##--Droite--##
            if pos[0] > self.WIDTH + 20:
                self.left_score += 1
                self.canvas.itemconfig(self.left_score_text, text=f"Score : {self.left_score}")
                self.etat = "arret"
                self.initialise()
                
            #if self.numberofplayer == 1:
            if self.numberofplayer == 1:    
            #botposition = self.canvas.coords(self.paddle_left)[1] - 45
                botposition = self.canvas.coords(self.paddle_left)
            
            #if 0 < botposition[1] < self.HEIGHT - 80 and 1 == 2:
                #print(botposition[1])
                
                if botposition[1] + 30 > pos[1]:
                    self.canvas.move(self.paddle_left, 0, -7)
                    
                if botposition[1] + 60 < pos[1]:
                    self.canvas.move(self.paddle_left, 0, +7)
               
            
            #self.canvas.coords(self.paddle_left, 10, pos[1]-40, 20, pos[1] + 50)
            #self.canvas.coords(self.paddle_right, self.WIDTH - 20, pos[1]-40, self.WIDTH - 10, pos[1] + 50)
            
            
            
            #self.canvas.coords(self., self.WIDTH/2 - 5, self.HEIGHT/2 - 5, self.WIDTH/2 + 5, self.HEIGHT/2 + 5)
                
            
            if self.etat == "actif":
                self.after(int(time), self.update())
        
if __name__ == "__main__":
    #intro()
    game = PongGame()
    #game.after(1000, game.play)
    game.mainloop()
    
#def