import pygame as pg

class Book:

    def __init__(self, position):
        self.image = pg.image.load("assets/book.png").convert()
        self.rect = self.image.get_rect(topleft=position)
        self.open_book_image = pg.image.load("assets/open_book.png").convert()
        self.open_book_rect = self.open_book_image.get_rect(center=(pg.display.get_surface().get_rect().center))
        self.close_button_rect = pg.Rect(self.open_book_rect.right - 42, self.open_book_rect.top + 10, 21, 30)
        self.open_book = False
        self.highlighted = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        if self.open_book:
            screen.blit(self.open_book_image, self.open_book_rect) 
    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                if self.rect.collidepoint(event.pos):
                    self.open_book = not self.open_book
                if self.close_button_rect.collidepoint(event.pos):
                    self.open_book = False