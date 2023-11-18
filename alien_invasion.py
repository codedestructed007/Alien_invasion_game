import sys
import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group


# create screen object
def run_game() :
    pygame.init()

    # Initiating object of class Settings(settings.py)
    ai_settings = Settings()

    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height)
    )
    pygame.display.set_caption('Alien Invasion')

    # make a ship , a group of bullets , and group of aliens
    ship = Ship(ai_settings,screen)

    aliens = Group()
    
    bullets = Group()
    
    # background color
    bg_color = (230, 230, 220)
    
    # Create the fleet of aliens
    gf.create_fleet(ai_settings,screen,ship, aliens)

    # loop for game
    while True :
        gf.check_events(ai_settings,screen,ship, bullets)
        ship.update()
        gf.update_bullets(ai_settings,screen, ship,aliens, bullets)
        gf.update_aliens(ai_settings, ship, aliens)
        gf.update_screen(ai_settings, screen, ship, aliens, bullets)
        bullets.update()
        # screen.fill(bg_color)
        
        # Get rid of bullets that have disappeared
        for bullet in bullets.copy():
            if bullet.rect.bottom <=0:
                bullets.remove(bullet)
                
        print(len(bullets))
        
        gf.update_screen(ai_settings,screen, ship,aliens, bullets)
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                sys.exit()
        ship.blitme()
        pygame.display.flip()


run_game()
