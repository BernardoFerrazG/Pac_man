import pygame as pg

LARGURA = 755
ALTURA = 520

class Mapa:

    def __init__(self, altura, largura):

        self.altura = altura
        self.largura = largura
        self.barreiras = []
        self.extremidade = []
        self.porta=[]
        self.bolinhas=[]
        self.sprite_barreira = pg.image.load("barreira2.png").convert_alpha()
        self.sprite_extremidade = pg.image.load("extremidade.png").convert_alpha()  #carrega a sprite
        self.sprite_barreira = pg.transform.scale(self.sprite_barreira, (50, 30))
        self.sprite_extremidade = pg.transform.scale(self.sprite_extremidade, (100, 30))  #redimensiona o tamanho
    def desenhar_mapa(self):

        mapa = pg.display.set_mode((LARGURA, ALTURA))
        pg.display.set_caption('Pac - Man ')

        return mapa

    def desenha_extremidades(self, mapa):
        self.extremidade = [
            pg.draw.rect(mapa, (0, 0, 255), (0, 0, 15, 505)),
            pg.draw.rect(mapa, (0, 0, 255), (0, 0, 630, 15)),
            pg.draw.rect(mapa, (0, 0, 255), (620, 0, 15, 505)),#
            pg.draw.rect(mapa, (0, 0, 255), (0, 505, 635, 15)),
        ]
        for x, y, largura, altura in self.extremidade:
            sprite = pg.transform.scale(self.sprite_extremidade, (largura, altura))  # Ajusta a sprite ao tamanho da barreira
            mapa.blit(sprite, (x, y))

    def desenha_porta(self, mapa):
        self.porta=[
            pg.draw.rect(mapa, (0, 0, 0), (275, 180, 80 ,5))#
        ]

    def desenhar_barreiras_internas(self, mapa):
        
        self.barreiras =[
            #casinha dos fantasmas
            pg.draw.rect(mapa, (0, 0, 255), (220, 215, 180, 5)),#*
            pg.draw.rect(mapa, (0, 0, 255), (220, 175, 55, 5)),#*
            pg.draw.rect(mapa, (0, 0, 255), (355, 175, 50, 5)),#*
            pg.draw.rect(mapa, (0, 0, 255), (220, 175, 5, 40)),#*
            pg.draw.rect(mapa, (0, 0, 255), (400, 180, 5, 40)),#*

            pg.draw.rect(mapa, (0,255, 255), (45,50, 85, 20)),#*
            pg.draw.rect(mapa, (0,0, 255), (173,50, 85, 20)),#*
            
            pg.draw.rect(mapa, (255,0, 255), (45, 105, 215, 30)),#*
            pg.draw.rect(mapa, (255,0, 255), (370, 105, 215, 30)),#*

            pg.draw.rect(mapa, (0,255, 255), (500,50, 85, 20)),#*
            pg.draw.rect(mapa, (0,0, 255), (370,50, 85, 20)),#*
            
            pg.draw.rect(mapa, (255,255, 255), (45, 175, 135, 45)),#*
            pg.draw.rect(mapa, (255,255, 255), (450, 175, 135, 45)),#*
            ####################^^parte de cima
            
            pg.draw.rect(mapa, (255,255, 255), (15, 255, 170, 30)),#*
            pg.draw.rect(mapa, (255,255, 255), (450, 255, 170, 30)),#*
            pg.draw.rect(mapa, (0,0, 255), (225, 255, 180, 30)),#*
            ##################^^^parte do meio
            pg.draw.rect(mapa, (255,255, 255), (295, 15, 35, 120)),#*
            
            pg.draw.rect(mapa, (0,255, 255), (295, 375, 35, 130)),#*

            pg.draw.rect(mapa, (255,0, 255), (175, 320, 280, 20)),#*
            pg.draw.rect(mapa, (0,255, 255), (45,320, 85, 20)),#*
            pg.draw.rect(mapa, (0,255, 255), (500,320, 85, 20)),#*
            
            
            
            pg.draw.rect(mapa, (255,255, 255), (175,375, 280, 30)),#*
            pg.draw.rect(mapa, (0,255, 255), (45,375, 85, 30)),#*
            pg.draw.rect(mapa, (0,255, 255), (500,375, 85, 30)),#*
            
            pg.draw.rect(mapa, (225,255, 255), (45,440, 210, 30)),#*
            pg.draw.rect(mapa, (225,255, 255), (375,440, 210, 30)),#*
        ]
        for x, y, largura, altura in self.barreiras:
            sprite = pg.transform.scale(self.sprite_barreira, (largura, altura))  #redimensiona a sprite com o tamanho da barreira
            mapa.blit(sprite, (x, y))
        
