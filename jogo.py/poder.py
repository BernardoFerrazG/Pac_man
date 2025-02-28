import pygame as pg

class Poder:
    def __init__(self, x, y, largura, altura, cor, tipo):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.cor = cor
        self.tipo = tipo 
        self.sprite = None  

        
        if tipo == "velocidade":
            self.sprite = pg.image.load("raio.png")  
            self.sprite = pg.transform.scale(self.sprite, (int(largura * 2.0), int(altura * 2.0))) 

        elif tipo == "vida":
            self.sprite = pg.image.load("coracao.png")  
            self.sprite = pg.transform.scale(self.sprite, (int(largura * 1.8), int(altura * 1.8)))

        elif tipo == "invencibilidade":
            self.sprite = pg.image.load("pacman.png")
            self.sprite = pg.transform.scale(self.sprite, (int(largura * 1.3), int(altura * 1.3)))

    def desenhar_poder(self, mapa):
        pg.draw.rect(mapa, self.cor, (self.x, self.y, self.largura, self.altura))  
        if self.sprite:  
            mapa.blit(self.sprite, (self.x, self.y))

    def aplicar_poder(self, pacman):
        if self.tipo == 'velocidade':
            pacman.velocidade += 0.05  
            pacman.tem_velocidade = True  
            pacman.tempo_velocidade = pg.time.get_ticks() 
              
        elif self.tipo == 'vida':
            pacman.vidas += 1  
            
        elif self.tipo == 'invencibilidade':
            pacman.invencivel = True  
            pacman.tempo_invencivel = pg.time.get_ticks()  

     