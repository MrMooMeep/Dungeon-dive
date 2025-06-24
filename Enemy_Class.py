import pygame
import sys

RED = (255,0,0)
Enemy_Img= pygame.image.load("Enemy.png")

class Enemy:
    def __init__(self,HP,SP,ATK,DEF,GOLD,x,y,cooldown=3,SKILLCOST=25, Special_Damage=15, Basic_Dmg= 10): #GOLD is like how much the enemy would drop when defeated
        self.HP = HP
        self.SP = SP
        self.ATK = ATK
        self.DEF = DEF
        self.GOLD = GOLD
        self.x = x
        self.y = y
        self.cooldown = cooldown
        self.counter_cooldown = 0
        self.SKILLCOST = SKILLCOST
        self.Special_Damage = Special_Damage
        self.Basic_Dmg = Basic_Dmg
    
    def draw(self,win):
        win.blit(Enemy_Img,(self.x,self.y),) #image,position,size?
    
    def can_use_special(self):
        if self.SP >= self.SKILLCOST and self.counter_cooldown <= 0:
            self.use_special # run line 26-29 whne conditions are viable
    
    def use_special(self):
        self.counter_cooldown = self.cooldown
        self.SP -= self.SKILLCOST
        return (self.Special_Damage * self.ATK)  # damage dealt
    
    def use_basic_atk(self):
        return (self.Basic_Dmg * self.ATK)
    
    def damage_intake(self,incoming_dmg):
        self.HP - (incoming_dmg - self.DEF)
    
    def is_dead(self):
        if self.HP <= 0:
            return True
        else:
            return False

