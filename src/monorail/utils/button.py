import pygame as pg

from monorail.utils.asset_manager import Font


# the actual Button class
# it takes an action that is invoked when the player clicks it
class Button(pg.sprite.Sprite):
    font: pg.Font = Font.m_small.load()

    def __init__(self, pos, color, text, game, action):
        super().__init__(game.sprites)
        self.color = color
        self.action = action
        self.game = game
        self.text = text
        self.image: pg.Surface = pg.Surface((150, 40))
        self.rect: pg.Rect = self.image.get_rect(topleft=pos)
        self.fill_surf(self.color)

    def fill_surf(self, color):
        self.image.fill(pg.Color(color))
        self.image.blit(self.font.render(self.text, antialias=True, color=pg.Color('White')), (10, 10))

    def update(self, events, dt):
        self.fill_surf(self.color)
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    # if the player clicked the button, the action is invoked
                    self.action(self.game)
