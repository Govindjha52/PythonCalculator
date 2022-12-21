from kivy.config import Config

Config.set("input", "mouse", "mouse,disable_multitouch")
Config.set("graphics", "height", 500)
Config.set("graphics", "width", 420)
Config.set("graphics", "resizable", 1)
Config.write()

from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivymd.uix.button import MDFlatButton
from kivymd.uix.button import MDRaisedButton
from kivy.properties import ListProperty
from kivymd.uix.list import TwoLineListItem
from math import sin, cos, tan, log, log10, factorial, sqrt

fact = factorial
kv = """
MDBoxLayout:
    orientation:"vertical"
    padding:(5,5,5,5)
    spacing:2
    ScrollView:
        MDList:
            id:container_history
            size_hint_y:None
    TextInput:
        id:txt_equation
        size_hint_y:None
        height:50
        font_size:32
        background_color:(0,0,0,0)
        foreground_color:(1,1,1,1)
        cursor_color:(1,1,1,1)
        on_text_validate: app.calculate()
        on_touch_up: app.set_selection()
        text_validate_unfocus:False
        multiline:False
        on_focus : if not self.focus and app.selection_coordinate:self.select_text(app.selection_coordinate[0],app.selection_coordinate[1])
    PageLayout:
        border:20
        MDGridLayout:
            id: grid
            cols:4
            spacing:2
        MDGridLayout:
            id:grid_function
            md_bg_color: app.theme_cls.primary_color
            cols:3
"""


class Calculator(MDApp):
    selection_coordinate = ListProperty()
    history = set()
    functions = [
        "sin",
        "cos",
        "tan",
        "pow",
        "sqrt",
        "sum",
        "log",
        "log10",
        "fact",
        "(",
        ")",
        ",",
    ]

    def set_selection(self):
        self.selection_coordinate = (
            self.root.ids.txt_equation.selection_from,
            self.root.ids.txt_equation.selection_to,
        )

    def restore_history(self, instance, touch):
        self.root.ids.txt_equation.text = instance.text

    def calculate(self, *args):
        txt_equation = self.root.ids.txt_equation
        if txt_equation.text:
            equation = txt_equation.text.replace("x", "*")
            answer = str(eval(equation))
            if txt_equation.text not in self.history:
                self.root.ids.container_history.add_widget(
                    TwoLineListItem(
                        text=txt_equation.text,
                        secondary_text="Answer " + answer,
                        on_touch_down=self.restore_history,
                    )
                )
                self.history.add(txt_equation.text)
            txt_equation.text = answer
        txt_equation.focus = True

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Purple"
        # self.theme_cls.primary_hue = "900"
        root = Builder.load_string(kv)
        buttons = (
            "AC",
            "Del",
            "%",
            "+",
            "7",
            "8",
            "9",
            "/",
            "4",
            "5",
            "6",
            "-",
            "1",
            "2",
            "3",
            "x",
            "00",
            "0",
            ".",
            "=",
        )

        grid = root.ids.grid
        grid_function = root.ids.grid_function
        for button_text in buttons:
            if button_text == "=":
                grid.add_widget(
                    MDRaisedButton(
                        text=button_text,
                        font_size="16sp",
                        on_release=self.calculate,
                    )
                )
                continue

            grid.add_widget(
                MDFlatButton(
                    text=button_text,
                    on_release=self.button_released,
                    size_hint=(1, 1),
                    font_size="16sp",
                )
            )
        for function in self.functions:
            grid_function.add_widget(
                MDFlatButton(
                    text=function,
                    on_release=self.button_released,
                    size_hint=(1, 1),
                    font_size="16sp",
                )
            )
        root.ids.txt_equation.focus = True
        return root

    def button_released(self, instance):
        txt_equation = self.root.ids.txt_equation
        if instance.text == "=":
            self.calculate()
        elif instance.text == "AC":
            txt_equation.text = ""
        elif instance.text == "Del":
            if txt_equation.selection_text:
                txt_equation.delete_selection()
            else:
                txt_equation.do_backspace()
        elif instance.text in self.functions[:9]:
            print(instance.text)
            txt_equation.insert_text(instance.text + "(")
        else:
            txt_equation.insert_text(instance.text)
        self.root.ids.txt_equation.focus = True


if __name__ == "__main__":
    Calculator().run()
