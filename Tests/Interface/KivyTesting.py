from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.boxlayout import BoxLayout

class TestApp(App):
    def build(self):
        layout = GridLayout(cols = 1, spacing = 10, padding = 10)

        # Title Label
        titleLabel = Label(text = 'Study-Bot', font_size = 24)
        layout.add_widget(titleLabel)

        # Dropdown Menu
        dropdown = DropDown()
        options = ['Human Body', 'Krebs Cycle']
        for option in options:
            btn = Button(
                text=option, size_hint_y = None, height = 30,
                background_color = (0.392, 0.278, 0.200, 1), size_hint_x = None, width = 150
            )
            btn.bind(on_release = lambda btn_option: dropdown.select(btn_option.text))
            dropdown.add_widget(btn)

        dropdownButton = Button(
            text = 'Select an option', size_hint_y = None, height = 30, 
            size_hint_x = None, width = 150
        )
        dropdownButton.bind(on_release = dropdown.open)
        dropdown.bind(on_select = lambda instance, x: setattr(dropdownButton, 'text', x))


        # Three Buttons with left margin and reduced vertical spacing
        buttonLayout = BoxLayout(padding = (20, 0), spacing = 50)  # Add left margin and reduce vertical spacing
        button1 = Button(
            text = 'Select', size_hint_y = None, height = 30,
            background_color = (0.885, 1, 0.689, 1), size_hint_x = None, width = 150
        )
        button2 = Button(
            text = 'Ask question', size_hint_y = None, height = 30,
            background_color = (1, 1, 1, 1), size_hint_x = None, width = 150
        )
        button3 = Button(
            text = 'Exit', size_hint_y = None, height = 30,
            background_color = (0.572, 0.188, 0.188, 1), size_hint_x = None, width = 150
        )
        
        buttonLayout.add_widget(dropdownButton)
        buttonLayout.add_widget(button1)
        buttonLayout.add_widget(button2)
        buttonLayout.add_widget(button3)

        layout.add_widget(buttonLayout)

        text = """Welcome to Study-Bot! Please select a topic before asking a question."""

        # Variable Text Display Element
        variableText = Label(text = text)
        layout.add_widget(variableText)

        return layout

TestApp().run()