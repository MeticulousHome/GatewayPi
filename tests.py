from functools import wraps
from threading import Thread
import time
from queue import Empty, Queue
import time
from queue import Empty, Queue
from threading import Thread

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivy.metrics import dp
from kivy.properties import StringProperty


from networking import is_wifi_connected, has_internet_connection,is_wireguard_connected


class TestResultWidget(MDBoxLayout):
    result = StringProperty("")
    status_text = StringProperty("")

    def __init__(self, test_function, test_name, **kwargs):
        super(TestResultWidget, self).__init__(**kwargs, result="Loading ↻", status_text="Loading")

        self.test_func = test_function
        self.test_name = test_name

        self.orientation = "horizontal"
        self.spacing = dp(10)

        self.test_name_label = MDLabel(
            text=self.test_name,
            font_name="NotoColorEmoji.ttf",
            theme_text_color="Primary",
            size_hint_y=None,
        )

        self.status_label = MDLabel(
            text=self.status_text,
            font_name="NotoColorEmoji.ttf",
            theme_text_color="Secondary",
            size_hint_y=None,
        )

        self.result_label = MDLabel(
            text=self.result, font_name="NotoColorEmoji.ttf", theme_text_color="Hint"
        )
        self.box = MDGridLayout(rows=2)
        self.box.add_widget(self.test_name_label)
        self.box.add_widget(self.status_label)
        self.add_widget(self.box)
        self.add_widget(self.result_label)

        self.bind(result=self.update_result)
        self.bind(status_text=self.update_status_text)

    def update_result(self, instance, value):
        self.result_label.text = value
        if value == "SUCCESS":
            self.result_label.on_theme_text_color(instance, "Primary")
        else:
            self.result_label.on_theme_text_color(instance, "Error")

    def update_status_text(self, instance, value):
        self.status_label.text = value


class Test:

    def __init__(self, test_function, test_name):
        self.test_function = test_function
        self.test_name = test_name
        self.widget: TestResultWidget = None

    def get_widget(self):
        self.widget = TestResultWidget(
            test_function=self.test_function, test_name=self.test_name
        )
        return self.widget


tests = []


# Decorator to register a test function
def register_test(test_func, test_name):
    @wraps(test_func)
    def wrapper(*args, **kwargs):
        return test_func(*args, **kwargs)

    tests.append(Test(test_function=wrapper, test_name=test_name))
    return wrapper


def get_all_tests():
    return tests


register_test(is_wifi_connected, "WIFI connection")
register_test(has_internet_connection, "Internet Connection")
register_test(is_wireguard_connected, "Wireguard Connection")

# Function to run a test with timeout
def run_test_with_timeout(test, timeout=10):
    result_queue = Queue()

    def target():
        result = test.test_function()
        result_queue.put(result)

    thread = Thread(target=target)
    thread.start()
    thread.join(timeout)

    if thread.is_alive():
        return False, f"Test '{test.__name__}' failed due to timeout."
    try:
        result = result_queue.get_nowait()
        return result
    except Empty:
        return False, f"Test '{test.__name__}' failed to produce a result."


# Function to run all tests every 10 seconds
def run_all_tests():
    tests = get_all_tests()
    print(f"Running all {len(tests)} Tests")
    while True:
        for test in tests:
            success, explanation = run_test_with_timeout(test)
            status = "SUCCESS" if success else "FAILURE"

            if success:
                test.widget.status_text = explanation
                test.widget.result = status
            else:
                test.widget.status_text = explanation
                test.widget.result = status

            print(f"Test '{test.test_function.__name__}': {status} - {explanation}")
        time.sleep(1)
