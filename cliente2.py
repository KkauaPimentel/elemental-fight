import pygame as pg
import os
import socket
import pickle as pk
import threading
from botao import Botao
from elementos.personagem import Personagem  # Sua classe com desenhar() e drawOponent()

# --- Conexão com o servidor ---
IP, port = "127.0.0.1", 8000
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, port))

# --- Parâmetros da janela e assets ---
tela_larg, tela_alt = 1000, 640
tela_atual = 'espera'
pg.font.init()
tela = pg.display.set_mode((tela_larg, tela_alt))
pg.display.set_caption("Client")
img_fundo = pg.image.load(os.path.join('imagens', 'fundo-x1.jpg'))
img_selec = pg.image.load(os.path.join('imagens', 'fundo-tela.jpg'))

# --- Variáveis globais de jogo ---
nome = ''
select = None
host = None  # Objeto do personagem deste cliente (nosso host)
oponente = None  # O objeto do oponente, quando recebido
flag= False
# O protocolo: o servidor envia uma tupla (opponent_object, flag)
# Se flag == False, o oponente não escolheu ainda.
# Se flag == True, o oponente já escolheu.
# Inicialmente, ambos estão (None, False)

# --- Botões de escolha dos elementos ---
botoes = [
    Botao("water", 250, 200, (255,255,255), (0,0,0)),
    Botao("earth", 450, 200, (255,255,255), (0,0,0)),
    Botao("fire", 650, 200, (255,255,255), (0,0,0)),
    Botao("air", 350, 350, (255,255,255), (0,0,0)),
    Botao("wood", 550, 350, (255,255,255), (0,0,0))
]

# --- Função auxiliar ---
def background(img):
    img_ajust = pg.transform.scale(img, (tela_larg, tela_alt))
    tela.blit(img_ajust, (0,0))

# --- Telas ---
def tela_espera():
    background(img_selec)
    fonte = pg.font.SysFont('comicsans', 65)
    texto = fonte.render("Esperando oponente...", True, (0,0,0))
    texto2 = fonte.render("Esperando oponente...", True, (255,255,255))
    tela.blit(texto, (tela_larg/2 - texto.get_width()/2, tela_alt/2 - texto.get_height()/2))
    tela.blit(texto2, (tela_larg/2 - texto2.get_width()/2, tela_alt/2 - texto2.get_height()/2))
    pg.display.update()

def tela_selecao():
    background(img_selec)
    fonte = pg.font.SysFont('arial', 35)
    fonte_name = pg.font.SysFont('arial', 24)
    texto = fonte.render("Digite seu nome: *", True, (255,255,255))
    tela.blit(texto, (340, 50))
    pg.draw.rect(tela, (0,0,0), (327, 95, 316, 50))
    pg.draw.rect(tela, (200,200,200), (337, 100, 300, 40))
    txt_nome = fonte_name.render(nome[:12], True, (0,0,0))
    tela.blit(txt_nome, (342, 107))
    for bot in botoes:
        bot.draw_B(tela)
    if select:
        msg = f"Elemento selecionado: {select.capitalize()}"
        txt_selec = fonte.render(msg, True, (255,255,255))
        tela.blit(txt_selec, (tela_larg/2 - txt_selec.get_width()/2, tela_alt - 100))
    # Se o host já enviou sua escolha mas o oponente ainda não escolheu, exibe mensagem:
    if host is not None and oponente is None:
        aguarde = fonte.render("Aguardando escolha do oponente.", True, (255,255,0))
        tela.blit(aguarde, (tela_larg/2 - aguarde.get_width()/2, tela_alt - 150))
    pg.display.update()

def tela_combat():
    global host, oponente
    background(img_fundo)
    # Desenha o host e sua vida
    if host is not None and oponente is not None:
        dic_host = host.get_imagens()
        host.desenhar(tela, dic_host, oponente)
        host.life(tela, host.vida, host.vidaBase, 20, 20)
        
    # Se o oponente foi recebido, desenha-o
    if oponente is not None:
        host.drawOponent(tela, oponente)  # Aqui usamos "parado" por default
        # Exibe a barra de vida do oponente (posição à direita)
        oponente.life(tela, oponente.vida, oponente.vidaBase, 540, 20)
    pg.display.update()

# --- Thread de comunicação ---
def comunicacao():
    """
    Este loop envia periodicamente o estado do cliente para o servidor e recebe do servidor
    uma tupla (oponente_obj, flag). A interpretação é a seguinte:
      - (None, False): o oponente ainda não está conectado.
      - (None, True): o oponente está conectado, mas ainda não escolheu.
      - (object, True): o oponente já escolheu seu personagem.
    """
    global host, oponente, flag
    while True:
        try:
            # Se o cliente ainda não escolheu seu personagem, host é None.
            # Nesse caso, enviamos (None, True) para indicar "estou conectado"
            # (a flag True é para indicar que o cliente está pronto para jogar).
            if host is None:
                msg = (None, True)
            else:
                msg = (host, True)
            client.send(pk.dumps(msg))
            
            # Recebe do servidor a tupla com o estado do oponente.
            data = client.recv(4096)
            resp = pk.loads(data)
            
            # Interpretação do que foi recebido:
            # Se resp[1] for True e resp[0] for None -> o oponente está conectado mas ainda não escolheu.
            # Se resp[1] for True e resp[0] não for None -> o oponente já escolheu.
            # Se resp[1] for False -> o oponente não está presente (ou desconectado).
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
    global tela_atual, nome, select, host, flag
    run = True
    while run:
        for evento in pg.event.get():
            if evento.type == pg.QUIT:
                run = False
                break
            if evento.type == pg.KEYDOWN:
                if evento.key == pg.K_x:
                    run = False
                    break
                # Se estiver na tela de espera e receber uma flag True (do servidor), muda para seleção
                if tela_atual == 'espera':
                    # A mudança é feita com base na comunicação; aqui, se o flag for True, a thread de comunicação
                    # fará com que o oponente seja diferente de None e, assim, podemos mudar a tela.
                    if flag== True:
                        tela_atual = 'selecao'  
                if tela_atual == 'combate' and evento.key == pg.K_r:
                    tela_atual = 'selecao'
                if tela_atual == 'selecao':
                    if evento.key == pg.K_BACKSPACE:
                        nome = nome[:-1]
                    elif evento.key == pg.K_RETURN and select:
                        print(f'Nome final: {nome}')
                        print(f"Escolheu o elemento: {select}")
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
                        if nome == 'Aang':
                            from elementos.avatar import Avatar
                            host = Avatar(nome if nome else 'client')

                        tela_atual = 'combate'
                    else:
                        if len(nome) < 12:
                            nome += evento.unicode
            if evento.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                for bot in botoes:
                    if bot.click(mouse_pos):
                        select = bot.txt
                        print(f'Personagem selecionado: {select}')
        if tela_atual == 'espera':
            tela_espera()
        elif tela_atual == 'selecao':
            tela_selecao()
        elif tela_atual == 'combate':
            tela_combat()
    pg.quit()

loop()
