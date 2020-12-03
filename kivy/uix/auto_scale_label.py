from kivy.metrics import sp
from kivy.properties import BooleanProperty, NumericProperty, StringProperty, ListProperty
from kivy.uix.label import Label


class AutoScaleLabel(Label):
    disable_auto_scale = BooleanProperty(False)

    allow_calculation = BooleanProperty(False)
    size_updates = NumericProperty(0)
    texture_scale = ListProperty(None, allownone=True)
    font_scale = NumericProperty(15.0)
    allow_regrab = BooleanProperty(False)
    old_text = StringProperty(None, allownone=True)

    def __init__(self, **kwargs):
        # self.allow_calculation = False
        # self.size_updates = 0
        # self.texture_scale = None
        # self.font_scale = 15.0
        # self.allow_regrab = False
        # self.old_text = None
        super().__init__(**kwargs)
        # print(self, 'Initalize a new label')

    # def __del__(self):
    #     print(self, 'Delete me')

    # def on_text(self, *args):
    #     if self.old_text is not None:
    #         self.old_text.replace('\n', ' ')
        # print(self, 'Text changed', self.old_text, '→', self.text.replace('\n', ' '))

    def on_texture_size(self, *args):
        # text = self.text.replace('\n', ' ')
        # print(self, f'"{text}"', 'texture update; font_size:', self.font_size, '; texture_size:', self.texture_size)
        if self.allow_calculation or self.allow_regrab:
            return
        self.allow_calculation = True
        if self.texture_scale is not None:
            self.font_scale = self.font_size
        self.texture_scale = self.texture_size[0], self.texture_size[1]
        self.calculate_font_size()

    def on_size(self, *args):
        self.size_updates += 1
        # text = self.text.replace('\n', ' ')
        # print(self, f'"{text}"', f'size update; number of size updates for this label {self.size_updates} ', '; size: (', self.size[0], self.size[1], '); saved texture_size:', self.texture_scale)

        if not self.allow_calculation:
            return
        if self.texture_scale is None:
            return
        self.calculate_font_size()

    def calculate_font_size(self):
        if self.disable_auto_scale:
            return
        if self.width in (0, 100) or self.height in (0, 100):
            return
        texture_width, texture_height = self.texture_scale[0], self.texture_scale[1]
        width, height = self.width, self.height
        if self.size_hint_x is None or self.size_hint_y is None:
            if self.size_hint_x is None:
                scale = 'height'
            else:
                scale = 'width'
        else:
            hs = (texture_width / texture_height * height) / width
            if hs < 1:  # If th=h, is w < w?
                scale = 'height'
            else:
                scale = 'width'
        if scale == 'height':
            font_size = round(self.font_scale / texture_height * height, 2)
        else:
            font_size = round(self.font_scale / texture_height * (texture_height / texture_width * width), 2)
        if font_size < 10 or font_size == self.font_size:
            return
        self.font_size = font_size
        # text = self.text.replace('\n', ' ')
        # print(self, f'\t→ text:"{text}"', 'font size changed; scaling by', scale, '; new font size:', font_size)
