import pygame as pg

pg.font.init()

#botões de interação na escolha de  usuários
class Botao:
    def __init__(self, txt, x, y, cor, cor_f):
        self.txt= txt
        self.x= x
        self.y= y
        self.cor= cor
        self.cor_f= cor_f
        self.larg= 100
        self.alt= 25
        self.rect= (x, y, self.larg, self.alt)

    def draw_B(self, tela):
        pg.draw.rect(tela, self.cor ,self.rect)
        fonte= pg.font.SysFont('arial', 18)
        texto= fonte.render(self.txt, True, (0,0,0))

        '''centraliza o texto no botão. Matemática confusa, mas básica.
        Calcula o centro do botão, depois o centro do textoo e insere
        levando isso em consideração'''
        tela.blit(texto, (self.x + round(self.larg/2) - round(texto.get_width()/2), self.y + round(self.alt/2) - round(texto.get_height()/2)))

    #pos refere-se a uma tupla com (x,y) do mouse, mostrando se foi ou não clicado
    def click(self, pos):
        x1= pos[0]
        y1= pos[1]

        if self.x <= x1 <= self.x + self.larg and self.y <= y1 <= self.y + self.alt:
            return True
        else:
            return False
        
