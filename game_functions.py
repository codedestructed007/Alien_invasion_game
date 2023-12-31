import sys
from bullet import Bullet
import pygame
from alien import Alien

def change_fleet_direction(ai_settings, aliens):
    """
    Drop the entire fleet and change the fleet's direction"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1
            

def check_fleet_edges(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
        
        
def get_number_aliens_x(ai_settings, alien_width):
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / ( 2* alien_width))
    return number_aliens_x

def get_numbner_rows(ai_settings, ship_height, alien_height):
    """Determine the number of aliens that fit in a row"""
    available_space_y = (ai_settings.screen_height - (3 * alien_height)- ship_height)
    
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create an alien and place it in the row"""
    alien= Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width +2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2* alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    # Create an alien and find the number of aliens in a row
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    number_alien_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_numbner_rows(ai_settings, ship.rect.height, alien.rect.height)
    
    
    # creating the first of alien
    for row_number in range(number_rows):
        for alien_number in range(number_alien_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)
            alien = Alien(ai_settings, screen)
            alien.x = alien_width + 2* alien_width * alien_number
            alien.rect.x = alien.x
            aliens.add(alien)

def update_aliens(ai_settings,ship, aliens):
    """
    Chekc if the fleet is at an edge,
    and then update the positions of all aliens in the fleet
    """
    
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    
    # Look for alien-ship collisions.
    if pygame.sprite.spritecollideany(ship,aliens):
        print('Ship destroyed')

def fire_bullet(ai_settings, screen ,ship, bullets):
    """
    Fire a bullet if limit not reached yet."""
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def check_keydown_events(event,ai_settings,screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
        
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
        
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    # will end the game when 'Q' is pressed
    elif event.key == pygame.K_q:
        sys.exit()
        
def check_keyup_events(event, ship):
    """
    Respond to key release"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings, screen, ship, bullets):
    """
    Respond to keypresses and mouse events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event,ai_settings,screen,ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
             
                
def update_screen(ai_settings, screen, ship,aliens,bullets):
    """
    Updates images on the screen adn flip to the new screen"""
    screen.fill(ai_settings.bg_color)
    
    # redraw all bulletes, behind ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    
    #make the most recently drawn screen visible.
    pygame.display.flip()
    
    
def update_bullets(ai_settings, screen,ship,aliens ,bullets):
    """Update position of bullets and get rid of bulletes."""
    bullets.update()
    
    # Get rid of bullets that have disappeared.
    for bullet in bullets.copy():
        if bullet.rect.bottom <=0:
            bullets.remove(bullet)
            
    check_bullet_alien_collisions(ai_settings,screen,ship,aliens,bullets)
    
def check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets):
    collisions = pygame.sprite.groupcollide(bullets,aliens,True, True)
    if len(aliens) == 0:
        # Destroy existing bullets and create new fleet
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)