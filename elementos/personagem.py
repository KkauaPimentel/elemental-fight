import pygame as pg
import os

#entidade pai que servirá  de "raiz" para os outros personagens
class Personagem:
    def __init__(self, nome="player"):
        self.tipo= "base"
        self.nome = nome
        self.ataqueBase = 15
        self.ataque = self.ataqueBase
        self.vidaBase = 250
        self.vida = self.vidaBase
        self.defesaBase = 25
        self.defesa = self.defesaBase
        self.largura = 25
        self.altura = 25
        self.cor = (255, 255, 255)
        self.rect = pg.Rect(200, 570, self.largura, self.altura)  # Usando rect para posição e tamanho
        self.vel = 20
        self.img_index = 0  # Índice para animação
        self.atc_index = 0  # Índice para animação de ataque
        self.cont_h1= 0
        self.cont_h2= 0
        self.atc_index2 = 0  # Índice para animação de ataque
        self.y = self.rect.y  # Posição Y inicial
        self.x= self.rect.x
    
    '''encontra as imagens que serão usadas e as coloca em uma lista.
    As imagens serão recortadas e usadas futuramente na função imagens(),
    que por sua vez faz as animações por frames'''
    def get_imagens(self):
        caminho= os.path.join('imagens', self.tipo)
        animacoes= ['parado.png', 'correndo.png', 'pulando.png', 'defesa.png', 'ataque.png', 'ataque2.png']
        pers_list = [pg.image.load(os.path.join(caminho, img)) for img in animacoes]

        dic_animacoes= {
            'parado':[],
            'correndo':[],
            'pulando':[],
            'defesa':[],
            'ataque':[],
            'ataque2':[]
        }

        for ind, tipo in enumerate(dic_animacoes):
            img_l = pers_list[ind].get_width()
            img_a = pers_list[ind].get_height()
            for frame in range(int(img_l / img_a)):  # Criando animações por frames
                img = pers_list[ind].subsurface(frame * img_a, 0, img_a, img_a)  # Recorte de frames
                dic_animacoes[tipo].append(pg.transform.scale(img, (img_a * 3, img_a * 3)))  # Redimensiona a imagem para o tamanho correto


        return dic_animacoes
    
    #função que fará as animações/interações do personagem de acordo com as teclas pressionadas 
    def desenhar(self, tela, oponente, mydic, opDic, opMov):
        vel= self.vel
        opVel= oponente.get_vel()

        #se nada for pressionado, só roda a animação de parado
        myself_im= mydic['parado'][self.img_index]
        self.img_index+=1
        if self.img_index>= len(mydic['parado']):
            self.img_index= 0

        op_im= opDic['parado'][oponente.img_index]
        oponente.img_index+=1
        if oponente.img_index>= len(opDic['parado']):
            oponente.img_index= 0

        tecla= pg.key.get_pressed()

        if tecla[pg.K_x]:
            pg.quit()

        if tecla[pg.K_a]:
            if self.img_index >= len(mydic['correndo']):
                self.img_index= 0
            myself_im= mydic['correndo'][self.img_index]
            self.rect.x-= vel
            if self.rect.left<0:
                self.rect.x=0
        
        if tecla[pg.K_d]:
            if self.img_index >= len(mydic['correndo']):
                self.img_index= 0
            myself_im= mydic['correndo'][self.img_index]
            self.rect.x+= vel
            if self.rect.right>tela.get_width():
                self.rect.x=tela.get_width() - 25
        
        '''if (tecla[pg.K_w] and ply==1) or (tecla[pg.K_UP] and ply==2) and self.rect.top>0:
            self.img_index=0 
            myself_im= mydic['pulando'][self.img_index]
            self.rect.y-= vel+25'''

        if tecla[pg.K_s]:
            self.img_index=0
            myself_im= mydic['defesa'][self.img_index]


        if self.atc_index != 0:
            if self.atc_index <len(mydic['ataque']):
                myself_im= mydic['ataque'][self.atc_index]
                self.atc_index+=1
            else:
                self.atc_index=0
            
        if tecla[pg.K_SPACE] and self.atc_index==0:
            self.atc_index= 1
            myself_im= mydic['ataque'][self.atc_index]

            # if self.rect.centerx < oponente.rect.centerx:
            #     ataque= pg.Rect((self.rect.right, self.rect.y, 70, 180))
            # else:
            #     ataque= pg.Rect((self.rect.left-80, self.rect.y, 70, 180))
            
            # if ataque.colliderect(oponente.rect) and oponente.atc_index== 0:
            #     oponente.vida-=self.atk()

        if self.atc_index2 != 0:
            if self.atc_index2 <len(mydic['ataque2']):
                myself_im= mydic['ataque2'][self.atc_index2]
                self.atc_index2+=1
            else:
                self.atc_index2=0
            
        if tecla[pg.K_c] and self.atc_index2== 0  and self.cont_h1<4:
            self.atc_index2=1
            self.cont_h1+=1
            myself_im= mydic['ataque2'][self.atc_index2]

            # if self.rect.centerx < oponente.rect.centerx:
            #     ataque= pg.Rect((self.rect.right, self.rect.y, 200, 180))
            # else:
            #     ataque= pg.Rect((self.rect.left-150, self.rect.y, 200, 180))
            
            # if ataque.colliderect(oponente.rect) and oponente.atc_index== 0:
            #     oponente.vida-=self.habilidade1()

        if tecla[pg.K_v] and self.cont_h2<3:
            self.habilidade2()
            self.cont_h2+=1

        if opMov =='a':
            if oponente.img_index >= len(opDic['correndo']):
                oponente.img_index= 0
            op_im= opDic['correndo'][oponente.img_index]
            oponente.rect.x-= opVel
            if oponente.rect.left>tela.get_width():
                oponente.rect.x=tela.get_width() - 25
        
        if opMov =='d':
            if oponente.img_index >= len(opDic['correndo']):
                oponente.img_index= 0
            op_im= opDic['correndo'][oponente.img_index]
            oponente.rect.x+= opVel
            if oponente.rect.right>tela.get_width():
                oponente.rect.x=tela.get_width() - 25
        
        if opMov =='s':
            if oponente.img_index >= len(opDic['defesa']):
                oponente.img_index= 0
            op_im= opDic['defesa'][oponente.img_index]
            
        '''esse trecho garante que os oersonagens irão ficar um de frente para o outro
        caso não estejam, inverte a imagem. Insere os personagens em tela com blit'''
        tela.blit(myself_im, (self.rect.x - 190, self.rect.y - 148))
        tela.blit(op_im, (oponente.rect.x - 190, oponente.rect.y - 148))
        # if self.rect.centerx> oponente.rect.centerx:
        #     myself_im= pg.transform.flip(myself_im, True, False)
        # if ply==1:
        #     tela.blit(myself_im, (self.rect.x - 190, self.rect.y - 148))
        # else:
        #     tela.blit(myself_im, (self.rect.x - 190, self.rect.y - 148))

    #função para retornar as animações em si 
    def imagens(self, dic, lista):
        for ind, tipo in enumerate(dic):#cria indices dentro do dic
            img_l = lista[ind].get_width()
            img_a = lista[ind].get_height()
            for frame in range(int(img_l / img_a)):#pega quantos e com quais frames irá trabalhar
                img = lista[ind].subsurface(frame*img_a,0,img_a,img_a)#faz o corte quadrado de acordo com o frame
                dic[tipo].append(pg.transform.scale(img, (img_a*3,img_a*3)))#redimensiona e add
        return(dic)
    
    #função futura que retornará o dano para a habilidade 1 do personagem
    def habilidade1(self):
        pass
    
    #função futura que retornará o dano para a habilidade 2 do personagem
    def habilidade2(self):
        pass    

    #função que coloca a barra de vida do personagem em tela
    def life(self, tela, vida, base, x, y):
        #cria a barra de life do personagem
        perda= vida / base
        larg, alt= 400, 30
        pg.draw.rect(tela, (70,70,90), (x-3,y-3,larg+6,alt+6))
        pg.draw.rect(tela, (255,0,0), (x,y,larg,alt))
        larg_atual= larg * perda
        pg.draw.rect(tela, (30,80,100), (x,y,larg_atual,alt))
        #insere informações do personagem na tela
        fonte= pg.font.SysFont('arial', 12)
        texto= fonte.render("Atributos: " + self.__str__(), True, (200,200,200))
        tela.blit(texto, (x, y+36))

    #função que retorna o ataque basico do personagem
    def set_atk(self, new):
        self.ataque = max(0, new)

    def set_vida(self, new):
        self.vida = max(0, new)

    def set_nome(self, new):
        self.nome = new

    def set_def(self, new):
        self.defesa = max(0, new)

    def set_imIndex(self, value):
        self.img_index= value

    def  get_vida(self):
        return self.vida
    
    def get_vel(self):
        return self.vel
    
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def get_imIndex(self):
        return self.img_index

    def atk(self):
        return self.ataque

    #retorna o quanto de dano um pesonagem pode receber
    def defense(self):
        return self.defesa

    #função usada para resetar os atributos após buffs passarem
    def reset(self):
        self.vida = self.vidaBase
        self.ataque = self.ataqueBase
        self.defesa = self.defesaBase

    #função toString
    def __str__(self):
        part1 = f"{self.nome} | Vida: {self.vida:.2f} |"
        part2 = f"Ataque: {self.ataque:.2f} | Defesa: {self.defesa:.2f}"
        return part1 + part2
    