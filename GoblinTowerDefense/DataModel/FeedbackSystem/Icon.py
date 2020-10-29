import pygame


class Icon(pygame.sprite.Sprite):
    def __init__(self, img_file, img_idx, x, y, size):
        super().__init__()
        self.image = pygame.image.load(img_file)
        self.image = pygame.transform.scale(self.image, (size[0], size[1]))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.size = size
        self.img_idx = img_idx

    def on_click(self, click_pos):
        if ((click_pos[0] > self.rect.x) and (click_pos[0] < self.rect.x + self.size[0])) and (
                (click_pos[1] > self.rect.y) and (click_pos[1] < self.rect.y + self.size[1])):
            return self.img_idx
        else:
            return None
