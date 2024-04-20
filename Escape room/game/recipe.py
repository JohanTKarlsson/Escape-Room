import pygame as pg

class Recipe():
    def __init__(self, position):
        self.image = pg.image.load("assets/recipe.png").convert()
        self.rect = self.image.get_rect(topleft=position)
        self.large_image = pg.image.load("assets/recipe_large.png").convert_alpha()
        self.large_rect = self.large_image.get_rect(center=(self.rect.centerx, self.rect.centery))
        self.close_button_rect = pg.Rect(self.large_rect.right - 20, self.large_rect.top + 7, 16, 16)
        self.show_large = False
        self.accessibility = False # ensures recipe is not highlighted by default
        self.highlighted = False # activated through mouseover

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        if self.show_large:
            screen.blit(self.large_image, self.large_rect)
        if self.accessibility and self.highlighted and not self.show_large:
            pg.draw.rect(screen, (255, 0, 0), self.rect, 4)

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                if self.rect.collidepoint(event.pos):
                    self.show_large = True
                elif self.show_large and self.close_button_rect.collidepoint(event.pos):
                        self.show_large = False
        if event.type == pg.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.highlighted = True
            else:
                self.highlighted = False
