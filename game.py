import pygame
from gamelogic import Wordle
from pygame_letters import Letter

TOP = 40
LEFT = 60

def run_game(surface, reveal):

    grid = []
    row = 0
    wordle = Wordle(reveal=reveal)

    current_input = ""
    #kamēr spēles cikls izpildās, tikmēr tiek zīmēts režģis
    running = True
    game_over = False

    start_x = 40
    start_y = 100

    for r in range(6):
        grid_row = []
        for c in range(5):
            x = start_x + c * 85
            y = start_y + r * 85
            grid_row.append(Letter("", (x, y)))
        grid.append(grid_row)

    while running:
        surface.fill("white")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Aizver visu programmu
                return "quit"
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Atgriezties uz menu
                    return "back"
                
                if game_over:
                    continue

                #Rakstīšana
                if event.unicode.isalpha() and len(current_input) < 5:
                    col = len(current_input)
                    letter = event.unicode.upper()
                    grid[row][col].text = letter
                    grid[row][col].draw_letter()
                    current_input += event.unicode.lower()

                # Burta nodzēšana
                if event.key == pygame.K_BACKSPACE and len(current_input) > 0:
                    col = len(current_input) - 1
                    current_input = current_input[:-1]
                    grid[row][col].text = ""
                    grid[row][col].draw_letter()


                # Minējuma iesniegšana ar "enter"
                if event.key == pygame.K_RETURN:
                    if len(current_input) == 5:
                        result = wordle.evaluate_guess(current_input)
                        
                        for i in range(5):
                            box = grid[row][i]
                        if result[i] == "Green":
                            box.bg_color = "#6aaa64"
                        elif result[i] == "Yellow":
                            box.bg_color = "#c9b458"
                        else:
                            box.bg_color = "#787c73"

                        box.text_color = "white"
                        box.draw_letter()

                    if current_input == wordle.answer:
                        game_over = True
                    else:
                        row += 1
                        current_input = ""
            pygame.display.update()
                # Pievieno burtu minējumam        

        #Nodzēš iepriekšējo "loding" ekrānu un uzliek melnu fonu
        # surface.fill((20, 20, 20))