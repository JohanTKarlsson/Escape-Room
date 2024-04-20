import pygame as pg

class Poster():
    correct_code = "SOLUTION"

    def __init__(self, position):
        self.image = pg.image.load("assets/poster.png").convert()
        self.rect = self.image.get_rect(topleft=position)
        self.large_image = pg.image.load("assets/poster_large.png").convert_alpha()
        self.large_rect = self.large_image.get_rect(center=(self.rect.centerx, self.rect.centery))
        self.close_button_rect = pg.Rect(self.large_rect.right - 29, self.large_rect.top + 12, 16, 24)
        self.show_large = False
        self.entered_code = ""
        self.solved = False
        self.wrong_code = False
        self.accessibility = False
        self.highlighted = False

        #Load sound effects
        self.correct_sound = pg.mixer.Sound("assets/correct.mp3")
        self.incorrect_sound = pg.mixer.Sound("assets/incorrect.wav")
        self.door_sound = pg.mixer.Sound("assets/door.wav")

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        code_font = pg.font.Font(None, 39)  
        if self.show_large:
            screen.blit(self.large_image, self.large_rect)  
            code_text = code_font.render(f"{self.entered_code}", True, (0, 0, 0))
            text_rect = code_text.get_rect(center=(self.large_rect.centerx, self.large_rect.centery + 150))
            screen.blit(code_text, text_rect)
            if self.wrong_code:
                incorrect_text = code_font.render("Incorrect", True, (255, 0, 0))
                incorrect_rect = incorrect_text.get_rect(center=(self.large_rect.centerx, self.large_rect.centery + 150))
                screen.blit(incorrect_text, incorrect_rect)
            elif self.solved:
                correct_text = code_font.render("Correct!", True, (0, 255, 0))
                correct_rect = correct_text.get_rect(center=(self.large_rect.centerx, self.large_rect.centery + 150))
                screen.blit(correct_text, correct_rect)
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
                if event.key in [pg.K_a, pg.K_b, pg.K_c, pg.K_d, pg.K_e, pg.K_f, pg.K_g, pg.K_h, pg.K_i, pg.K_j, pg.K_k,
                                 pg.K_l, pg.K_m, pg.K_n, pg.K_o, pg.K_p, pg.K_q, pg.K_r, pg.K_s, pg.K_t, pg.K_u, pg.K_v,
                                 pg.K_w, pg.K_x, pg.K_y, pg.K_z, pg.K_RETURN, pg.K_BACKSPACE] and not self.solved:
                    if event.key == pg.K_RETURN:
                        if self.check_code(self.entered_code):
                            self.correct_sound.play()
                            self.solved = True
                            self.entered_code = ""
                            self.door_sound.play()   
                        else:
                            self.incorrect_sound.play()
                            self.wrong_code = True
                            self.entered_code = "" 
                    elif event.key == pg.K_BACKSPACE:
                        self.entered_code = self.entered_code[:-1]
                    elif len(self.entered_code) < 12: #ensure a word that is too long is not entered
                        self.wrong_code = False
                        self.entered_code += event.unicode.upper() if event.key != pg.K_BACKSPACE else ""

    def check_code(self, entered_code):
        if entered_code == self.correct_code:
            return True
