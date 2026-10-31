"""Caminhos dos assets, independentes do diretório de onde o jogo é executado."""

from pathlib import Path

import pygame as pg

ASSETS = Path(__file__).resolve().parent.parent / "assets"


def imagem(nome: str) -> pg.Surface:
    return pg.image.load(str(ASSETS / "images" / nome))


def som(nome: str) -> str:
    return str(ASSETS / "sounds" / nome)
