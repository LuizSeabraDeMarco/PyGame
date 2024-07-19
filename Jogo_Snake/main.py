import pygame
import random

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

# Parâmetros da cobrinha
tamanha_quadrado = 10
velocidade_jogo = 15

def gerar_comida():
    comida_x = round(random.randrange(0, largura - tamanha_quadrado) / 10.0) * 10.0
    comida_y = round(random.randrange(0, altura - tamanha_quadrado) / 10.0) * 10.0
    return comida_x, comida_y

def selecionar_velocidade(tecla, velocidade_atual_x, velocidade_atual_y):
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
    return velocidade_x, velocidade_y

def desenhar_comida(tamanho, comida_x, comida_y):
    pygame.draw.rect(tela, verde, [comida_x, comida_y, tamanho, tamanho])

def desenhar_cobra(tamanho, pixels):
    for pixel in pixels:
        pygame.draw.rect(tela, branco, [pixel[0], pixel[1], tamanho, tamanho])

def desenhar_pontuacao(pontuacao):
    fonte = pygame.font.SysFont("Helvetica", 20)
    texto = fonte.render(f"Pontos: {pontuacao}", True, vermelho)
    tela.blit(texto, [1, 1])

def rodar_jogo():
    fim_do_jogo = False
    reiniciar_jogo = False

    x = largura / 2
    y = altura / 2

    velocidade_x = 0
    velocidade_y = 0

    tamanho_cobra = 1
    pixels = []

    comida_x, comida_y = gerar_comida()

    while not fim_do_jogo:

        tela.fill(preta)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                fim_do_jogo = True
            elif evento.type == pygame.KEYDOWN:
                velocidade_x, velocidade_y = selecionar_velocidade(evento.key, velocidade_x, velocidade_y)

        desenhar_comida(tamanha_quadrado, comida_x, comida_y)

        x += velocidade_x
        y += velocidade_y

        pixels.append([x, y])
        if len(pixels) > tamanho_cobra:
            del pixels[0]

        for pixel in pixels[:-1]:
            if pixel == [x, y]:
                reiniciar_jogo = True

        if x >= largura or x < 0 or y >= altura or y < 0:
            reiniciar_jogo = True

        if reiniciar_jogo:
            rodar_jogo()
            return

        desenhar_cobra(tamanha_quadrado, pixels)
        desenhar_pontuacao(tamanho_cobra - 1)

        pygame.display.update()

        if x == comida_x and y == comida_y:
            tamanho_cobra += 1
            comida_x, comida_y = gerar_comida()

        relogio.tick(velocidade_jogo)

rodar_jogo()
pygame.quit()
