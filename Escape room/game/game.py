import pygame as pg
import sys
from keypad import Keypad
from recipe import Recipe
from door import Door
from table import Table
from table_riddle import TableRiddle
from book import Book
from poster import Poster

class Game:

    def __init__(self, screen, clock):
        pg.init()
        self.load_images()
        self.load_sounds()
        self.room_number = 1
        self.hints_used = 0
        self.room2_rendered = False
        self.accessibility_activated = False
        self.end_of_game = False
        self.hint_clicked = False
        self.hint1_used = False
        self.hint2_used = False
        self.hint3_used = False
        self.screen = screen
        self.clock = clock
        self.width, self.height = self.screen.get_size()

        self.font = pg.font.Font(None, 36)
        self.elapsed_time = 0  # Elapsed time in milliseconds
        self.update_room() # loads the current room

    def load_images(self):
        #Load accessibility buttons and hint button, and create a rect for both
        self.acc_button_on = pg.image.load("assets/acc_button_on.png").convert_alpha() 
        self.acc_button_off = pg.image.load("assets/acc_button_off.png").convert_alpha()
        self.acc_button_rect = self.acc_button_on.get_rect(topleft=(1100, 800)) # create the rectangle of the button
        self.hint_button = pg.image.load("assets/hint_button.png").convert_alpha()
        self.hint_button_rect = self.hint_button.get_rect(topleft=(1200, 800))
        self.hint1 = pg.image.load("assets/hint1.png").convert()
        self.hint2 = pg.image.load("assets/hint2.png").convert() 
        self.hint3 = pg.image.load("assets/hint3.png").convert()
        self.hint_rect = self.hint1.get_rect(center=(pg.display.get_surface().get_rect().center))
        close_button_x = 1085
        close_button_y = 211
        self.close_button_rect = pg.Rect(close_button_x, close_button_y, 21, 30)

        

    def load_sounds(self):  
        pg.mixer.music.load("assets/room1_music.wav")
        pg.mixer.music.play(loops=-1)
        self.room2transition_sound = pg.mixer.Sound("assets/room2transition.wav")
        self.victory = pg.mixer.Sound("assets/victory.wav")

    def update_room(self):
        if self.room_number == 1: #loads the first room
            self.background_image = pg.image.load("assets/room1.png").convert()
            self.recipe = Recipe((950, 210))
            self.keypad = Keypad((630, 330))
            self.door = Door((700, 130))
        elif self.room_number == 2: # loads the second room 
            self.background_image = pg.image.load("assets/room2.png").convert()
            self.door = Door((1100, 73))
            self.poster = Poster((200, 100))
            self.table_riddle = TableRiddle((425, 360))
            self.table = Table((400, 430))
            self.book = Book((40, 680))
            self.room2transition_sound.play()
            if self.accessibility_activated: # Ensures that if accessbility mode is activated it continues in room 2
                self.table.accessibility = True
                self.door.accessibility = True
                self.table_riddle.accessibility = True
                self.poster.accessibility = True   
        
    def run(self): 
        self.playing = True
        while self.playing:
            self.clock.tick(60)
            self.handle_event()
            self.update()
            self.draw()
            if self.end_of_game:
                pg.mixer.music.stop()
                
    def handle_event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if self.door is not None:
                self.door.handle_event(event)
            if self.room_number == 1: # Checks what room is being played
                if self.recipe is not None:
                    self.recipe.handle_event(event)
                if self.keypad is not None:
                    self.keypad.handle_event(event)
            if self.room_number == 2: # Checks what room is being played
                if self.table is not None:
                    self.table.handle_event(event)
                if self.table_riddle is not None:
                    self.table_riddle.handle_event(event)
                if self.book is not None:
                    self.book.handle_event(event)
                if self.poster is not None:
                    self.poster.handle_event(event)
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
                # if event.type == pg.K_TAB:
                    # to do. tabbing between objects
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    if self.door is not None:
                        if self.door.rect.collidepoint(event.pos):
                            if self.door.show_open:
                                self.room_number = 2
                            if hasattr(self, 'poster') and self.poster.solved and self.table_riddle.solved: #trigger the end of game function
                                self.game_over()
                        elif self.acc_button_rect.collidepoint(event.pos):
                            self.accessibility_activated = not self.accessibility_activated
                            self.toggle_accessibility()
                        if self.hint_button_rect.collidepoint(event.pos): # ensures hint cannot be clicked if it is already displayed
                            if not self.hint_clicked:
                                self.hint_clicked = True
                                self.hint_counter()
                            else:
                                self.hint_clicked = False
                        if self.close_button_rect.collidepoint(event.pos):
                            self.hint_clicked = False

    def toggle_accessibility(self):
        self.door.accessibility = not self.door.accessibility
        if self.keypad is not None:
            self.keypad.accessibility = not self.keypad.accessibility
        if self.recipe is not None:
            self.recipe.accessibility = not self.recipe.accessibility  
        if self.room_number == 2:
                self.table.accessibility = not self.table.accessibility  
                self.table_riddle.accessibility = not self.table_riddle.accessibility
                self.poster.accessibility = not self.poster.accessibility  

    def hint_counter(self): # increments the hint counter depending on how many hints have been used
        if self.room_number == 1:
            if self.hints_used == 0 and not self.hint1_used:
                self.hint1_used = True
                self.hints_used = 1
        elif self.room_number == 2:
            if self.hints_used == 0:
                if not self.table_riddle.solved and not self.hint2_used:
                    self.hint2_used = True
                    self.hints_used = 1
                elif self.table_riddle.solved and not self.hint3_used:
                    self.hint3_used = True
                    self.hints_used = 1
            elif self.hints_used == 1:
                if not self.hint2_used and not self.table_riddle.solved:
                    self.hint2_used = True
                    self.hints_used = 2             
                elif self.table_riddle.solved and not self.hint3_used: 
                    self.hint3_used = True
                    self.hints_used = 2
            elif self.hints_used == 2 and self.table_riddle.solved and not self.hint3_used:
                self.hint3_used = True
                self.hints_used = 3


                    
    def clear_room1(self): # clears the first room when room 2 is entered
        self.keypad = None
        self.recipe = None

    def draw(self):
        self.screen.blit(self.background_image, (0, 0))
        if self.door is not None:
            self.door.draw(self.screen)
        if self.recipe is not None:
            self.recipe.draw(self.screen)
        if self.keypad is not None:
            self.keypad.draw(self.screen)
        if self.room_number == 2:
            if self.poster is not None:
                self.poster.draw(self.screen)
            if self.table is not None:
                self.table.draw(self.screen)
            if self.table_riddle is not None:
                self.table_riddle.draw(self.screen)
            if self.table is not None and self.table_riddle is not None and self.table.open_drawer_clicked: # changing the drawing order to ensure visibility of objects
                self.table_riddle.draw(self.screen)
                self.table.draw(self.screen)
            if self.table is not None and self.table.book_taken and self.book is not None:
                self.book.draw(self.screen)
        if not self.end_of_game: # removes buttons when game is over
            if self.accessibility_activated == False:
                self.screen.blit(self.acc_button_off, (1100, 800)) # rendering this last ensures the accessibility button is drawn on top of other objects
            else:
                self.screen.blit(self.acc_button_on, (1100, 800))
            self.screen.blit(self.hint_button, (1200, 800))
        if self.room_number == 1:
            if self.hint_clicked:
                self.screen.blit(self.hint1, (350, 200))
        elif self.room_number == 2:
            if self.hint_clicked and self.table_riddle is not None:
                if not self.table_riddle.solved:
                    self.screen.blit(self.hint2, (350, 200))
                elif self.table_riddle.solved and self.poster is not None:
                    self.screen.blit(self.hint3, (350, 200))
            
                        
        total_seconds = self.elapsed_time // 1000
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60

        # Format the time string as "00:00:00"
        time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        
        if self.end_of_game:
            end_game_text = self.font.render("You have escaped!", True, (255, 0, 0))
            end_game_text2 = self.font.render(f"You took {minutes} minutes and {seconds} seconds to escape and used {self.hints_used} hints", True, (255, 0, 0))
            score_text = self.font.render(f"Your score is {self.score}", True, (255, 0, 0))
            self.screen.blit(end_game_text, (self.width // 2 - end_game_text.get_width() // 2, self.height // 2 - end_game_text.get_height() // 2))
            self.screen.blit(end_game_text2, (self.width // 2 - end_game_text2.get_width() // 2, (self.height // 2 - end_game_text2.get_height() // 2) + 50))
            self.screen.blit(score_text, (self.width // 2 - score_text.get_width() // 2, (self.height // 2 - score_text.get_height() // 2) + 100))
                     
        if not self.end_of_game:
            # Render and display the timer text
            timer_text = self.font.render(time_str, True, (255, 0, 0))
            self.screen.blit(timer_text, (10, 10))

            # Render and display the hint counter
            hint_counter_text = self.font.render(f"Hints Used: {self.hints_used}", True, (255, 0, 0))
            self.screen.blit(hint_counter_text, (10, 50))

        pg.display.flip()

    def update(self):
        if not self.end_of_game: #ensures timer only runs until the game is over
            self.elapsed_time += self.clock.get_time()
        if self.keypad is not None and self.keypad.entered_code == self.keypad.correct_code:
            self.door.toggle_open()
            self.background_image.fill((0, 0, 0))  # Fill the surface with black to only show the door
            self.clear_room1()
        if self.room_number == 2:
            if not self.room2_rendered: #ensure room only renders once
                self.update_room()
                self.room2_rendered = True
            elif self.table_riddle is not None and self.table is not None:
                if self.table_riddle.solved and self.table.drawer_locked:
                # Set drawer_locked to False when riddle is solved
                    self.table.drawer_locked = False 
            if self.poster is not None and self.poster.solved and self.table_riddle.solved:
                self.door.toggle_open()

    def game_over(self): # run at the end of game
        self.end_of_game = True
        self.background_image.fill((0,0,0))
        self.poster = None
        self.table = None
        self.book = None
        self.table_riddle = None
        self.door = None
        self.victory.play()
        self.scoring()

    #Score calculation
    def scoring(self):
        if self.elapsed_time < 300000: # score is based on time elapsed and number of hints used
            if self.hints_used == 0:
                self.score = "10/10"
            elif self.hints_used == 1:
                self.score = "9/10"
            elif self.hints_used == 2:
                self.score = "8/10"
            else:
                self.score = "7/10"
        elif self.elapsed_time > 300000 and self.elapsed_time < 450000:
            if self.hints_used == 0:
                self.score = "9/10"
            elif self.hints_used == 1:
                self.score = "8/10"
            elif self.hints_used == 2:
                self.score = "7/10"
            else:
                self.score = "6/10"
        elif self.elapsed_time > 450000 and self.elapsed_time < 600000:
            if self.hints_used == 0:
                self.score = "8/10"
            elif self.hints_used == 1:
                self.score = "7/10"
            elif self.hints_used == 2:
                self.score = "6/10"
            else:
                self.score = "5/10"
        elif self.elapsed_time >= 600000 and self.elapsed_time < 900000:
            if self.hints_used == 0:
                self.score = "7/10"
            elif self.hints_used == 1:
                self.score = "6/10"
            elif self.hints_used == 2:
                self.score = "5/10"
            else:
                self.score = "4/10"
        elif self.elapsed_time >= 900000 and self.elapsed_time < 1200000:
            if self.hints_used == 0:
                self.score = "6/10"
            elif self.hints_used == 1:
                self.score = "5/10"
            elif self.hints_used == 2:
                self.score = "4/10"
            else:
                self.score = "3/10"
        else:
            if self.hints_used == 0:
                self.score = "5/10"
            elif self.hints_used == 1:
                self.score = "4/10"
            elif self.hints_used == 2:
                self.score = "3/10"
            else:
                self.score = "2/10"         