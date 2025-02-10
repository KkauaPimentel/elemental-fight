import pygame as pg
import os
from botao import Botao
import socket
import pickle as pk

#---conexão com o servidor---
IP, port= "0.0.0.0", 8000

client= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, port))

#parametros para a criação da janela do jogo
tela_larg, tela_alt= 1000, 640
tela_atual= 'espera'
#para uso posterior de fontes
pg.font.init()
#criação da tela
tela = pg.display.set_mode((tela_larg, tela_alt))#Cria a janela do jogo
pg.display.set_caption("Client")#Titulo da janela
#imagens dos fundos
img_fundo= pg.image.load(os.path.join('imagens', 'fundo-x1.jpg')) 
img_selec= pg.image.load(os.path.join('imagens', 'fundo-tela.jpg')) 
#variáveis globais para definição de jogo
nome=''
select= None
host= None
#botões de escolha dos tipos
botoes = [
    Botao("water", 250, 200, (255,255,255), (0,0,0)),
    Botao("earth", 450, 200, (255,255,255), (0,0,0)),
    Botao("fire", 650, 200, (255,255,255), (0,0,0)),
    Botao("air", 350, 350, (255,255,255), (0,0,0)),
    Botao("wood", 550, 350, (255,255,255), (0,0,0))
]

#inserção das imagens de fundo de acordo com a imagem passada
def background(img):
    img_ajust= pg.transform.scale(img, (tela_larg, tela_alt))
    tela.blit(img_ajust, (0,0))

#tela de espera
def tela_espera():
    #insere fundo de selec
    background(img_selec)
    #fontes do txt
    fonte1= pg.font.SysFont('comicsans', 65)
    fonte2= pg.font.SysFont('comicsans', 63)
    #texto em si
    texto= fonte1.render("Esperando oponente...", True, (0,0,0))
    texto2= fonte2.render("Esperando oponente...", True, (255,255,255))
    #inserção do txt
    tela.blit(texto, (tela_larg/2 - texto.get_width()/2, tela_alt/2 - texto.get_height()/2))
    tela.blit(texto2, (tela_larg/2 - texto2.get_width()/2, tela_alt/2 - texto2.get_height()/2))
    #atualização da tela
    pg.display.update()

#tela de seleção
def tela_selecao():

    background(img_selec)

    fonte= pg.font.SysFont('arial', 35)
    fonte_name= pg.font.SysFont('arial', 24)
    texto= fonte.render("Digite seu nome: *", True, (255,255,255))
    #insere o texto
    tela.blit(texto, (340, 50))
    #caixa que armazena o nome
    pg.draw.rect(tela, (0,0,0), (327, 95, 316, 50))
    pg.draw.rect(tela, (200,200,200), (337, 100, 300, 40))
    #exibição do nome digitado
    nome_limite = nome[:12]
    txt_nome= fonte_name.render(nome_limite, True, (0,0,0), (0,255,0))
    tela.blit(txt_nome, (342, 107, 300, 40))
    #criação dos botões em tela
    for bot in botoes:
        bot.draw_B(tela)
    #exibe que personagem você selecionou
    if select:
        msg = f"Elemento selecionado: {select.capitalize()}"
        txt_selec = fonte.render(msg, True, (255, 255, 255))
        tela.blit(txt_selec, (tela_larg/2 - txt_selec.get_width()/2, tela_alt - 100))

    pg.display.update()

#tela de x1
def tela_combat(oponente):
    global host
    #insere o a imagem de fundo de x1
    background(img_fundo)
    #insere a vida atual do host/oponente
    host.life(tela, host.vida, host.vidaBase, 20, 20)
    # oponente.life(tela, oponente.vida, oponente.vidaBase, 560, 20)
    # #insere a posição atual do host
    dic_host= host.get_imagens()
    host.desenhar(tela, dic_host)
    host.drawOponent(tela, oponente)
    
    #inserção do oponente
    # host.drawOponent(tela, oponente, mov)

    pg.display.update()


def loop():
    global tela_atual, nome, select, host

    run= True
    server_conec= True
    msg=(None, False) # mensagem de conexão

    oponente= None # objeto que será oponente

    while server_conec:
        
        # Envia a escolha para o server transmitir ao oponente
        client.send(pk.dumps(msg))
        '''resp é usada para interação entre as telas'''
        oponente, resp= client.recv(pk.loads())

        #roda enquanto não ocorrer os eventos de parada(key==x)
        while run:
            #looping de interação do usuário
            for evento in pg.event.get():
                #se pressionar o X da tela, fecha
                if evento.type == pg.QUIT:
                    run= False
                    break
                #capturas e interpretações de teclas 
                if evento.type== pg.KEYDOWN:
                    if evento.key == pg.K_x:
                        run= False
                        break
                    '''quando um host consegue achar um oponente,
                    muda para tela de seleção de personagens'''
                    if tela_atual=='espera' and resp== True:
                        tela_atual= 'selecao'
                    '''quando host aperta 'r', reseta  a tela para seleção novamente'''
                    if tela_atual=='combate' and evento.key== pg.K_r:
                        tela_atual= 'selecao'
                    #interações na tela de seleção
                    if tela_atual=='selecao':
                        #apaga letra digitada no nome
                        if evento.key == pg.K_BACKSPACE:
                            nome= nome[:-1]
                        #envia escolhas do host
                        elif evento.key== pg.K_RETURN and select:
                            print(f'nome final: {nome}')
                            print("Escolheu o elemento: {select}")
                            #cadeia de seleção/criação de personagem do host
                            if select=='water':
                                from elementos.water import Agua
                                host= Agua(nome if nome else 'client')
                            if select=='fire':
                                from elementos.fire import Fogo
                                host= Fogo(nome if nome else 'client')
                            if select=='air':
                                from elementos.air import Ar
                                host= Ar(nome if nome else 'client')
                            if select=='wood':
                                from elementos.wood import Madeira
                                host= Madeira(nome if nome else 'client')
                            if select=='earth':
                                from elementos.earth import Terra
                                host= Terra(nome if nome else 'client')
                            if nome=='Aang':
                                from elementos.avatar import Avatar
                                host= Avatar(nome if nome else 'client')
                            #após escolha/enter, muda para tela de combate
                            msg= (host, True)
                            if resp == True:
                                tela_atual= 'combate'
                        #adiciona letra digitada ao nome
                        else:
                            nome+= evento.unicode
                            #limita o nome a 12 caracteres
                            if len(nome)>12:
                                nome= nome[:-1]
                #captura o tipo de personagem selecionado
                if evento.type== pg.MOUSEBUTTONDOWN:
                    #armazena a posição do clique do mouse para comparação
                    mouse_pos= pg.mouse.get_pos()
                    #criação de botões de escolha na tela
                    for bot in botoes:
                        if bot.click(mouse_pos):
                            select= bot.txt
                            print(f'personagem selecionado: {select}')
                            
            #onde se decide qual tela desenhar(e desenha)

            if tela_atual=='espera' and resp== False:
                tela_espera()
            if tela_atual=="selecao" and resp== True:
                tela_selecao()
            if tela_atual=='combate' and resp== True:
                tela_combat(oponente)
                
    #se run=False, encerra
    pg.quit()
    
loop()
