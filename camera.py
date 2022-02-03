import pygame


class CameraAwareGroup(pygame.sprite.Group):
    def camera_draw(self, surface, camera):
        sprites = self.sprites()
        if hasattr(surface, "blits"):
            self.spritedict.update(
                zip(sprites, surface.blits((spr.image, spr.rect.move(camera)) for spr in sprites))
            )
        else:
            for spr in sprites:
                self.spritedict[spr] = surface.blit(spr.image, spr.rect.move(camera))
        self.lostsprites = []
        dirty = self.lostsprites

        return dirty
