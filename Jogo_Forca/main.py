import pygame
import unicodedata
import sys

# Inicializa o Pygame
pygame.init()

# Definições de cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)

# Definições da tela
LARGURA_TELA = 800
ALTURA_TELA = 600
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption('Jogo da Forca')

# Fonte
fonte = pygame.font.SysFont('arial', 36)

def desenha_texto(texto, fonte, cor, superficie, x, y):
    obj_texto = fonte.render(texto, True, cor)
    rect_texto = obj_texto.get_rect()
    rect_texto.topleft = (x, y)
    superficie.blit(obj_texto, rect_texto)

def desenha_coracoes(vida):
    coracao = unicodedata.lookup('HEAVY BLACK HEART')
    coracao_surface = fonte.render(coracao, True, VERMELHO)
    for i in range(vida):
        tela.blit(coracao_surface, (10 + i * 40, 10))

def forca(vida):
    palavra_escolhida = input('Escolha uma palavra: ').lower()

    if not palavra_escolhida.isdigit():
        # Inicializa a palavra e os status do jogo
        palavra = list(palavra_escolhida)
        palavra_mostrada = ['_' for _ in palavra_escolhida]
        letra_encontrada = []
        letra_errada = []

        while vida > 0:
            tela.fill(BRANCO)
            desenha_coracoes(vida)
            desenha_texto(' '.join(palavra_mostrada), fonte, PRETO, tela, 20, 100)
            desenha_texto('Letras erradas: ' + ' '.join(letra_errada), fonte, PRETO, tela, 20, 200)
            pygame.display.flip()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.KEYDOWN:
                    letra = pygame.key.name(evento.key).lower()
                    if len(letra) == 1 and letra.isalpha():
                        if letra in palavra:
                            for i in range(len(palavra)):
                                if palavra[i] == letra:
                                    palavra_mostrada[i] = letra
                            letra_encontrada.append(letra)
                            if '_' not in palavra_mostrada:
                                print('A palavra é ' + palavra_escolhida)
                                return
                        else:
                            if letra not in letra_encontrada and letra not in letra_errada:
                                letra_errada.append(letra)
                                vida -= 1
                                if vida == 0:
                                    print('Acabaram suas vidas')
                                    return
                    else:
                        print('Digite apenas uma letra por vez')
            pygame.display.update()

def dificuldade():
    print('[1] Facil(10 vidas)')
    print('[2] Medio(7 vidas)')
    print('[3] Dificil(5 vidas)')
    dificuldade_input = int(input('Digite a dificuldade: '))
    print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=')
    if 0 < dificuldade_input < 4:
        if dificuldade_input == 1:
            forca(10)
        elif dificuldade_input == 2:
            forca(7)
        elif dificuldade_input == 3:
            forca(5)
    else:
        dificuldade()

dificuldade()
