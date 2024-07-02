from threading import Thread
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.metrics import dp
import logging

from .tests import get_all_tests, run_all_tests

from kivy.core.window import Window

Window.maximize()


class GatewayApp(MDApp):

    def build(self):
        self.layout = MDBoxLayout(orientation="vertical", padding=dp(20))
        for test in get_all_tests():
            logging.info(f"Adding widget: {test}")
            self.layout.add_widget(test.get_widget())

        return self.layout

    def run(sef):
        thread = Thread(target=run_all_tests, daemon=True)
        thread.start()

        super().run()


def main():
    GatewayApp().run()


# Run all tests every 10 seconds
if __name__ == "__main__":
    main()
