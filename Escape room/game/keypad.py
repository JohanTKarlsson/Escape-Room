import pygame as pg

class Keypad():

    correct_code = "3249"

    def __init__(self, position):
        self.load_images()
        self.load_sound_effects()
        self.rect = self.image.get_rect(topleft=position)
        self.large_rect = self.large_image.get_rect(center=(self.rect.centerx, self.rect.centery))
        self.close_button_rect = pg.Rect(self.large_rect.right - 17, self.large_rect.top + 4, 16, 16) 
        self.entered_code = ""  # Initialize entered code
        self.can_click_keypad = True
        self.show_large = False
        self.keypad_clicked = False
        self.wrong_code = False
        self.accessibility = False
        self.highlighted = False
        self.solved = False

        self.button_rects = self.create_button_rects()


    def load_images(self):
            self.image = pg.image.load("assets/keypad.png").convert()
            self.large_image = pg.image.load("assets/keypad_large.png").convert_alpha()

    def load_sound_effects(self):
            self.key_sound = pg.mixer.Sound("assets/beep.wav")
            self.correct_sound = pg.mixer.Sound("assets/correct.mp3")
            self.incorrect_sound = pg.mixer.Sound("assets/incorrect.wav")
            self.door_sound = pg.mixer.Sound("assets/door.wav")


    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        code_font = pg.font.Font(None, 39)  
        if self.show_large:
            screen.blit(self.large_image, self.large_rect)  
            code_text = code_font.render(f"{self.entered_code}", True, (0, 0, 0))
            text_rect = code_text.get_rect(center=(self.large_rect.centerx, self.large_rect.centery + 120))
            screen.blit(code_text, text_rect)
            if self.wrong_code:
                incorrect_text = code_font.render("Incorrect", True, (255, 0, 0))
                incorrect_rect = incorrect_text.get_rect(center=(self.large_rect.centerx, self.large_rect.centery + 150))
                screen.blit(incorrect_text, incorrect_rect)
        if self.accessibility and self.highlighted and not self.show_large:
            pg.draw.rect(screen, (255, 0, 0), self.rect, 4)  
            
    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                if self.rect.collidepoint(event.pos) and self.can_click_keypad and not self.show_large: 
                    self.show_large = True
                elif self.show_large and self.close_button_rect.collidepoint(event.pos):
                    self.show_large = False
                    self.wrong_code = False
                    self.entered_code = ""
                # Check if a button in the keypad is clicked
                elif self.show_large:
                    for i, rect in enumerate(self.button_rects):
                        if rect.collidepoint(event.pos) and len(self.entered_code) < 4:
                            # Append the corresponding digit to the entered code
                            self.entered_code += str(i + 1) if i < 9 else "0"
                            self.wrong_code = False #ensures that the "incorrect" message only displays after four digits are entered
                            self.key_sound.play()
                    if len(self.entered_code) == 4:
                        if self.check_code(self.entered_code):
                            self.correct_sound.play()
                            self.door_sound.play()
                            self.show_large = False
                            self.can_click_keypad = False  # Ensure you cannot click the keypad once the code is correct
                            self.solved = True
                        else:
                            self.incorrect_sound.play()
                            self.wrong_code = True
                            self.entered_code = ""
        if event.type == pg.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.highlighted = True
            else:
                self.highlighted = False

    def create_button_rects(self):
        # Define the positions and sizes of the keypad buttons
        button_rects = []
        button_width = 25
        button_height = 25
        button_spacing = 10

        for row in range(4):
            for col in range(3):
                left = self.large_rect.left + 60 + col * (button_width + button_spacing)
                top = self.large_rect.top + 75 + row * (button_height + button_spacing)
                if col == 0 and row == 3 or col == 2 and row == 3:
                    continue  # Skip drawing buttons that are not used, which is star and pound
                button_rects.append(pg.Rect(left, top, button_width, button_height))
                
        return button_rects
    
    def check_code(self, entered_code):
        if entered_code == self.correct_code:
            return True
