class Settings():
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 600
        self.bg_color  = (230,230,220)
        
        # ship speed
        self.ship_speed_factor = 1.5
        
        #Bullet settings
        self.bullet_speed_factor = 3
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60,50,60

        self.bullets_allowed = 3
        # Alien settings
        self.alien_speed_factor = 1
        
        self.fleet_drop_speed = 0.2
        # fleet direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1