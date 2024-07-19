import pygame
import random
import time

pygame.init()
pygame.display.set_caption("Jogo Snake Python")
largura, altura = 600, 400
tela = pygame.display.set_mode((largura, altura))
relogio = pygame.time.Clock()

# Cores RGB
preta = (0, 0, 0)
branco = (255, 255, 255)
vermelho = (255, 0, 0)
verde = (0, 255, 0)
azul = (0, 0, 255)

# Parâmetros da cobrinha
tamanha_quadrado = 10
velocidade_jogo = 15

def gerar_comida():
    comida_x = round(random.randrange(0, largura - tamanha_quadrado) / 10.0) * 10.0
    comida_y = round(random.randrange(0, altura - tamanha_quadrado) / 10.0) * 10.0
    return comida_x, comida_y

def selecionar_velocidade(tecla, velocidade_atual_x, velocidade_atual_y, jogador):
    if jogador == 1:
        if tecla == pygame.K_s and velocidade_atual_y == 0:
            velocidade_x = 0
            velocidade_y = tamanha_quadrado
        elif tecla == pygame.K_w and velocidade_atual_y == 0:
            velocidade_x = 0
            velocidade_y = -tamanha_quadrado
        elif tecla == pygame.K_d and velocidade_atual_x == 0:
            velocidade_x = tamanha_quadrado
            velocidade_y = 0
        elif tecla == pygame.K_a and velocidade_atual_x == 0:
            velocidade_x = -tamanha_quadrado
            velocidade_y = 0
        else:
            velocidade_x = velocidade_atual_x
            velocidade_y = velocidade_atual_y
    elif jogador == 2:
        if tecla == pygame.K_DOWN and velocidade_atual_y == 0:
            velocidade_x = 0
            velocidade_y = tamanha_quadrado
        elif tecla == pygame.K_UP and velocidade_atual_y == 0:
            velocidade_x = 0
            velocidade_y = -tamanha_quadrado
        elif tecla == pygame.K_RIGHT and velocidade_atual_x == 0:
            velocidade_x = tamanha_quadrado
            velocidade_y = 0
        elif tecla == pygame.K_LEFT and velocidade_atual_x == 0:
            velocidade_x = -tamanha_quadrado
            velocidade_y = 0
        else:
            velocidade_x = velocidade_atual_x
            velocidade_y = velocidade_atual_y
    return velocidade_x, velocidade_y

def desenhar_comida(tamanho, comida_x, comida_y):
    pygame.draw.rect(tela, verde, [comida_x, comida_y, tamanho, tamanho])

def desenhar_cobra(tamanho, pixels, cor):
    for pixel in pixels:
        pygame.draw.rect(tela, cor, [pixel[0], pixel[1], tamanho, tamanho])

def desenhar_pontuacao(pontuacao1, pontuacao2):
    fonte = pygame.font.SysFont("Helvetica", 20)
    texto1 = fonte.render(f"Jogador 1: {pontuacao1}", True, vermelho)
    texto2 = fonte.render(f"Jogador 2: {pontuacao2}", True, azul)
    tela.blit(texto1, [1, 1])
    tela.blit(texto2, [400, 1])

def desenhar_tempo_restante(tempo_restante):
    fonte = pygame.font.SysFont("Helvetica", 20)
    texto_tempo = fonte.render(f"Tempo restante: {int(tempo_restante)}s", True, branco)
    tela.blit(texto_tempo, [largura - 200, altura - 30])

def desenhar_mensagem_fim_jogo(mensagem):
    fonte = pygame.font.SysFont("Helvetica", 50)
    texto_fim = fonte.render(mensagem, True, branco)
    tela.blit(texto_fim, [largura / 4, altura / 2])

def verificar_colisao_cabeça(cobra1, cobra2):
    if not cobra1["pixels"] or not cobra2["pixels"]:
        return False

    cabeça_cobra1 = cobra1["pixels"][-1]
    cabeça_cobra2 = cobra2["pixels"][-1]
    return cabeça_cobra1 == cabeça_cobra2

def verificar_colisao_borda(cobra):
    cabeça = cobra["pixels"][-1]
    return (cabeça[0] < 0 or cabeça[0] >= largura or
            cabeça[1] < 0 or cabeça[1] >= altura)

def reiniciar_jogador(jogador, posicao_inicial):
    jogador["x"] = posicao_inicial[0]
    jogador["y"] = posicao_inicial[1]
    jogador["velocidade_x"] = 0
    jogador["velocidade_y"] = 0
    jogador["pixels"] = []
    jogador["tamanho_cobra"] = 1

def rodar_jogo():
    global jogador1, jogador2
    jogador1 = inicializar_jogador(largura / 4, altura / 2)
    jogador2 = inicializar_jogador(3 * largura / 4, altura / 2)
    comida_x, comida_y = gerar_comida()

    inicio = time.time()
    duracao = 60  # Alterar o tempo aqui se necessário

    while True:
        tela.fill(preta)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif evento.type == pygame.KEYDOWN:
                jogador1["velocidade_x"], jogador1["velocidade_y"] = selecionar_velocidade(evento.key, jogador1["velocidade_x"], jogador1["velocidade_y"], 1)
                jogador2["velocidade_x"], jogador2["velocidade_y"] = selecionar_velocidade(evento.key, jogador2["velocidade_x"], jogador2["velocidade_y"], 2)

        desenhar_comida(tamanha_quadrado, comida_x, comida_y)

        jogador1["x"] += jogador1["velocidade_x"]
        jogador1["y"] += jogador1["velocidade_y"]
        jogador2["x"] += jogador2["velocidade_x"]
        jogador2["y"] += jogador2["velocidade_y"]

        jogador1["pixels"].append([jogador1["x"], jogador1["y"]])
        jogador2["pixels"].append([jogador2["x"], jogador2["y"]])

        if len(jogador1["pixels"]) > jogador1["tamanho_cobra"]:
            del jogador1["pixels"][0]
        if len(jogador2["pixels"]) > jogador2["tamanho_cobra"]:
            del jogador2["pixels"][0]

        if jogador1["x"] == comida_x and jogador1["y"] == comida_y:
            comida_x, comida_y = gerar_comida()
            jogador1["tamanho_cobra"] += 1

        if jogador2["x"] == comida_x and jogador2["y"] == comida_y:
            comida_x, comida_y = gerar_comida()
            jogador2["tamanho_cobra"] += 1

        desenhar_cobra(tamanha_quadrado, jogador1["pixels"], vermelho)
        desenhar_cobra(tamanha_quadrado, jogador2["pixels"], azul)

        jogador1_morto = verificar_colisao_borda(jogador1) or verificar_colisao_cabeça(jogador1, jogador2)
        jogador2_morto = verificar_colisao_borda(jogador2) or verificar_colisao_cabeça(jogador2, jogador1)

        if jogador1_morto:
            reiniciar_jogador(jogador1, (largura / 4, altura / 2))

        if jogador2_morto:
            reiniciar_jogador(jogador2, (3 * largura / 4, altura / 2))

        pontuacao1 = jogador1["tamanho_cobra"] - 1
        pontuacao2 = jogador2["tamanho_cobra"] - 1

        desenhar_pontuacao(pontuacao1, pontuacao2)

        tempo_restante = duracao - (time.time() - inicio)
        desenhar_tempo_restante(tempo_restante)

        if tempo_restante <= 0:
            break

        pygame.display.update()
        relogio.tick(velocidade_jogo)
    if pontuacao1 > pontuacao2:
        desenhar_mensagem_fim_jogo("Red win!")
    elif pontuacao2 > pontuacao1:
        desenhar_mensagem_fim_jogo("Blue win!")
    else:
        desenhar_mensagem_fim_jogo("Empate")
    pygame.display.update()
    time.sleep(2)

def inicializar_jogador(x_inicial, y_inicial):
    return {
        "x": x_inicial,
        "y": y_inicial,
        "velocidade_x": 0,
        "velocidade_y": 0,
        "pixels": [],
        "tamanho_cobra": 1
    }

if __name__ == "__main__":
    while True:
        rodar_jogo()
