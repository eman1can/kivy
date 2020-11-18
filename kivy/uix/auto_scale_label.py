from kivy.properties import OptionProperty, BooleanProperty
from kivy.uix.label import Label


class AutoScaleLabel(Label):
    scale_by = OptionProperty('width', options=['width', 'height'])
    disable_auto_scale = BooleanProperty(False)
    scale_lock = BooleanProperty(False)

    def __init__(self, **kwargs):
        self.sw, self.sh = None, None
        self.fs = None
        super().__init__(**kwargs)

    def on_width(self, *args):
        if self.size_hint_x is None:
            return
        self.calculate_font_size()

    def on_height(self, *args):
        if self.size_hint_y is None:
            return
        if self.size_hint_x is not None:
            return
        self.calculate_font_size()

    def on_texture_size(self, *args):
        if self.sw is not None:
            return
        if self.texture_size == [0, 0]:
            return
        self.sw, self.sh = self.texture_size
        self.fs = self.font_size

    def calculate_font_size(self):
        if self.disable_auto_scale:
            return
        if self.sw is None:
            return
        ws = (self.sh / self.sw * self.width)
        hs = (self.sw / self.sh * self.height)
        ws /= self.width
        hs /= self.height
        if self.size_hint_x is None or self.size_hint_y is None:
            if self.size_hint_x is None:
                scale = 'height'
            else:
                scale = 'width'
        else:
            if ws < 1 and hs < 1:  # Both can be used
                if ws > hs:  # Use the one that will scale less
                    scale = 'width'
                else:
                    scale = 'height'
            elif ws < 1:  # Width is only option
                scale = 'width'
            else:  # Height is only option
                scale = 'height'
        if scale == 'height':
            font_size = round(self.fs / self.sh * self.height, 2)
        else:
            font_size = round(self.fs / self.sw * self.width, 2)
        if self.font_size != font_size:
            self.font_size = font_size
        del font_size