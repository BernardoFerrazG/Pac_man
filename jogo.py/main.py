import pygame as pg
import sys
from mapa import Mapa
from bolinha import Bolinha
from poder import Poder
from boneco import PacMan, Fantasma


LARGURA = 755
ALTURA = 520

# Coordenadas do retângulo para spawn dos fantasmas
RETANGULO_X = 220
RETANGULO_Y = 170
RETANGULO_LARGURA = 180
RETANGULO_ALTURA = 35

def musica_abertura():

    pg.mixer.init() #inicializa o audio
    pg.mixer.music.load("intro_1.mp3") #carrega a musica de um arquivo
    pg.mixer.music.set_volume(0.05) #define o volume 
    pg.mixer.music.play(loops = - 1) # loops = -1 significa que a musica via reiniciar toda vez

def musica_gameover():

    pg.mixer.init() #inicializa o audio
    pg.mixer.music.load("game_over.mp3") #carrega a musica de um arquivo
    pg.mixer.music.set_volume(0.05) #define o volume 
    pg.mixer.music.play(loops = - 1) # loops = -1 significa que a musica via reiniciar toda vez

def musica_vitoria():

    pg.mixer.init() #inicializa o audio
    pg.mixer.music.load("audio_vitoria.mp3") #carrega a musica de um arquivo
    pg.mixer.music.set_volume(0.05) #define o volume 
    pg.mixer.music.play(loops = 1) # loops = -1 significa que a musica via reiniciar toda vez


def musica_jogo():

    pg.mixer.init() #inicializa o audio
    pg.mixer.music.load("musica_jogo_2.mp3") #carrega a musica de um arquivo
    pg.mixer.music.set_volume(0.05) #define o volume 
    pg.mixer.music.play(loops = - 1) # loops = -1 significa que a musica via reiniciar toda vez


def comeu_bolinha():

    efeito_sonoro = pg.mixer.Sound("comeu_bolinha.mp3")
    efeito_sonoro.set_volume(0.02)
    efeito_sonoro.play()

def morreu():

    efeito_sonoro = pg.mixer.Sound("morte.mp3")
    efeito_sonoro.set_volume(0.03)
    efeito_sonoro.play()
    
    

def tela_inicial():
    
    pg.init()

    
    
    tela = pg.display.set_mode((LARGURA, ALTURA))
    pg.display.set_caption("Tela Inicial do Jogo")

    
      

    
    fonte = pg.font.Font(pg.font.get_default_font(), 36)

    # Mensagem
    

    # Carregar imagem de fundo
    imagem_fundo = pg.image.load("tela_nova1.png")
    imagem_fundo = pg.transform.scale(imagem_fundo, (LARGURA, ALTURA)) #aqui a imagem é redimensionada, por exemplo, se pegar uma imagem muito pequena, ela será redimensionada para caber certinho na janela do jogo
    
    musica_abertura()
    # loop da tela inicial
    rodando_tela_inicial = True
    while rodando_tela_inicial:
        for evento in pg.event.get():
            if evento.type == pg.QUIT:
                pg.quit()
                sys.exit() #interrompe a execução do programa de fato, pois a linha anterior não faz isso, apenas fecha a janela

            if evento.type == pg.KEYDOWN: #usado para verificar se alguma tecla foi pressionada
                if evento.key == pg.K_RETURN:  # tecla Enter
                    rodando_tela_inicial = False # o jogo começa

        # desenhar a tela
        tela.blit(imagem_fundo, (0, 0)) #desenha a tela de fato e em qual posição, testem a posição 10, 10 para ver o comportamento
        

        #atualiza a tela, poderia usar update, que apesar de ter melhor desempenho, o flip é mais simples de implementar e recomendado para tela inicial
        pg.display.flip()

    pg.mixer.music.stop() #a musica para quando sair da tela inical
    
def tela_vitoria():
    pg.init()
    
    tela = pg.display.set_mode((LARGURA, ALTURA))
    pg.display.set_caption("Vitória")
    
    imagem_fundo = pg.image.load("tela_vitoria.png")
    imagem_fundo = pg.transform.scale(imagem_fundo, (LARGURA, ALTURA))
    
    musica_vitoria()
    
    rodando_tela_vitoria = True
    while rodando_tela_vitoria:
        for evento in pg.event.get():
            if evento.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if evento.type == pg.KEYDOWN:
                if evento.key == pg.K_RETURN:
                    print("Saindo da tela de vitória!")  # Debug
                    rodando_tela_vitoria = False  
                    reinicia_jogo()

        tela.blit(imagem_fundo, (0, 0))
        pg.display.flip()

    pg.mixer.music.stop()


def tela_game_over():
    pg.init()
    
    tela = pg.display.set_mode((LARGURA, ALTURA))
    pg.display.set_caption("Game Over")
    
    imagem_fundo = pg.image.load("tela_game_over_nova.png")
    imagem_fundo = pg.transform.scale(imagem_fundo, (LARGURA, ALTURA))
    
    musica_gameover()
    
    rodando_tela_game_over = True
    while rodando_tela_game_over:
        for evento in pg.event.get():
            if evento.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if evento.type == pg.KEYDOWN:
                if evento.key == pg.K_RETURN:  # Se pressionar Enter, reinicia o jogo
                    rodando_tela_game_over = False  
                    reinicia_jogo()  # Reinicia o jogo ao sair da tela Game Over

        tela.blit(imagem_fundo, (0, 0))
        pg.display.flip()

    pg.mixer.music.stop()



def reinicia_jogo():
    # Inicializar o mapa
    mapa = Mapa(ALTURA, LARGURA)
    tela = mapa.desenhar_mapa()
    mapa.desenha_extremidades(tela)
    mapa.desenhar_barreiras_internas(tela)
    mapa.desenha_porta(tela)
    
    # Inicializar Pac-Man e Fantasma
    pacman = PacMan(vidas=3, x=15, y=20, largura=30, altura=30)  # Ajuste a posição inicial
    
    # Lista de personagens disponíveis
    nomes_fantasmas = ["zeca", "mini", "leoncio", "arranca"]

    fantasmas = []
    for i, nome_fantasma in enumerate(nomes_fantasmas):
        x_fantasma = RETANGULO_X + (RETANGULO_LARGURA // 5) * i + 5
        y_fantasma = RETANGULO_Y + RETANGULO_ALTURA // 2 - 5
        tempo_para_sair = i * 2000  # Cada fantasma sai com um intervalo de 2s
        fantasmas.append(Fantasma(vidas=None, x=x_fantasma, y=y_fantasma, largura=30, altura=30, nome=nome_fantasma, velocidade=0.08, tempo_para_sair=tempo_para_sair))

    # Inicializar Bolinhas
    bolinha = Bolinha(10, 10, (0, 0, 0))
    bolinha.criar_bolinhas_em_grade(mapa.barreiras, mapa.extremidade, 630, 520, espacamento=25)

    # Inicializar Poderes com tempos diferentes e locais predeterminados
    poderes = []
    tempos_poderes = [10000, 20000, 25000]
    poderes_tipos = [
        (55, 224, 'velocidade', (0, 0, 0)),
        (337, 441, 'vida', (0, 0, 0)),
        (418, 258, 'invencibilidade', (0, 0, 0))
    ]
    poderes_ativos = []
    tempo_inicial_poderes = pg.time.get_ticks()
    
    fonte = pg.font.SysFont('arial', 18, True, True)
    pontos = -10
    
    pacman.invencivel = False
    pacman.tempo_invencivel = 0
    pacman.velocidade_extra = False  
    estado_fantasma = True  
    tempo_inicial = pg.time.get_ticks()  
    
    musica_jogo()
    
    rodando = True
    while rodando:
        for evento in pg.event.get():
            if evento.type == pg.QUIT:
                rodando = False

        tempo_atual = pg.time.get_ticks()
        
        for i, tempo_poder in enumerate(tempos_poderes):
            if tempo_atual - tempo_inicial_poderes >= tempo_poder and i not in poderes_ativos:
                x, y, tipo, cor = poderes_tipos[i]
                poderes.append(Poder(x, y, 15, 15, cor, tipo))
                poderes_ativos.append(i)
        
        pacman.movimentar_boneco(mapa.barreiras, mapa.extremidade, mapa.porta)
        
        for poder in poderes:
            if (pacman.x in range(poder.x, poder.x + poder.largura) and 
                pacman.y in range(poder.y, poder.y + poder.altura)):
                if poder.tipo == 'invencibilidade':
                    pacman.invencivel = True
                    pacman.tempo_invencivel = pg.time.get_ticks()
                elif poder.tipo == 'velocidade':
                    pacman.velocidade_extra = True  
                else:
                    poder.aplicar_poder(pacman)
        
        if pacman.invencivel and (tempo_atual - pacman.tempo_invencivel > 5000):
            pacman.invencivel = False 
        
        for fantasma in fantasmas:
            if not fantasma.saiu_casinha:
                if pg.time.get_ticks() < fantasma.tempo_imunidade_porta:
                    fantasma.sair_da_casinha(305, 150, mapa.barreiras, mapa.extremidade, [])
                else:
                    fantasma.sair_da_casinha(305, 150, mapa.barreiras, mapa.extremidade, mapa.porta)
            else:
                if estado_fantasma:
                    fantasma.seguir_pacman(pacman, mapa.barreiras, mapa.extremidade, mapa.porta)
                else:
                    fantasma.movimentar_fantasma(mapa.barreiras, mapa.extremidade, mapa.porta)
        
        if pacman.colisao_boneco_fantasma(fantasmas):
            pacman.velocidade_extra = False  
            pacman.tem_velocidade = False  
            pacman.velocidade = 0.1  
            morreu()
            
            for fantasma in fantasmas:
                fantasma.tempo_imunidade_porta = 0
                fantasma.resetar_tempo_saida()
                fantasma.saiu_casinha = False  
        
        if pacman.colisao_boneco_bolinhas(tela, bolinha):
            pontos += 10
            comeu_bolinha()
            
            if pontos>2240:
                tela_vitoria()
                return
        
        if pacman.vidas == 0:
            tela_game_over()
        
        
            return

        pacman.verificar_colisao_poder(poderes, fantasmas)

        tela.fill((0, 0, 0))  
        mapa.desenha_extremidades(tela)
        mapa.desenhar_barreiras_internas(tela)
        mapa.desenha_porta(tela)

        bolinha.desenhar_bolinhas(tela)  
        pacman.desenhar_boneco(tela)    

        for fantasma in fantasmas:
            fantasma.desenhar_boneco(tela)

        for poder in poderes:
            poder.desenhar_poder(tela)  
        
        mensagem = f"Score: {pontos}"
        vida = f"Live(s): {pacman.vidas}"
        
        texto_formatado = fonte.render(mensagem, False, (255,255,255))
        
        vidas_formatadas = fonte.render(vida, False, (255, 255, 255))
        tela.blit(texto_formatado, (645, 30))
        
        tela.blit(vidas_formatadas, (645, 70))

        pg.display.update()

    pg.mixer.music.stop()
    pg.quit()



def main():
    pg.init()

    tela_inicial()
    reinicia_jogo()


if __name__ == "__main__":
    main()