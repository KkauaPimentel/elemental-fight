import pygame as pg
import os
import socket
import pickle as pk
import threading
from botao import Botao

# Realiza a busca pelo IP do servidor na rede usando broadcast 
def discover_server():
    UDP_IP = "<broadcast>"
    UDP_PORT = 9000

    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    udp_sock.settimeout(4)  # Timeout de 4 segundos

    '''
    Envia-se uma mensagem broadcast(para toda a rede local)
    Se obter um IP, conecta-se a primeira máquina que respondeu
    Se você quiser se conectar a um IP específico, pode inserir ele
    em server_ip, substituindo a descoberta 
    '''
    try:
        udp_sock.sendto("cade_server".encode(), (UDP_IP, UDP_PORT))
        data, addr = udp_sock.recvfrom(1024)
        resp= pk.loads(data)
        if resp[0] == "aqui_estou":
            # addr é o address do server
            print("Server encontrado em:", resp[1])
            return resp[1]
    except Exception as e:
        print("Server não encontrado:", e)
    return None

client_teste= ""
server_ip = discover_server()

def background(img):
    # Ajusta as imagens a tela
    img_ajust = pg.transform.scale(img, (tela_larg, tela_alt))
    tela.blit(img_ajust, (0,0))


def tela_espera():
    background(img_selec)

    # Fontes usadas na tela
    fonte1 = pg.font.SysFont('comicsans', 65)
    fonte2 = pg.font.SysFont('comicsans', 63)
    fonte3 = pg.font.SysFont('arial', 40)
    
    # Textos principais
    texto = fonte1.render("Esperando oponente...", True, (0,0,0))
    texto2 = fonte2.render("Esperando oponente...", True, (255,255,255))
    
    # Texto da legenda da caixa de digitação
    texto_legenda = fonte3.render("Digite o IP do servidor:", True, (200,200,200))
    
    # Desenha os textos de espera
    tela.blit(texto, (tela_larg/2 - texto.get_width()/2, tela_alt/2 - texto.get_height()/2))
    tela.blit(texto2, (tela_larg/2 - texto2.get_width()/2, tela_alt/2 - texto2.get_height()/2))
    
    # Desenha a caixa de digitação
    pg.draw.rect(tela, (0,0,0), (444, 495, 330, 60))
    pg.draw.rect(tela, (200,255,200), (450, 500, 316, 50))
    
    # Insere a legenda na caixa
    tela.blit(texto_legenda, (16, 510))
    
    # Exibe o IP digitado até o momento
    ip_text = fonte3.render(client_teste, True, (0,0,0))
    tela.blit(ip_text, (460, 510))
    
    pg.display.update()

# --- Parâmetros da janela ---

tela_larg, tela_alt = 1000, 640
tela_atual = 'espera'# O valor default da janela é em espera

pg.font.init()# Usado para iniciar as fontes que usaremos em tela
tela = pg.display.set_mode((tela_larg, tela_alt))
pg.display.set_caption("Elemental Fight")# Nome da janela

#Imagens usadas no fundo da tela
img_fundo = pg.image.load(os.path.join('imagens', 'fundo-x1.jpg'))
img_selec = pg.image.load(os.path.join('imagens', 'fundo-tela.jpg'))
img_win = pg.image.load(os.path.join('imagens', 'fundo-win.png'))
img_lose = pg.image.load(os.path.join('imagens', 'fundo-lose.jpg'))


# --- Variáveis globais de jogo ---
nome = ''#Nome do personagem
select = None# Indica que personagem foi escolhido no botão
host = None  # Objeto do personagem do host
oponente = None  # O objeto do personagem oponente
flag= False # Indica se há oponente ou não

'''
------ Interação de telas: o servidor envia uma tupla (opponent_object, flag) ------
Se flag == False and objt None, o oponente não está disponível ainda.
Se flag == True and objt None, oponente já está disponível, avançando para tela de seleção
Se flag == True and oponente is not None, o oponente já escolheu.
No começo, ambos estão (None, False)
'''

# Se a busca automática de IP não der certo, permite ao usuário digitar o IP do server
if server_ip is None:
    print("Não foi possível encontrar o servidor na rede.")
    run= True
    while run:
        # As interações serão as mesmas encontradas na main
        tela_espera()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                break
            # Captura do teclado
            if event.type == pg.KEYDOWN:
                # Se host tecla x, fecha 
                if event.key == pg.K_x:
                    run = False
                    break
                if event.key == pg.K_BACKSPACE:
                        client_teste = client_teste[:-1]
                    # Se apertar enter, envia suas escolhas e flags pro oponente e aguarda as seleções dele
                elif event.key == pg.K_RETURN and tela_atual=='espera':
                    print(f'IP digitado: {client_teste}')
                    server_ip= client_teste
                    run= False
                    break
                else:
                    if len(client_teste) < 14:
                        client_teste += event.unicode

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((server_ip, 8000))


# --- Botões de escolha dos elementos ---
botoes = [
    Botao("water", 250, 200, (255,255,255), (0,0,0)),
    Botao("earth", 450, 200, (255,255,255), (0,0,0)),
    Botao("fire", 650, 200, (255,255,255), (0,0,0)),
    Botao("air", 350, 350, (255,255,255), (0,0,0)),
    Botao("wood", 550, 350, (255,255,255), (0,0,0))
]

def tela_selecao():
    background(img_selec)

    fonte = pg.font.SysFont('arial', 35)
    fonte_name = pg.font.SysFont('arial', 24)
    
    texto = fonte.render("Digite seu nome: *", True, (255,255,255))
    
    tela.blit(texto, (340, 50))
    # Retangulos de exibiçao do nome
    pg.draw.rect(tela, (0,0,0), (327, 95, 316, 50))
    pg.draw.rect(tela, (200,200,200), (337, 100, 300, 40))
    # Exibe o nome digitado do personagem com no máx 12 caracteres
    txt_nome = fonte_name.render(nome[:12], True, (0,0,0))
    tela.blit(txt_nome, (342, 107))
    # Insere os botões de elementos na tela
    for bot in botoes:
        bot.draw_B(tela)
    # Indica qual elemento o host selecionou
    if select:
        msg = f"Elemento selecionado: {select.capitalize()}"
        txt_selec = fonte.render(msg, True, (255,255,255))
        tela.blit(txt_selec, (tela_larg/2 - txt_selec.get_width()/2, tela_alt - 100))
    
    # Se o host já enviou sua escolha mas o oponente ainda não escolheu, mostra a  mensagem:
    if host is not None and oponente is None:
        aguarde = fonte.render("Aguardando escolha do oponente.", True, (255,255,0))
        tela.blit(aguarde, (tela_larg/2 - aguarde.get_width()/2, tela_alt - 150))
    
    pg.display.update()

def tela_combat():
    global host, oponente, tela_atual

    background(img_fundo)
    # Sé o oponente está nulo, quer dizer que apertou 'r'
    if oponente is not None:
        # Se o oponente foi selecionado, desenha
        if oponente is not None:
            # Desenha o oponente com base no último movimento recebido
            host.drawOponent(tela, oponente)
            # Exibe a barra de vida do oponente mais a direita(oponente.x >> host.x)
            oponente.life(tela, oponente.vida, oponente.vidaBase, 540, 20)
        
        # Desenha o host e sua vida
        if host is not None and oponente is not None:
            dic_host = host.get_imagens()
            host.desenhar(tela, dic_host, oponente)
            host.life(tela, host.vida, host.vidaBase, 20, 20)
    else:
        tela_atual= 'selecao'
        

    pg.display.update()

def tela_win():
    global tela_atual
    
    if host.vida<10:# Quer dizer que perdeu
        background(img_lose)
    else:# Quer dizer que ganhou
        background(img_win)
    
    # Garantir permanencia na tela de win
    tela_atual= 'win'
    pg.display.update()


# --- Thread de comunicação ---
def comunicacao():
    """
    Este loop envia periodicamente as escolhas do cliente para o servidor e recebe do servidor
    uma tupla (obj, flag) do oponente. Também mantem a conexão
    """
    global host, oponente, flag
    
    while True:
        try:
            '''--- Envio de mensagens para o servidor ---
            Se o host não estiver conectado, o servidor recebe (None, False)
            Se o host conecta, envia (None, True), ainda na tela de espera
            Se ainda não escolheu ser personagem, envia novamente (None, True), na tela de seleção
            Se o host escolheu, envia (objt_host, True)
            '''
            if host is None:
                msg = (None, True)
            else:
                msg = (host, True)
            # Envia a decisão serializada(Binária) para o servidor
            client.send(pk.dumps(msg))
            
            # Recebe do servidor a tupla com o estado do oponente e desserializa
            data = client.recv(4096)
            resp = pk.loads(data)
            
            # Line 31 - 34
            if resp[1] == True:
                oponente = resp[0]
                flag= True
            else:
                oponente = None
        except Exception as e:
            print("Erro na comunicação:", e)
            break

threading.Thread(target=comunicacao, daemon=True).start()
print("Thread de comunicação iniciada")

# --- Loop principal ---
def loop():
    global tela_atual, nome, select, host, flag, client_teste

    run = True

    while run:
        # Captura cada interação do host x oponente
        for evento in pg.event.get():
            # Se host clica no X da tela, fecha
            if evento.type == pg.QUIT:
                run = False
                break
            # Captura do teclado
            if evento.type == pg.KEYDOWN:
                # Se host tecla x, fecha 
                if evento.key == pg.K_x:
                    run = False
                    break
                # Se estiver na tela de espera e receber uma flag True (do servidor), muda para seleção
                if tela_atual == 'espera':
                    #se tiver oponente, pode mudar de tela
                    if flag== True:
                        tela_atual = 'selecao'
                if tela_atual == 'combate' and oponente is None:
                    tela_atual= 'selecao'
                # Se tecla r, volta para tela de seleção  
                if tela_atual == 'combate' and evento.key == pg.K_r:
                    # host= None    
                    tela_atual = 'selecao'
                if tela_atual=='win' and evento.key == pg.K_r:
                    tela_atual='selecao'
                # Interações de escolha da tela de seleção
                if tela_atual == 'selecao':
                    # Apaga uma letra digitada
                    if evento.key == pg.K_BACKSPACE:
                        nome = nome[:-1]
                    # Se apertar enter, envia suas escolhas e flags pro oponente e aguarda as seleções dele
                    elif evento.key == pg.K_RETURN and select:
                        print(f'Nome final: {nome}')
                        print(f"Escolheu o elemento: {select}")
                        # Cria personagem host com base no botão/escolha
                        if select == 'water':
                            from elementos.water import Agua
                            host = Agua(nome if nome else 'client')
                        elif select == 'fire':
                            from elementos.fire import Fogo
                            host = Fogo(nome if nome else 'client')
                        elif select == 'air':
                            from elementos.air import Ar
                            host = Ar(nome if nome else 'client')
                        elif select == 'wood':
                            from elementos.wood import Madeira
                            host = Madeira(nome if nome else 'client')
                        elif select == 'earth':
                            from elementos.earth import Terra
                            host = Terra(nome if nome else 'client')
                        if nome == 'Aang' or host.nome =='Aang':
                            from elementos.avatar import Avatar
                            host = Avatar('Avatar - gg')
                        # Muda para tela de combate
                        if oponente is not None:
                            tela_atual = 'combate'
                    # Continua a digitação adicionando letra ao nome
                    else:
                        if len(nome) < 12:
                            nome += evento.unicode
            # Captura do clique em botões
            if evento.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                for bot in botoes:
                    if bot.click(mouse_pos):
                        select = bot.txt
                        print(f'Personagem selecionado: {select}')
        # Decisão de tela
        if tela_atual == 'espera':
            tela_espera()
        elif tela_atual == 'selecao':
            tela_selecao()
        elif tela_atual == 'combate':
            if host.vida<= 0 or oponente.vida <=0:
                tela_win()
            else:
                tela_combat()
    # Fecha a tela se aperta X da tela/teclado
    pg.quit()

loop()