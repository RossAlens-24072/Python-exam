from time import sleep
import pygame
import pygame_menu
from pygame_menu import themes
from game import run_game
 
pygame.init()
surface = pygame.display.set_mode((700, 700))

selector_sound = pygame.mixer.Sound('sounds/cursor.wav')

STATE_MENU = "menu"
STATE_LOADING = "loading"
STATE_GAME = "game"

state = STATE_MENU

def start_the_game():
    """Funkcija, kas uzsāk lādēšanās procesu spēles palaišanai"""
    global state
    selector_sound.play()

    progress = loading.get_widget("1") 
    progress.set_value(0) #reseto, lai atgriežoties atpakaļ un spiežot play no jauna, nepaliek loading sceen uz 100%
    state = STATE_LOADING
    pygame.time.set_timer(update_loading, 30)


REVEAL = 0 #glabās izvēlēto pakāpi: cik daudz burtus atklāt.

def set_difficulty(*args, **kwargs):
    """Funkcija, kas ļauj uzstādīt grūtības pakāpi"""
    global REVEAL
    selected_item, index = difficulty_selector.get_value()
    REVEAL = selected_item[1]  #paņem otro no touple
    selector_sound.play()


mainmenu = pygame_menu.Menu('WORDLE game', 700, 700, theme=themes.THEME_SOLARIZED)

difficulty_selector = mainmenu.add.selector(
    'Difficulty :',
    [('Hard (no hints and colors)', 0), ('Standard', 1), ('Easy(first letter is shown)', 2) ],
onchange=set_difficulty)

difficulty_selector._select= True 
    
mainmenu.add.button('Play', start_the_game)
mainmenu.add.button('Quit', pygame_menu.events.EXIT)

loading = pygame_menu.Menu('Loading the Game...', 700, 700, theme=themes.THEME_DARK)
loading.add.progress_bar("Progress", progressbar_id = "1", default=0, width = 200, )
 
arrow = pygame_menu.widgets.LeftArrowSelection(arrow_size = (10, 15))
 
update_loading = pygame.USEREVENT + 0

last_selected_index = difficulty_selector.get_index()
last_selected_widget = None
 
while True:
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        
        if state == STATE_LOADING and event.type == update_loading:
            progress = loading.get_widget("1")
            progress.set_value(min(100, progress.get_value() + 1))

            if progress.get_value() == 100:
                pygame.time.set_timer(update_loading, 0)
                state = STATE_GAME
        
        # Menu sadaļa
        if state == STATE_MENU:
            previous_selected = last_selected_widget

            mainmenu.update(events)
            mainmenu.draw(surface)

            current = mainmenu.get_selected_widget()
            if current and current != previous_selected:
                selector_sound.play()
                last_selected_widget = current
            if current and last_selected_widget is None:
                last_selected_widget = current
                
            if current:
                arrow.draw(surface, current)
        
        # Loading sadaļa
        elif state == STATE_LOADING:
            loading.update(events)
            loading.draw(surface)

        # Spēles sadaļa
        elif state == STATE_GAME:
            result = run_game(surface, REVEAL)

            if result == "quit":
                pygame.quit()
                raise SystemExit
            
            if result == "back":
                state = STATE_MENU
                mainmenu.enable()

        pygame.display.flip()