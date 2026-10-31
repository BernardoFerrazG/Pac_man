import sys

import pygame as pg

from bolinha import Bolinha
from boneco import Fantasma, PacMan
from mapa import Mapa
from poder import Poder
from recursos import imagem, som

LARGURA = 755
ALTURA = 520

# Retângulo da casinha onde os fantasmas nascem
RETANGULO_X = 220
RETANGULO_Y = 170
RETANGULO_LARGURA = 180
RETANGULO_ALTURA = 35

NOMES_FANTASMAS = ["zeca", "mini", "leoncio", "arranca"]

# (instante de surgimento em ms, x, y, tipo)
PODERES = [
    (10000, 55, 224, "velocidade"),
    (20000, 337, 441, "vida"),
    (25000, 418, 258, "invencibilidade"),
]

DURACAO_INVENCIBILIDADE_MS = 5000


def tocar_musica(arquivo, loops=-1, volume=0.05):
    pg.mixer.music.load(som(arquivo))
    pg.mixer.music.set_volume(volume)
    pg.mixer.music.play(loops=loops)


def tocar_efeito(arquivo, volume):
    efeito = pg.mixer.Sound(som(arquivo))
    efeito.set_volume(volume)
    efeito.play()


def sair():
    pg.quit()
    sys.exit()


def tela_estatica(tela, arquivo_imagem, titulo, musica, loops=-1):
    """Mostra uma tela cheia até o jogador apertar Enter (fechar a janela encerra o jogo)."""
    pg.display.set_caption(titulo)
    fundo = pg.transform.scale(imagem(arquivo_imagem), (LARGURA, ALTURA))
    tocar_musica(musica, loops=loops)

    while True:
        for evento in pg.event.get():
            if evento.type == pg.QUIT:
                sair()
            if evento.type == pg.KEYDOWN and evento.key == pg.K_RETURN:
                pg.mixer.music.stop()
                return
        tela.blit(fundo, (0, 0))
        pg.display.flip()


def criar_fantasmas():
    fantasmas = []
    for i, nome in enumerate(NOMES_FANTASMAS):
        x = RETANGULO_X + (RETANGULO_LARGURA // 5) * i + 5
        y = RETANGULO_Y + RETANGULO_ALTURA // 2 - 5
        # Cada fantasma sai da casinha 2 s depois do anterior
        fantasmas.append(Fantasma(vidas=None, x=x, y=y, largura=30, altura=30, nome=nome,
                                  velocidade=0.08, tempo_para_sair=i * 2000))
    return fantasmas


def partida():
    """Roda uma partida. Retorna "vitoria", "derrota" ou "sair"."""
    mapa = Mapa(ALTURA, LARGURA)
    tela = mapa.desenhar_mapa()
    mapa.desenha_extremidades(tela)
    mapa.desenhar_barreiras_internas(tela)
    mapa.desenha_porta(tela)

    pacman = PacMan(vidas=3, x=15, y=20, largura=30, altura=30)
    fantasmas = criar_fantasmas()

    bolinha = Bolinha(10, 10, (0, 0, 0))
    bolinha.criar_bolinhas_em_grade(mapa.barreiras, mapa.extremidade, 630, 520, espacamento=25)

    poderes = []
    poderes_surgidos = set()
    inicio = pg.time.get_ticks()

    fonte = pg.font.SysFont("arial", 18, True, True)
    # O Pac-Man já nasce em cima de uma bolinha; ela não vale pontos.
    pontos = -10

    pacman.invencivel = False
    pacman.tempo_invencivel = 0

    tocar_musica("musica_jogo_2.mp3")

    while True:
        for evento in pg.event.get():
            if evento.type == pg.QUIT:
                return "sair"

        agora = pg.time.get_ticks()

        for i, (instante, x, y, tipo) in enumerate(PODERES):
            if agora - inicio >= instante and i not in poderes_surgidos:
                poderes.append(Poder(x, y, 15, 15, (0, 0, 0), tipo))
                poderes_surgidos.add(i)

        pacman.movimentar_boneco(mapa.barreiras, mapa.extremidade, mapa.porta)

        if pacman.invencivel and agora - pacman.tempo_invencivel > DURACAO_INVENCIBILIDADE_MS:
            pacman.invencivel = False

        for fantasma in fantasmas:
            if not fantasma.saiu_casinha:
                porta = [] if agora < fantasma.tempo_imunidade_porta else mapa.porta
                fantasma.sair_da_casinha(305, 150, mapa.barreiras, mapa.extremidade, porta)
            else:
                fantasma.seguir_pacman(pacman, mapa.barreiras, mapa.extremidade, mapa.porta)

        if pacman.colisao_boneco_fantasma(fantasmas):
            pacman.tem_velocidade = False
            pacman.velocidade = 0.1
            tocar_efeito("morte.mp3", 0.03)
            for fantasma in fantasmas:
                fantasma.tempo_imunidade_porta = 0
                fantasma.resetar_tempo_saida()
                fantasma.saiu_casinha = False

        if pacman.colisao_boneco_bolinhas(tela, bolinha):
            pontos += 10
            tocar_efeito("comeu_bolinha.mp3", 0.02)
            if not bolinha.posicoes:
                return "vitoria"

        if pacman.vidas == 0:
            return "derrota"

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

        tela.blit(fonte.render(f"Score: {pontos}", False, (255, 255, 255)), (645, 30))
        tela.blit(fonte.render(f"Live(s): {pacman.vidas}", False, (255, 255, 255)), (645, 70))
        pg.display.update()


def main():
    pg.init()
    pg.mixer.init()
    tela = pg.display.set_mode((LARGURA, ALTURA))

    tela_estatica(tela, "tela_nova1.png", "Pac-Man", "intro_1.mp3")

    while True:
        resultado = partida()
        pg.mixer.music.stop()
        if resultado == "sair":
            break
        if resultado == "vitoria":
            tela_estatica(tela, "tela_vitoria.png", "Vitória", "audio_vitoria.mp3", loops=1)
        else:
            tela_estatica(tela, "tela_game_over_nova.png", "Game Over", "game_over.mp3")

    pg.quit()


if __name__ == "__main__":
    main()
