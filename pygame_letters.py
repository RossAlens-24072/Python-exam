from gamelogic import Wordle
import pygame

# Konstantes
screen = pygame.display.set_mode((633, 900))
font = pygame.font.Font("fonts/FreeSansBold.otf")

class Letter:
    def __init__(self, text, bg_position):
        self.bg_color = "white"
        self.text_color = "black"
        self.bg_position = bg_position
        self.bg_x = bg_position[0]
        self.bg_y = bg_position[1]
        self.bg_rect = (bg_position[0], self.bg_y, 75, 75)
        self.text = text
        self.text_position = (self.bg_x+36, self.bg_position[1]+34)
        self.text_surface = font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.text_position)

    def draw_letter(self):
        """Funkcija, kas ievieto burtus uz ekrāna attiecīgajās vietās"""            
        pygame.draw.rect(screen, self.bg_color, self.bg_rect)
        if self.bg_color == "white":
            pygame.draw.rect(screen, "#878a8c", self.bg_rect, 3) #uztaisam taisnstūri
        self.text_surface = font.render(self.text, True, self.text_color)
        screen.blit(self.text_surface, self.text_rect)
        pygame.display.update()

    def delete(self):
        """Burtu kvadrātu atbrīvo no vērtības"""
        pygame.draw.rect(screen, "white", self.bg_rext)
        pygame.draw.rect(screen, "#d3d6da", self.bg_rect, 3)
        pygame.display.update()