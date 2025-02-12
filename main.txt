import pygame as pg
from elementos.water import Agua# Verifique se o caminho está correto
from elementos.fire import Fogo
from elementos.earth import Terra
from elementos.air import Ar
from elementos.wood import Madeira


import os

pg.init()

# Configurações da tela
largura_t, altura_t = 1000, 680
tela = pg.display.set_mode((largura_t, altura_t))
pg.display.set_caption("Elemental Fight")

# Carrega o fundo
imagem_fundo = pg.image.load(os.path.join("imagens", "fundo-x1.jpg"))

clock = pg.time.Clock()
FPS = 30

def desenhar_fundo():
    fundo_ajustado = pg.transform.scale(imagem_fundo, (largura_t, altura_t))
    tela.blit(fundo_ajustado, (0, 0))

# Criação dos personagens do tipo Água
personagem1 = Agua("Água 1")
personagem2 = Terra("Água 2")
personagem3 = Fogo("Água 2")
personagem4 = Ar("Água 2")
# personagem5 = Madeira("Água 2")

# Ajuste das posições iniciais
personagem1.rect.x = 100
personagem1.rect.y = 570

personagem2.rect.x = 800
personagem2.rect.y = 570

# Carrega as animações para cada personagem utilizando os métodos da classe base
dic_anim1 = personagem1.get_imagens()

dic_anim2 = personagem2.get_imagens()

run = True
while run:
    clock.tick(FPS)
    desenhar_fundo()
    
    # Exibe as barras de vida e os atributos
    personagem1.life(tela, personagem1.vida, personagem1.vidaBase, 20, 20)
    personagem2.life(tela, personagem2.vida, personagem2.vidaBase, 550, 20)
    
    # Desenha os personagens na tela
    # Parâmetros:
    # - tela
    # - ply: 1 para o primeiro personagem, 2 para o segundo
    # - oponente: para verificação de colisão no ataque
    # - dicionário de animações carregado
    personagem1.desenhar(tela, 1, personagem2, dic_anim1)
    personagem2.desenhar(tela, 2, personagem1, dic_anim2)
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    pg.display.update()

pg.quit()
