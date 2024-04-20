import pygame as pg

class Table:

    def __init__(self, position):
        self.image = pg.image.load("assets/table.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=position)
        self.drawer_rect = pg.Rect(self.rect.left, self.rect.top + 25, self.rect.width - 12, self.rect.height // 4)  # rectrangle for the drawer only
        self.drawer_locked = True
        self.drawer_open_image = pg.image.load("assets/drawer.png").convert_alpha()
        self.drawer_open_rect = self.drawer_open_image.get_rect(center=(pg.display.get_surface().get_rect().center))
        self.close_button_rect = pg.Rect(self.drawer_open_rect.right - 33, self.drawer_open_rect.top + 10, 21, 30)
        self.open_drawer_clicked = False
        self.book_rect = pg.Rect(self.drawer_open_rect.right - 390, self.drawer_open_rect.top + 85, 140, 200)
        self.book_collided_with = False
        self.book_taken = False
        self.accessibility = False
        self.highlighted = False
        

        # Load sound effects
        self.locked_sound = pg.mixer.Sound("assets/locked.wav")
        self.open_drawer = pg.mixer.Sound("assets/open_drawer.wav")
        self.pop = pg.mixer.Sound("assets/pop.wav")

    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        if self.open_drawer_clicked:
            screen.blit(self.drawer_open_image, self.drawer_open_rect)  
            if self.book_collided_with:
                pg.draw.rect(screen, (116, 30, 118), self.book_rect, 4)
        if self.accessibility and self.highlighted and not self.open_drawer_clicked:
           pg.draw.rect(screen, (0, 255, 0), self.drawer_rect, 4)   

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and not self.book_taken: # Ensures that all table events are disabled once the book is taken
            if event.button == 1:  # Left mouse button
                if self.drawer_rect.collidepoint(event.pos):
                    print(self.drawer_locked) # Checks if the drawer has been clicked
                    if self.drawer_locked:
                        self.locked_sound.play()
                        print("drawer locked")
                    elif not self.open_drawer_clicked: 
                        self.open_drawer.play()
                        print("drawer unlocked")
                        self.open_drawer_clicked = True
                elif self.open_drawer_clicked and self.close_button_rect.collidepoint(event.pos):
                        self.open_drawer_clicked = False
                elif self.book_rect.collidepoint(event.pos) and self.open_drawer_clicked:
                        self.book_taken = True
                        self.open_drawer_clicked = False
                        self.pop.play()
        if event.type == pg.MOUSEMOTION:
            if self.book_rect.collidepoint(event.pos):
                self.book_collided_with = True
            else:
                self.book_collided_with = False
            if self.drawer_rect.collidepoint(event.pos):
                self.highlighted = True
            else:
                self.highlighted = False
