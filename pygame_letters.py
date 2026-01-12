import pygame

pygame.font.init()
font = pygame.font.Font("fonts/FreeSansBold.otf", 42)

class Letter:
    def __init__(self, text, bg_position):
        self.bg_color = "white"
        self.text_color = "black"
        self.bg_x = bg_position[0]
        self.bg_y = bg_position[1]

        self.bg_rect = pygame.Rect(self.bg_x, self.bg_y, 75, 75)
        self.text = text
        self.text_surface = None
        self.text_rect = None
        self._refresh_text()  # sagatavo renderi sākumā

    def _refresh_text(self):
        """Pārrenderē tekstu (sauc tikai tad, kad mainās text/color )."""
        if self.text:
            self.text_surface = font.render(self.text, True, pygame.Color(self.text_color))
            self.text_rect = self.text_surface.get_rect(center=self.bg_rect.center)
        else:
            self.text_surface = None
            self.text_rect = None

    def set_text (self, new_text):
        """Maina burtu un pārrenderē tikai tad, ja tiešām izmainījās."""
        new_text = new_text or ""
        if new_text != self.text:
            self.text = new_text
            self._refresh_text()

    def set_text_color(self, new_color):
        """Ja maina text_color, vajag pārrenderēt."""
        if new_color != self.text_color:
            self.text_color = new_color
            self._refresh_text()

    def draw_letter(self, surface):
        """Zīmē lauciņu uz padotā surface."""
        pygame.draw.rect(surface, pygame.Color(self.bg_color), self.bg_rect)
        pygame.draw.rect(surface, pygame.Color("#878a8c"), self.bg_rect, 3)

        if self.text_surface:
            surface.blit(self.text_surface, self.text_rect)

    def delete(self):
        """Burtu kvadrātu atbrīvo no vērtības"""
        self.set_text("")
