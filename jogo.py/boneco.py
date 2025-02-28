import pygame as pg 
import random
import time

class Boneco:

    def __init__(self, vidas, x, y, largura, altura):
        self.vidas = vidas
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.tempo_inicial=time.time()

    def verificar_colisao_boneco_extremidade(self, extremidades):
        boneco_rect = pg.Rect(self.x, self.y, self.largura, self.altura)
        for extremidade in extremidades:
            if boneco_rect.colliderect(extremidade):
                return True
        return False

    def verificar_colisao_boneco_barreira(self, barreiras):
        boneco_rect = pg.Rect(self.x, self.y, self.largura, self.altura)
        for barreira in barreiras:
            if boneco_rect.colliderect(barreira):
                return True
        return False
    
    def verificar_colisao_boneco_porta(self, porta):
        boneco_rect = pg.Rect(self.x, self.y, self.largura, self.altura)
        for porta in porta:
            if boneco_rect.colliderect(porta):
                return True
        return False
    
    

    def desenhar_boneco(self, mapa):
        pg.draw.rect(mapa, (255,255,0), (self.x, self.y, self.largura, self.altura))
        


class PacMan(Boneco):
    def __init__(self, vidas, x , y , largura, altura):
        super().__init__(vidas, x, y, largura, altura)
        self.x = x
        self.y = y
        self.velocidade = 0.1  
        self.tem_velocidade = False  
        self.tempo_velocidade = 0
        self.invencivel = False
        self.tempo_invencivel=0
        self.pontos=0
        self.vidas = 3
        self.y_inicial = y# usado para verificar a colisao entre o pacman e fantasmas, se morrer o pacman volta para posição inicial
        self.x_inicial = x
        self.direcao = "direita"  # Direção inicial

        self.boca_aberta = True  #primeiro estado da boca
        self.ultimo_tempo_sprite = pg.time.get_ticks()  # Marca o tempo da última troca de sprite
        self.intervalo_sprite = 200  #tempo de mudança entre as sprites
        
        self.sprites = {
            "direita": [pg.image.load("boca_fechada_direita.png"), pg.image.load("boca_aberta_direita.png")],
            "esquerda": [pg.image.load("boca_fechada_esquerda.png"),pg.image.load("boca_aberta_esquerda.png")],
            "cima": [pg.image.load("boca_fechada_cima.png"), pg.image.load("boca_aberta_cima.png")],
            "baixo": [pg.image.load("boca_fechada_baixo.png"), pg.image.load("boca_aberta_baixo.png")],
}
        
        #resimensiona o tamanho das sprites com base no tamanho de retangulo
        for i in self.sprites:
            self.sprites[i] = [pg.transform.scale(img, (self.largura , self.altura)) for img in self.sprites[i]]

    def desenhar_boneco(self, mapa):
        
        # Alterna entre boca aberta e fechada a cada intervalo de tempo
        tempo_atual = pg.time.get_ticks()
        if tempo_atual - self.ultimo_tempo_sprite > self.intervalo_sprite:
            self.boca_aberta = not self.boca_aberta  # Alterna estado da boca
            self.ultimo_tempo_sprite = tempo_atual   # Atualiza o tempo de troca

        # Obtém a sprite de acordo com a direção e estado da boca
        sprite_atual = self.sprites[self.direcao][0 if self.boca_aberta else 1]
        mapa.blit(sprite_atual, (self.x, self.y))
        
    def atualizar_estado(self):
        if self.invencivel:
            tempo_atual = pg.time.get_ticks()
            if tempo_atual - self.tempo_invencivel > 5000:  # Invencibilidade dura 5 segundos
                self.invencivel = False  

    def verificar_colisao_poder(self, poderes, fantasmas):
        pacman_rect = pg.Rect(self.x, self.y, self.largura, self.altura)
        for poder in poderes:
            if pacman_rect.colliderect(pg.Rect(poder.x, poder.y, poder.largura, poder.altura)):
                poderes.remove(poder)  # Remove o poder do mapa
                if poder.tipo == 'invencibilidade':
                    self.invencivel = True
                    self.tempo_invencivel = pg.time.get_ticks()

                    # Ativar imunidade dos fantasmas à porta
                    for fantasma in fantasmas:
                        fantasma.ativar_imunidade_porta()

                else:
                    poder.aplicar_poder(self)
                return poder
        return None

    
    def colisao_boneco_bolinhas(self, mapa, bolinhas):
        pacman_rect = pg.Rect(self.x, self.y, self.largura, self.altura)

        for posicao in bolinhas.posicoes:
            bolinha_rect = pg.Rect(posicao[0], posicao[1], bolinhas.largura, bolinhas.altura)
            if pacman_rect.colliderect(bolinha_rect):
                bolinhas.posicoes.remove(posicao)
                return True
        return False
    
    def colisao_boneco_fantasma(self, lista_fantasmas):
        posicao_pacman = pg.Rect(self.x, self.y, self.largura, self.altura)

        if isinstance(lista_fantasmas, list):  # Se for uma lista, itere normalmente
            for fantasma in lista_fantasmas:
                posicao_fantasma = pg.Rect(fantasma.x, fantasma.y, fantasma.largura, fantasma.altura)

                if posicao_pacman.colliderect(posicao_fantasma):
                    if self.invencivel:
                        fantasma.x = fantasma.x_inicial  # Fantasma volta para o spawn
                        fantasma.y = fantasma.y_inicial
                        return False  # Não perde vida

                    self.vidas -= 1
                    self.x = self.x_inicial
                    self.y = self.y_inicial

                    for fantasma in lista_fantasmas:
                        fantasma.x = fantasma.x_inicial
                        fantasma.y = fantasma.y_inicial

                    return True

            return False
        
        else:
            posicao_fantasma = pg.Rect(lista_fantasmas.x, lista_fantasmas.y, lista_fantasmas.largura, lista_fantasmas.altura)

            if posicao_pacman.colliderect(posicao_fantasma):
                    if self.invencivel:
                        lista_fantasmas.x = lista_fantasmas.x_inicial  # Fantasma volta para o spawn
                        lista_fantasmas.y = lista_fantasmas.y_inicial
                        return False  # Não perde vida

                    self.vidas -= 1
                    self.x = self.x_inicial
                    self.y = self.y_inicial

                    for fantasma in lista_fantasmas:
                        fantasma.x = fantasma.x_inicial
                        fantasma.y = fantasma.y_inicial
                        
                    return True
            return False

    
    def movimentar_boneco(self, barreiras, extremidade, porta):
        pos_x_anterior = self.x
        pos_y_anterior = self.y

        # Detectar a direção com base na última tecla pressionada
        if pg.key.get_pressed()[pg.K_a] and self.direcao != "esquerda":
            self.direcao = "esquerda"
        elif pg.key.get_pressed()[pg.K_d] and self.direcao != "direita":
            self.direcao = "direita"
        elif pg.key.get_pressed()[pg.K_w] and self.direcao != "cima":
            self.direcao = "cima"
        elif pg.key.get_pressed()[pg.K_s] and self.direcao != "baixo":
            self.direcao = "baixo"

        # Mover o PacMan na direção atual
        if self.direcao == "esquerda":
            self.x -= self.velocidade
        elif self.direcao == "direita":
            self.x += self.velocidade
        elif self.direcao == "cima":
            self.y -= self.velocidade
        elif self.direcao == "baixo":
            self.y += self.velocidade

        # Verificar colisões com barreiras, extremidades ou portas
        if self.verificar_colisao_boneco_barreira(barreiras):
            self.x = pos_x_anterior
            self.y = pos_y_anterior

        if self.verificar_colisao_boneco_extremidade(extremidade):
            self.x = pos_x_anterior
            self.y = pos_y_anterior

        if self.verificar_colisao_boneco_porta(porta):
            self.x = pos_x_anterior
            self.y = pos_y_anterior

        # Reseta a velocidade após o tempo especificado
        if self.tem_velocidade and pg.time.get_ticks() - self.tempo_velocidade > 5000:
            self.velocidade = 0.1  # Restaura a velocidade original
            self.tem_velocidade = False

    


class Fantasma(Boneco):
    def __init__(self, vidas, x, y, largura, altura,nome, velocidade = 0.05, tempo_para_sair=0):
        super().__init__(vidas, x, y, largura, altura)
        self.velocidade = velocidade
        self.direcao = random.choice(['cima', 'baixo', 'esquerda', 'direita'])  # Direção inicial aleatória
        self.saiu_casinha = False  # Indica se o fantasma já saiu da casinha
        self.tempo_para_sair = tempo_para_sair  # Tempo (em ms) para começar a sair da casinha
        self.tempo_inicio = pg.time.get_ticks()  # Marca o momento da criação do fantasma
        self.x = x
        self.y = y
        self.x_inicial = x
        self.y_inicial = y
        self.vivo=True
        self.tempo_imunidade_porta = 0 
        self.imunidade_porta=False
        # Carregar imagens dinamicamente
        self.sprites = {
            direcao: pg.transform.scale(
                pg.image.load(f"{nome}_{direcao}.png"), 
                (largura , altura)
            ) 
            for direcao in ["cima", "baixo", "esquerda", "direita"]
        }

    def desenhar_boneco(self, mapa):
        """Desenha o fantasma com a sprite correspondente à direção atual."""
        mapa.blit(self.sprites[self.direcao], (self.x, self.y))
        
    
    def esta_imune_a_porta(self):
        """Verifica se o fantasma ainda está no período de imunidade à porta."""
        return pg.time.get_ticks() < self.tempo_imunidade_porta and self.imunidade_porta


    def ativar_imunidade_porta(self):
        """Ativa a imunidade dos fantasmas contra a porta, durando mais que a invencibilidade do Pac-Man."""
        self.imunidade_porta=True
        self.tempo_imunidade_porta = pg.time.get_ticks() + 10000000

    def verificar_colisao_boneco_porta(self, porta):
        """Ignora a colisão com a porta se o fantasma ainda não saiu da casinha ou estiver imune."""
        if not self.saiu_casinha or self.esta_imune_a_porta():
            return False  # Fantasma ignora a porta enquanto não saiu ou enquanto estiver imune
        return super().verificar_colisao_boneco_porta(porta)  # Verifica a colisão normalmente após o tempo acabar



    def verificar_colisao_poder(self, poderes, fantasmas):
        pacman_rect = pg.Rect(self.x, self.y, self.largura, self.altura)
        for poder in poderes:
            if pacman_rect.colliderect(pg.Rect(poder.x, poder.y, poder.largura, poder.altura)):
                poderes.remove(poder)  # Remove o poder do mapa
                if poder.tipo == 'invencibilidade':
                    self.invencivel = True
                    self.tempo_invencivel = pg.time.get_ticks()
                    

                    # Ativar imunidade dos fantasmas à porta
                    for fantasma in fantasmas:
                        fantasma.ativar_imunidade_porta()

                else:
                    poder.aplicar_poder(self)
                return poder
        return None
            
    def verificar_colisao(self, pacman):
        if self.vivo and pacman.invencivel:
            self.vivo = False  # Fantasma é "comido" por Pac-Man
            self.x = self.x_inicial  # Volta para a posição inicial
            self.y = self.y_inicial
            self.saiu_casinha = False  # Volta para a casinha
            self.tempo_inicio = None
            self.tempo_inicio = pg.time.get_ticks()  # Reseta o tempo para sair


    def seguir_pacman(self, pacman, barreiras, extremidade, porta):
        pos_x_anterior = self.x
        pos_y_anterior = self.y

        dx = pacman.x - self.x
        dy = pacman.y - self.y
        distancia = (dx**2 + dy**2)**0.5
        if distancia != 0:
            dx /= distancia
            dy /= distancia

        self.x += dx * self.velocidade #controla a força pra seguir o pacman
        self.y += dy * self.velocidade 

        if self.verificar_colisao_boneco_barreira(barreiras) or self.verificar_colisao_boneco_extremidade(extremidade) or \
            (not self.esta_imune_a_porta() and self.verificar_colisao_boneco_porta(porta)):

            self.x = pos_x_anterior
            self.y = pos_y_anterior
            self.movimentar_fantasma(barreiras, extremidade, porta)



    def chegou_na_posicao(self, alvo_x, alvo_y, tolerancia=5):
        
        return abs((self.x) - alvo_x) <= tolerancia and abs((self.y+5) - alvo_y) <= tolerancia
    
    


        
    def movimentar_fantasma(self, barreiras, extremidade, porta):
        pos_x_anterior = self.x
        pos_y_anterior = self.y

        # Movimenta-se na direção atual
        if self.direcao == 'cima':
            self.y -= 0.1
        elif self.direcao == 'baixo':
            self.y += 0.1
        elif self.direcao == 'esquerda':
            self.x -= 0.1
        elif self.direcao == 'direita':
            self.x += 0.1

        # Verifica colisão
        if self.verificar_colisao_boneco_barreira(barreiras) or self.verificar_colisao_boneco_extremidade(extremidade) or self.verificar_colisao_boneco_porta(porta):
            
            self.x = pos_x_anterior
            self.y = pos_y_anterior
    
            self.direcao = random.choice(['cima', 'baixo', 'esquerda', 'direita'])

        # Mudança de direção ocasionalmente para criar um movimento menos previsível
        if random.random() < 0.001:  # 0.1% de chance a cada frame
            self.direcao = random.choice(['cima', 'baixo', 'esquerda', 'direita'])
    

    def sair_da_casinha(self, alvo_x, alvo_y, barreiras, extremidade, porta):
        if not self.saiu_casinha:
            tempo_atual = pg.time.get_ticks()

            if self.tempo_inicio is None:
                self.tempo_inicio = tempo_atual  # Inicializa o tempo de saída

            if tempo_atual - self.tempo_inicio >= self.tempo_para_sair:
                pos_x_anterior = self.x
                pos_y_anterior = self.y

                # Calcula a direção para sair da casinha
                dx = alvo_x - self.x
                dy = alvo_y - self.y
                distancia = (dx**2 + dy**2)**0.5
                if distancia != 0:
                    dx /= distancia
                    dy /= distancia

                self.x += dx * self.velocidade
                self.y += dy * self.velocidade

                # O fantasma IGNORA a porta enquanto não saiu da casinha
                if self.verificar_colisao_boneco_barreira(barreiras) or self.verificar_colisao_boneco_extremidade(extremidade) or \
                    (not self.saiu_casinha and self.verificar_colisao_boneco_porta(porta)):

                    self.x = pos_x_anterior
                    self.y = pos_y_anterior
                    self.movimentar_fantasma(barreiras, extremidade, porta)  # Movimenta aleatoriamente para não ficar preso

                if self.chegou_na_posicao(alvo_x, alvo_y):
                    self.saiu_casinha = True  # Agora ele pode colidir com a porta normalmente
                    self.tempo_inicio = None



    def resetar_tempo_saida(self):
        """ Reinicia a contagem do tempo para sair da casinha. """
        self.tempo_inicio = None