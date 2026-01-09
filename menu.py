from time import sleep
import pygame
import pygame_menu
from pygame_menu import themes
from game import run_game
 
pygame.init()
surface = pygame.display.set_mode((600, 400))

selector_sound = pygame.mixer.Sound('sounds/cursor.wav')

def start_the_game():
    selector_sound.play()

    progress = loading.get_widget("1") 
    progress.set_value(0) #reseto, lai atgriežoties atpakaļ un spiežot play no jauna, nepaliek loading sceen uz 100%

    mainmenu._open(loading)
    pygame.time.set_timer(update_loading, 30)


REVEAL = 0 #glabās izvēlēto pakāpi: cik daudz burtus atklāt.

def set_difficulty(*args, **kwargs):
    global REVEAL
    selected_item, index = difficulty_selector.get_value()
    REVEAL = selected_item[1]  #paņem otro no touple
    selector_sound.play()


mainmenu = pygame_menu.Menu('WORDLE game', 600, 400, theme=themes.THEME_SOLARIZED)
mainmenu.add.text_input('Name: ', default='username')

difficulty_selector = mainmenu.add.selector(
    'Difficulty :',
    [('Hard (no hint)', 0), ('Moderate(first letter)', 1), ('Easy(first 2 letters)', 2) ],
onchange=set_difficulty)

difficulty_selector._select= True 
    
mainmenu.add.button('Play', start_the_game)
mainmenu.add.button('Quit', pygame_menu.events.EXIT)

loading = pygame_menu.Menu('Loading the Game...', 600, 400, theme=themes.THEME_DARK)
loading.add.progress_bar("Progress", progressbar_id = "1", default=0, width = 200, )
 
arrow = pygame_menu.widgets.LeftArrowSelection(arrow_size = (10, 15))
 
update_loading = pygame.USEREVENT + 0

last_selected_index = difficulty_selector.get_index()
last_selected_widget = None
 
while True:
    events = pygame.event.get()
    for event in events:
        if event.type == update_loading:
            progress = loading.get_widget("1")
            progress.set_value(min(100, progress.get_value() + 1))
            if progress.get_value() == 100:
                pygame.time.set_timer(update_loading, 0)

                #Jo ielādēja tikai līdz 99 un palaida režģi
                loading.draw(surface)
                pygame.display.update()

                # Palaiž režģi (spēles ekrānu)
                result = run_game(surface, REVEAL)
                if result == "quit":
                    pygame.quit()
                    raise SystemExit

                # Ar ESC, atgriezties uz menu.. nestrādā
                loading._open(mainmenu)
                progress.set_value(0)

        if event.type == pygame.QUIT:
            exit()
    current_widget = mainmenu.get_current().get_selected_widget() if mainmenu.get_current() else None
    
    # Atskaņo skaņas efektus katru reizi, kad kaut ko izvēlās
    if current_widget and current_widget != last_selected_widget:
        if current_widget != difficulty_selector:
            selector_sound.play()
        last_selected_widget = current_widget
 
    if mainmenu.is_enabled():
        mainmenu.update(events)
        mainmenu.draw(surface)
        if (mainmenu.get_current().get_selected_widget()):
            arrow.draw(surface, mainmenu.get_current().get_selected_widget())
 
    pygame.display.update()