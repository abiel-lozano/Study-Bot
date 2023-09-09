from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.spinner import Spinner

class TestApp(App):
	def build(self):
		layout = GridLayout(cols=1, spacing=10, padding=10)

		# Title Label
		title_label = Label(text='Study-Bot', font_size=24)
		layout.add_widget(title_label)

		# Dropdown with three options
		dropdown = DropDown()
		options = ['Human Body', 'Krebs Cycle']
		for option in options:
			btn = Button(text=option, size_hint_y=None, height=30, background_color=(0.392, 0.278, 0.200, 1))
			btn.bind(on_release=lambda btn_option: dropdown.select(btn_option.text))
			dropdown.add_widget(btn)

		dropdown_button = Button(text='Select an option', size_hint_y=None, height=30)
		dropdown_button.bind(on_release=dropdown.open)
		dropdown.bind(on_select=lambda instance, x: setattr(dropdown_button, 'text', x))

		layout.add_widget(dropdown_button)

		# Three Buttons
		button1 = Button(text='Select', size_hint_y=None, height=30, background_color=(0.345, 0.482, 0.149, 1))
		button2 = Button(text='Ask question', size_hint_y=None, height=30, background_color=(0.498, 0.392, 0.149, 1))
		button3 = Button(text='Exit', size_hint_y=None, height=30, background_color=(0.572, 0.188, 0.188, 1))
		
		layout.add_widget(button1)
		layout.add_widget(button2)
		layout.add_widget(button3)

		text = """Stomach: The stomach is an organ located in the upper abdomen that plays a vital role in 
the digestion of food. Its main function is to store and break down food into smaller 
particles through the process of mechanical and chemical digestion. The stomach secretes 
gastric juices, including hydrochloric acid and enzymes, which help in the breakdown of 
proteins. It also mixes the partially digested food with these juices to form a 
semi-liquid mixture called chyme, which is then gradually released into the small 
intestine for further digestion and absorption."""

		# Variable Text Display Element
		variable_text = Label(text=text)
		layout.add_widget(variable_text)

		return layout

if __name__ == '__main__':
	TestApp().run()
