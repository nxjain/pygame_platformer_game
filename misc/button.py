import pygame


class Button:
    """The object for creating a clickable button with text"""
    # fgc = foreground colour, bgc = background colour
    def __init__(self, x, y, width, height, fg_colour, bg_colour, content, fontsize):
        self.font = pygame.font.Font("courier.ttf", fontsize)
        self.width = width
        self.height = height

        # Building the box for the button:
        self.image = pygame.Surface((width, height))
        self.image.fill(bg_colour)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Building the text for the button:
        self.content = content  # the words on the button
        self.text = self.font.render(content, True, fg_colour)  # the text being made into a displayable object
        self.text_rect = self.text.get_rect(center=(width/2, height/2))

        self.image.blit(self.text, self.text_rect)  # actually displays them onto the screen

    def is_pressed(self, mouse_pos, pressed) -> bool:
        """Detects whether the button has been clicked or not"""
        if self.rect.collidepoint(mouse_pos):
            if pressed[0]:
                return True
        return False
