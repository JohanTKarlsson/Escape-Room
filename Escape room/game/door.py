import pygame as pg

class Door:

    def __init__(self, position):
        self.image = pg.image.load("assets/door.png").convert()
        self.rect = self.image.get_rect(topleft=position)
        self.unlocked_image = pg.image.load("assets/door_unlocked.png").convert_alpha()
        self.open_rect = self.unlocked_image.get_rect(center=(self.rect.centerx, self.rect.centery))
        self.door_locked = True
        self.show_open = False
        self.accessibility = False
        self.highlighted = False

        # Load sound effects
        self.locked_sound = pg.mixer.Sound("assets/locked.wav")

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        if self.show_open:
            screen.blit(self.unlocked_image, self.open_rect)
        if self.accessibility and self.highlighted:
            pg.draw.rect(screen, (255, 0, 0), self.rect, 4)       
    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                if self.rect.collidepoint(event.pos): # Checks if the drawer has been clicked
                    if self.door_locked:
                        self.locked_sound.play()
        if event.type == pg.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.highlighted = True
            else:
                self.highlighted = False

    def toggle_open(self):
        self.show_open = True
        self.door_locked = False