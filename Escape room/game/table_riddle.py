import pygame as pg

class TableRiddle:
    correct_code = "134"

    def __init__(self, position):
        self.image = pg.image.load("assets/table_picture.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=position)
        self.large_image = pg.image.load("assets/table_code.png").convert_alpha()
        self.large_rect = self.large_image.get_rect(center=(pg.display.get_surface().get_rect().center))
        self.close_button_rect = pg.Rect(self.large_rect.right - 20, self.large_rect.top + 7, 16, 16)
        self.entered_code = ""
        self.show_large = False
        self.wrong_code = False
        self.solved = False
        self.accessibility = False
        self.highlighted = False
        
        #Load sound effects
        self.correct_sound = pg.mixer.Sound("assets/correct.mp3")
        self.incorrect_sound = pg.mixer.Sound("assets/incorrect.wav")
        
    

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        code_font = pg.font.Font(None, 39) 
        if self.show_large and not self.solved:
            screen.blit(self.large_image, self.large_rect)  
            code_text = code_font.render(f"{self.entered_code}", True, (0, 0, 0))
            text_rect = code_text.get_rect(center=(self.large_rect.centerx, self.large_rect.centery + 290))
            screen.blit(code_text, text_rect)
            if self.wrong_code:
                incorrect_text = code_font.render("Incorrect", True, (255, 0, 0))
                incorrect_rect = incorrect_text.get_rect(center=(self.large_rect.centerx, self.large_rect.centery + 290))
                screen.blit(incorrect_text, incorrect_rect)
        if self.accessibility and self.highlighted and not self.show_large:
           pg.draw.rect(screen, (0, 255, 0), self.rect, 4)   
            

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                if self.rect.collidepoint(event.pos):
                    self.show_large = True
                elif self.show_large and self.close_button_rect.collidepoint(event.pos):
                        self.show_large = False
                        self.wrong_code = False
                        self.entered_code = ""
        if event.type == pg.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.highlighted = True
            else:
                self.highlighted = False
        if self.show_large:
            if event.type == pg.KEYDOWN:
                if event.key in [pg.K_1, pg.K_2, pg.K_3, pg.K_4, pg.K_5, pg.K_6, pg.K_7, pg.K_8, pg.K_9, pg.K_0] and not self.solved:
                    self.wrong_code = False
                    self.entered_code += str((event.key - pg.K_0) % 256)
                    if len(self.entered_code) == 3:
                        if self.check_code(self.entered_code):
                            self.correct_sound.play()
                            self.solved = True
                        else:
                            self.incorrect_sound.play()
                            self.wrong_code = True
                            self.entered_code = ""  

    def check_code(self, entered_code):
        if entered_code == self.correct_code:
            return True                  