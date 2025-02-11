from .personagem import Personagem
import pygame as pg
import os

class Avatar(Personagem):
    def __init__(self, nome="Avatar"):
        super().__init__(nome)
        self.tipo= 'avatar'
        # self.set_nome(nome)
        self.set_vida(300)
        self.vidaBase= self.vida
        self.set_def(999)
        self.defesaBase= self.defesa
        self.set_atk(99)
        self.ataqueBase= self.ataque
        self.vel= 80
        self.atc_indexAgua= 0
        self.atc_indexAr= 0
        self.atc_indexTerra= 0

    
    def get_imagens(self):
        caminho= os.path.join('imagens', self.tipo)
        animacoes= ['parado.png', 'correndo.png', 'pulando.png',
                    'defesa.png', 'ataque.png', 'ataq_fogo.png',
                    'ataq_agua.png', 'ataq_ar.png', 'ataq_terra.png',
                    'pulando.png']
        
        pers_list = [pg.image.load(os.path.join(caminho, img)) for img in animacoes]

        dic_animacoes= {
            'parado':[],
            'correndo':[],
            'pulando':[],
            'defesa':[],
            'ataque':[],
            'fogo':[],
            'agua':[],
            'ar':[],
            'terra':[],
            'pulo':[]
        }

        for ind, tipo in enumerate(dic_animacoes):
            img_l = pers_list[ind].get_width()
            img_a = pers_list[ind].get_height()
            for frame in range(int(img_l / img_a)):  # Criando animações por frames
                img = pers_list[ind].subsurface(frame * img_a, 0, img_a, img_a)  # Recorte de frames
                dic_animacoes[tipo].append(pg.transform.scale(img, (img_a * 3, img_a * 3)))  # Redimensiona a imagem para o tamanho correto


        return dic_animacoes
    
    #mudar
    def desenhar(self, tela, mydic, oponente):
        vel= self.vel
        
        #se nada for pressionado, só roda a animação de parado
        myself_im= mydic['parado'][self.img_index]
        self.img_index+=1
        if self.img_index>= len(mydic['parado']):
            self.img_index= 0
        self.mov='p'
        #Inicia a captura de teclas pressionadas
        tecla= pg.key.get_pressed()

        #fecha a janela se x for pressionado
        if tecla[pg.K_x]:
            pg.quit()
        #Esquerda
        if tecla[pg.K_a]:
            if self.img_index >= len(mydic['correndo']):
                self.img_index= 0
            myself_im= mydic['correndo'][self.img_index]
            self.rect.x-= vel
            if self.rect.left<0:
                self.rect.x=0
            self.mov='a'
        #Direita
        if tecla[pg.K_d]:
            if self.img_index >= len(mydic['correndo']):
                self.img_index= 0
            myself_im= mydic['correndo'][self.img_index]
            self.rect.x+= vel
            if self.rect.right>tela.get_width():
                self.rect.x=tela.get_width() - 25
            self.mov='d'
        #Defesa
        if tecla[pg.K_s]:
            self.img_index=0
            myself_im= mydic['defesa'][self.img_index]
            self.mov='s'


        if self.y != self.rect.y:
            self.rect.y += 10
            if self.y - self.rect.y > 25:
                if self.img_index >= len(mydic['pulo']):
                    self.img_index = 0
                myself_im = mydic['pulo'][self.img_index]

        if tecla[pg.K_w]  and self.rect.top > 0:
            self.img_index = 0
            myself_im = mydic['pulo'][self.img_index]
            self.rect.y -= 30
            self.mov='w'


        #Ajustes para sair a animação completa do ataque
        if self.atc_index != 0:
            if self.atc_index <len(mydic['ataque']):
                myself_im= mydic['ataque'][self.atc_index]
                self.atc_index+=1
            else:
                self.atc_index=0
        #ataque normal
        if tecla[pg.K_h] and self.atc_index==0:
            self.atc_index= 1
            myself_im= mydic['ataque'][self.atc_index]
            self.mov='h'
        
        #Ajuste para sair as animações completas de habilidades
        if self.atc_index2 != 0:
            if self.atc_index2 <len(mydic['fogo']):
                myself_im= mydic['fogo'][self.atc_index2]
                self.atc_index2+=1
            else:
                self.atc_index2=0
            
        # Habilidade de fogo    
        if tecla[pg.K_LEFT] and self.atc_index2== 0:
            self.atc_index2=1
            myself_im= mydic['fogo'][self.atc_index2]
            self.mov='l'

        if self.atc_indexAgua != 0:
            if self.atc_indexAgua <len(mydic['agua']):
                myself_im= mydic['agua'][self.atc_indexAgua]
                self.atc_indexAgua+=1
            else:
                self.atc_indexAgua=0
            
        # Habilidade de agua    
        if tecla[pg.K_RIGHT] and self.atc_indexAgua== 0:
            self.atc_indexAgua=1
            myself_im= mydic['agua'][self.atc_indexAgua]
            self.mov='r'

        if self.atc_indexTerra != 0:
            if self.atc_indexTerra <len(mydic['terra']):
                myself_im= mydic['terra'][self.atc_indexTerra]
                self.atc_indexTerra+=1
            else:
                self.atc_indexTerra=0
            
        # Habilidade de terra    
        if tecla[pg.K_DOWN] and self.atc_indexTerra== 0:
            self.atc_indexTerra=1
            myself_im= mydic['terra'][self.atc_indexTerra]
            self.mov='c'

        if self.atc_indexAr != 0:
            if self.atc_indexAr <len(mydic['ar']):
                myself_im= mydic['ar'][self.atc_indexAr]
                self.atc_indexAr+=1
            else:
                self.atc_indexAr=0
            
        # Habilidade de ar    
        if tecla[pg.K_UP] and self.atc_indexAr== 0:
            self.atc_indexAr=1
            myself_im= mydic['ar'][self.atc_indexAr]
            self.mov='t'

        #habilidade2
        if tecla[pg.K_k] and self.cont_h2<1:
            self.habilidade2()
            self.mov='k'
    
        '''esse trecho garante que os oersonagens irão ficar um de frente para o outro
        caso não estejam, inverte a imagem. Insere os personagens em tela com blit'''
        if self.rect.centerx> oponente.rect.centerx:
            myself_im= pg.transform.flip(myself_im, True, False)
        

        tela.blit(myself_im, (self.rect.x - 190, self.rect.y - 148))
    

    def ataq_fogo(self):
        return self.ataque * 1.3

    def ataq_agua(self):
        return self.ataque * 1.1

    def ataq_ar(self):
        return self.ataque * 1.2

    def ataq_terra(self):
        return self.ataque * 1.05

    def habilidade2(self):
        self.set_vida(1500)
        self.set_def(1500)
        self.set_atk(999)


# boc= Avatar()
# print(boc)