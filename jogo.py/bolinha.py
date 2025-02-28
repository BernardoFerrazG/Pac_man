import pygame as pg

class Bolinha:
    def __init__(self, largura, altura, cor):
        self.largura = largura
        self.altura = altura
        self.cor = cor
        self.posicoes = []
        self.sprite = pg.image.load("bolinha_amarela.png")
        self.sprite = pg.transform.scale(self.sprite, (largura *1.0, altura *1.0))

    def criar_bolinhas_em_grade(self, barreiras, extremidades, largura_mapa, altura_mapa, espacamento):
        # Define o retângulo da casinha do fantasma
        casinha_fantasma = pg.Rect(215, 170, 190, 40)  # X, Y, Largura, Altura

        # Gera posições em uma grade
        for y in range(25, altura_mapa, espacamento):
            for x in range(20, largura_mapa, espacamento):
                nova_bolinha = pg.Rect(x, y, self.largura, self.altura)

                # Verifica se a posição é válida
                if not (
                    any(nova_bolinha.colliderect(barreira) for barreira in barreiras + extremidades) or 
                    nova_bolinha.colliderect(casinha_fantasma)  # Evita a casinha do fantasma
                ):
                    self.posicoes.append((x, y))  # Adiciona a posição válida

    def desenhar_bolinhas(self, mapa):
        for x, y in self.posicoes:
            pg.draw.rect(mapa, self.cor, (x, y, self.largura, self.altura))
            mapa.blit(self.sprite, (x, y))
        



class Poder:
    def __init__(self, x, y, largura, altura, cor, tipo):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.cor = cor
        self.tipo = tipo  

    def desenhar_poder(self, mapa):
        pg.draw.rect(mapa, self.cor, (self.x, self.y, self.largura, self.altura))

    def aplicar_poder(self, pacman):
        if self.tipo == 'velocidade':
            pacman.velocidade += 0.1  # Aumenta a velocidade 
            pacman.tem_velocidade = True  # Marca que pacman pegou o poder de velocidade
            pacman.tempo_velocidade = pg.time.get_ticks()   
        elif self.tipo == 'vida':
            pacman.vidas += 1  # Aumenta a vida
            
                   
     
