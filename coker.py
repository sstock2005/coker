import pygame.freetype
import pygame

import modules.globals as gs
import modules.constants as mc
import modules.sprites as sp
import modules.poker_types as pt

pygame.init()
screen = pygame.display.set_mode((mc.WINDOW_WIDTH, mc.WINDOW_HEIGHT))
pygame.display.set_caption("coker - crappy poker")

clock = pygame.time.Clock()
GAME_FONT = pygame.freetype.Font("resources/font/Pixelon.ttf", 32)
TITLE_FONT = pygame.freetype.Font("resources/font/Pixelon.ttf", 64)

if __name__ != '__main__':
    running = False
else:
    running = True
    
while running:
    clock.tick(60)
    
    screen.fill(mc.BACKGROUND_COLOR)
    
    event_list = pygame.event.get()
    
    for event in event_list:
        if event.type == pygame.QUIT:
            running = False
            
    gs.start()
    
    sprites_list = pygame.sprite.Group()
    
    sprites_list.add(gs.DECK)
    
    button_sprites: list[sp.PokerButtonSprite] = []
    
    for poker_button_type in list(pt.PokerButton):
        button_sprites.append(sp.PokerButtonSprite(button=poker_button_type))
        
    sprites_list.add(button_sprites[pt.PokerButton.RAISE.value])
    sprites_list.add(button_sprites[pt.PokerButton.CALL.value])
    sprites_list.add(button_sprites[pt.PokerButton.FOLD.value])
    
    test_button = sp.PokerButtonSprite(button=pt.PokerButton.CALL)

    sprites_list.add(test_button)

    sprites_list.update(event_list)

    for sprite in sprites_list:
        screen.blit(sprite.image, (sprite.x, sprite.y), sprite.rect)

    pygame.display.flip()

pygame.quit()