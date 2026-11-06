
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.popup import Popup

Window.clearcolor = (0.04, 0.06, 0.10, 1)


class SecurityLabApp(App):

    def build(self):
        root = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=15
        )

        title = Label(
            text="L WIFI SECURITY LAB",
            font_size=25,
            bold=True,
            size_hint_y=None,
            height=65
        )

        subtitle = Label(
            text="Your Personal Security Learning Toolkit",
            font_size=14,
            size_hint_y=None,
            height=40
        )

        root.add_widget(title)
        root.add_widget(subtitle)

        scroll = ScrollView()

        tools = BoxLayout(
            orientation="vertical",
            spacing=12,
            size_hint_y=None
        )

        tools.bind(
            minimum_height=tools.setter("height")
        )

        features = [
            "PMK Generation",
            "Password Testing Simulation",
            "MIC Verification",
            "WPA2 Handshake Theory",
            "Password Strength Checker",
            "Password Generator",
            "Dictionary Analysis",
            "Hash Comparison",
            "Password Security Analyzer",
            "Security Report"
        ]

        for feature in features:
            btn = Button(
                text=feature,
                size_hint_y=None,
                height=65,
                background_normal="",
                background_color=(0.10, 0.30, 0.45, 1)
            )

            btn.bind(
                on_release=lambda instance, name=feature: self.open_tool(name)
            )

            tools.add_widget(btn)

        scroll.add_widget(tools)
        root.add_widget(scroll)

        return root

    def open_tool(self, name):
        content = Label(
            text=name + "\n\nFeature selected!",
            font_size=18
        )

        popup = Popup(
            title="L WiFi Security Lab",
            content=content,
            size_hint=(0.85, 0.35)
        )

        popup.open()


if __name__ == "__main__":
    SecurityLabApp().run()

