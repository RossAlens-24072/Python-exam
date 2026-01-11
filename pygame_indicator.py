# import pygame
# from pygame_letters import Letter

# screen = pygame.display.set_mode((633, 900))
# font = pygame.font.Font("fonts/FreeSansBold.otf")

# class Indicator:
#     def __init__(self, x, y, letter):
#         self.x = x
#         self.y = y
#         self.text = letter
#         self.rect(self.x, self.y, 57, 75)
#         self.bg_color = "#d3d6da"

#     def draw(self):
#         """Funkcija, kas novieto indikatoru attiecīgajā vietā un ieraksta burtu"""
#         pygame.draw.rect(screen, self.bg_color, self.rect)
#         self.text_surface = font.render(self.text, True, "white")
#         self.text_rect = self.text_surface.get_rect(center=(self.x+27, self.y+30))
#         screen.blit(self.text_surface, self.text_rect)
#         pygame.display.update()