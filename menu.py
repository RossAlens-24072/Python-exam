from time import sleep
import pygame
import pygame_menu
from pygame_menu import themes
 
pygame.init()
surface = pygame.display.set_mode((600, 400))

selector_sound = pygame.mixer.Sound('sounds/cursor.wav')

REVEAL = 0 #glabās izvēlēto pakāpi: cik daud zburtus atklāt.
def set_difficulty(value, difficulty):
    global REVEAL
    REVEAL = value

def start_the_game():
    selector_sound.play()
    mainmenu._open(loading)
    pygame.time.set_timer(update_loading, 30)


def set_difficulty(value, difficulty):
    """Funkcija, kas ļauj lietotājam izvēlēties spēles grūtības pakāpi"""
    global REVEAL # galbās izvēlēto grūtības pakāpi
    REVEAL = difficulty
    selector_sound.play()


mainmenu = pygame_menu.Menu('WORDLE game', 600, 400, theme=themes.THEME_SOLARIZED)
mainmenu.add.text_input('Name: ', default='username')

difficulty_selector = mainmenu.add.selector(
    'Difficulty :',
    [('Hard (no hint)', 1), ('Moderate(first letter)', 2), ('Easy(first 2 letters)', 3) ],
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
            progress.set_value(progress.get_value() + 1)
            if progress.get_value() == 100:
                pygame.time.set_timer(update_loading, 0)
        if event.type == pygame.QUIT:
            exit()
    current_widget = mainmenu.get_current().get_selected_widget() if mainmenu.get_current() else None
    
    # Atskaņo skaņu, kad maina grūtības pakāpi
    if current_widget == difficulty_selector:
        current_index = difficulty_selector.get_index()
        if current_index != last_selected_index:
            selector_sound.play()
            last_selected_index = current_index
    
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