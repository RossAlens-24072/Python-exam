import pygame
from gamelogic import Wordle
from pygame_letters import Letter

def run_game(surface, reveal):
    game_lost_sound = pygame.mixer.Sound('sounds/gamelost.wav')
    victory_sound = pygame.mixer.Sound('sounds/victory.mp3')
    grid = []
    row = 0
    wordle = Wordle(reveal=reveal)
    print(f"Debug - atbilde:{wordle.answer}")

    current_input = ""

    #kamēr spēles cikls izpildās, tikmēr tiek zīmēts režģis
    running = True
    game_over = False

    score = 0
    message = ""
    ui_font = pygame.font.Font("fonts/FreeSansBold.otf", 28)

    tile = 75
    step = 85
    gap = step - tile

    W, H = surface.get_size()

    grid_w = 5 * tile + 4 * gap
    grid_h = 6 * tile + 5 * gap

    start_x = (W - grid_w)//2
    start_y = (H - grid_h)//2

    for r in range(6):
        grid_row = []
        for c in range(5):
            x = start_x + c * step
            y = start_y + r * step
            grid_row.append(Letter("", (x, y)))
        grid.append(grid_row)

    def apply_easy_hint():
        """Funcija, kas paredzēta izsaukšanai spēles sākumā un pēc raunda restartēšanas, lai parādītu atklātos burtus un krāsas"""
        nonlocal current_input #mainīgais, kas atrodas run_game() funkcijā
        if wordle.difficulty == "easy":
            hint = wordle.get_hint()
            if hint:
                for i, j in enumerate(hint):
                    grid[0][i].set_text(j.upper())
                    grid[0][i].set_text_color("black")
                    current_input += j.lower()
    
    def restart_round():
        """Funkcija raunda restartēšanai, jauna vārda ģenerēšanai"""
        nonlocal wordle, row, current_input, game_over, message
        wordle = Wordle(reveal=reveal)
        print(f"Debug - atbilde:{wordle.answer}")

        #Notīra visu režģi
        for r in range(6):
            for c in range(5):
                grid[r][c].bg_color = "white"
                grid[r][c].set_text_color("black")
                grid[r][c].set_text("")

        #Atjauno mainīgos
        row = 0
        current_input = ""
        game_over = False
        message = ""
        #message_timer = 0

        apply_easy_hint()

    # ieliek hintu pirmajā raundā
    apply_easy_hint()

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Aizver visu programmu
                return "quit"
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Atgriezties uz menu
                    return "back"
                
                if game_over and event.key == pygame.K_RETURN:
                    restart_round()
                    continue

                if game_over:
                    continue

                # Burta nodzēšana
                if event.key == pygame.K_BACKSPACE and len(current_input) > 0:
                    col = len(current_input) - 1
                    current_input = current_input[:-1]
                    grid[row][col].set_text("")
                    continue

                # Minējuma iesniegšana ar "enter"
                if event.key == pygame.K_RETURN and len(current_input) ==5:
                    wordle.guesses.add_attempt(current_input)
                    
                    result = wordle.evaluate_guess(current_input)
                        
                    for i in range(5):
                        box = grid[row][i]
                        if result[i] == "Green":
                           box.bg_color = "#6aaa64"
                        elif result[i] == "Yellow":
                            box.bg_color = "#c9b458"
                        else:
                            box.bg_color = "#787c7e"

                        box.set_text_color("black")
                    
                    # Paziņojums par uzvaru vai zaudējumu un punktiem.
                    if current_input == wordle.answer:
                        tries = row + 1
                        score += (7-tries)
                        victory_sound.play()
                        message = f"Correct! Attempts: {tries}. Press ENTER to continue."
                        game_over = True
                    else:
                        row += 1
                        current_input = ""
                        if row >=6:
                            game_lost_sound.play()
                            message = f"You lost! Word:{wordle.answer.upper()}. Press ENTER to continue."
                            game_over = True
                    continue

                #Rakstīšana
                if event.unicode and event.unicode.isalpha() and len(current_input) < 5:
                    col = len(current_input)
                    grid[row][col].set_text(event.unicode.upper())
                    current_input += event.unicode.lower()
                   
        #Nodzēš iepriekšējo "loding" ekrānu un uzliek melnu fonu
        surface.fill((20, 20, 20))

        # Paziņojuma attēlošana
        surface.blit(ui_font.render(f"Score: {score}", True, (230, 230, 230)), (20,20)) #uztaisa attēlu ar pelēku paziņojuma tekstu
        if message:
            surface.blit(ui_font.render(message, True, (255, 255, 255)), (20, 55))
   
        for r in range(6):
            for c in range(5):
                grid[r][c].draw_letter(surface)
        pygame.display.flip()
