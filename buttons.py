from pygame import SYSTEM_CURSOR_HAND


def button_img(self, baseimage, callback, *args, is_float=True):
    btn = self.add.button(' ', callback, *args, cursor=SYSTEM_CURSOR_HAND, selection_effect=None)
    if is_float:
        btn.set_float(True, origin_position=True)
    width, height = baseimage.get_size()
    btn.resize(width, height)
    decorator = btn.get_decorator()
    decorator.add_baseimage(0, 0, baseimage, centered=True)
    return btn
