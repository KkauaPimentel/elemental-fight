import pygame as pg
from elementos.personagem import Personagem

#parametros para a criação da janela do jogo
largura_t= 600
altura_t= 500

pg.init()

tela = pg.display.set_mode((largura_t, altura_t))#Cria a janela do jogo
pg.display.set_caption("Player")#Titulo da janela

num_players= 0#número de players que podem se conectar ao jogo

def redrawWindow(tela, player: Personagem):
    tela.fill((255,255,255))#define a janela com fundo branco
    player.desenhar(tela)
    pg.display.update()#atualiza a janela
     


def loop():
    run= True
    player= Personagem(x=50, y=50, altura=40, largura=40, cor=(0,255,0))

    while run:
        for evento in pg.event.get():
            if evento.type== pg.QUIT:#encerrra a janela caso a fechem
                run= False
                pg.quit()
        
        player.mov(largura_t, altura_t)
        redrawWindow(tela, player)

loop()