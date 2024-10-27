from kivy.app import App
from kivy.uix.button import Button

class KivyLearner(App):
    def build(self):
        return Button(text="Hello world", pos=(7,39), size=(100,100),size_hint=(.5,.5) # keep this to scale gracefully
        ) # Can take in image/text and display something 


if __name__=='__main__':
    KivyLearner().run()