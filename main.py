import hashlib
import hmac
import secrets
import string
import os
from datetime import datetime

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView

Window.clearcolor = (0.04, 0.06, 0.10, 1)

SSID = "MyWiFiLab"


class SecurityLabApp(App):

    def build(self):
        root = BoxLayout(
            orientation="vertical",
            padding=15,
            spacing=10
        )

        root.add_widget(Label(
            text="[b]L WIFI SECURITY LAB[/b]",
            markup=True,
            font_size=25,
            size_hint_y=None,
            height=55
        ))

        root.add_widget(Label(
            text="Educational WPA2 Security Toolkit",
            font_size=14,
            size_hint_y=None,
            height=35
        ))

        scroll = ScrollView()
        tools = BoxLayout(
            orientation="vertical",
            spacing=10,
            size_hint_y=None
        )
        tools.bind(minimum_height=tools.setter("height"))

        features = [
            ("PMK Generation", self.pmk),
            ("Password Testing Simulation", self.password_test),
            ("MIC Verification", self.mic_test),
            ("WPA2 Handshake Theory", self.handshake),
            ("Password Strength Checker", self.strength),
            ("Password Generator", self.generator),
            ("Dictionary Analysis", self.dictionary),
            ("Hash Comparison", self.hash_compare),
            ("Password Security Analyzer", self.analyzer),
            ("Security Report", self.report)
        ]

        for name, function in features:
            btn = Button(
                text=name,
                size_hint_y=None,
                height=60,
                background_normal="",
                background_color=(0.10, 0.30, 0.45, 1)
            )
            btn.bind(on_release=lambda instance, fn=function: fn())
            tools.add_widget(btn)

        scroll.add_widget(tools)
        root.add_widget(scroll)
        return root

    def show(self, title, message):
        box = BoxLayout(orientation="vertical", padding=12, spacing=10)
        output = TextInput(
            text=str(message),
            readonly=True,
            multiline=True,
            size_hint_y=1
        )
        close = Button(text="Close", size_hint_y=None, height=48)
        box.add_widget(output)
        box.add_widget(close)

        popup = Popup(
            title=title,
            content=box,
            size_hint=(0.92, 0.75)
        )
        close.bind(on_release=popup.dismiss)
        popup.open()

    def ask(self, title, prompt, callback, password=False):
        box = BoxLayout(orientation="vertical", padding=12, spacing=10)
        box.add_widget(Label(text=prompt, size_hint_y=None, height=45))

        field = TextInput(
            multiline=False,
            password=password,
            size_hint_y=None,
            height=48
        )
        box.add_widget(field)

        submit = Button(text="Continue", size_hint_y=None, height=48)
        box.add_widget(submit)

        popup = Popup(title=title, content=box, size_hint=(0.9, 0.4))

        def run(instance):
            value = field.text
            popup.dismiss()
            callback(value)

        submit.bind(on_release=run)
        popup.open()

    def pmk(self):
        self.ask("PMK Generation", "Enter an educational test password:",
                 self.make_pmk, True)

    def make_pmk(self, password):
        if not password:
            return
        pmk = hashlib.pbkdf2_hmac(
            "sha1", password.encode(), SSID.encode(), 4096, dklen=32
        )
        self.show("PMK Result", "Demo SSID: " + SSID +
                  "\n\nPMK:\n" + pmk.hex())

    def password_test(self):
        self.show(
            "Password Testing Simulation",
            "Offline educational demonstration only.\n\n"
            "This tool uses a fixed dummy password and the local "
            "passwords.txt file. It does not test Wi-Fi networks "
            "or accept real network credentials.\n\n"
            "Use Password Strength Checker to evaluate your own "
            "test passwords."
        )

    def mic_test(self):
        self.ask("MIC Verification", "Enter a test message:",
                 self.make_mic)

    def make_mic(self, message):
        if not message:
            return
        key = b"L_WIFI_LAB_KEY"
        mic = hmac.new(key, message.encode(), hashlib.sha256).hexdigest()
        self.ask("MIC Verification", "Generated MIC:\n" + mic +
                 "\n\nEnter MIC to verify:", lambda entered:
                 self.show("MIC Result",
                 "MIC VALID!" if hmac.compare_digest(mic, entered.strip())
                 else "MIC INVALID!"))

    def handshake(self):
        self.show("WPA2 Four-Way Handshake",
            "MESSAGE 1\nAccess Point sends ANonce.\n\n"
            "MESSAGE 2\nClient sends SNonce and MIC.\n\n"
            "MESSAGE 3\nAccess Point sends GTK and MIC.\n\n"
            "MESSAGE 4\nClient confirms key installation.\n\n"
            "PURPOSE\n"
            "- Authenticate the client.\n"
            "- Derive session encryption keys.\n"
            "- Confirm key possession.")

    def strength(self):
        self.ask("Password Strength", "Enter a test password:",
                 self.check_strength, True)

    def score_password(self, password):
        checks = {
            "12 or more characters": len(password) >= 12,
            "Uppercase letters": any(c.isupper() for c in password),
            "Lowercase letters": any(c.islower() for c in password),
            "Numbers": any(c.isdigit() for c in password),
            "Symbols": any(not c.isalnum() for c in password)
        }
        return checks, sum(checks.values())

    def check_strength(self, password):
        checks, score = self.score_password(password)
        level = "WEAK" if score <= 2 else "MEDIUM" if score <= 4 else "STRONG"
        self.show("Strength Result",
                  "Strength: " + level + "\nScore: " +
                  str(score) + "/5")

    def generator(self):
        self.ask("Password Generator",
                 "Enter password length (8-64):",
                 self.generate_password)

    def generate_password(self, value):
        try:
            length = int(value)
            if not 8 <= length <= 64:
                raise ValueError
        except ValueError:
            self.show("Error", "Choose a length from 8 to 64.")
            return

        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        password = ''.join(secrets.choice(chars) for _ in range(length))
        self.show("Generated Password", password)

    def dictionary(self):
        path = os.path.join(os.path.dirname(__file__), "passwords.txt")
        try:
            with open(path, "r") as file:
                words = [line.strip() for line in file if line.strip()]
            if not words:
                self.show("Dictionary Analysis", "Dictionary is empty.")
                return

            lengths = [len(word) for word in words]
            result = (
                "Total entries: " + str(len(words)) +
                "\nUnique entries: " + str(len(set(words))) +
                "\nDuplicates: " + str(len(words) - len(set(words))) +
                "\nShortest length: " + str(min(lengths)) +
                "\nLongest length: " + str(max(lengths)) +
                "\nEntries shorter than 8: " +
                str(sum(1 for word in words if len(word) < 8))
            )
            self.show("Dictionary Analysis", result)
        except FileNotFoundError:
            self.show("Dictionary Analysis", "passwords.txt not found.")

    def hash_compare(self):
        self.ask("Hash Comparison", "Enter a test password:",
                 self.make_hash, True)

    def make_hash(self, password):
        generated = hashlib.sha256(password.encode()).hexdigest()
        self.ask("Hash Comparison",
                 "Generated SHA-256:\n" + generated +
                 "\n\nEnter hash to compare:",
                 lambda saved: self.show(
                     "Hash Result",
                     "HASH MATCH!" if hmac.compare_digest(
                         generated, saved.strip().lower()
                     ) else "HASH DOES NOT MATCH!"
                 ))

    def analyzer(self):
        self.ask("Password Security Analyzer",
                 "Enter a test password:",
                 self.analyze_password, True)

    def analyze_password(self, password):
        checks, score = self.score_password(password)
        result = "PASSWORD SECURITY ANALYSIS\n\n"
        for name, passed in checks.items():
            result += name + ": " + ("PASS" if passed else "FAIL") + "\n"
        result += "\nSecurity Score: " + str(score) + "/5"
        result += "\n\n" + (
            "Good password structure!" if score == 5
            else "Consider improving your password."
        )
        self.show("Security Analysis", result)

    def report(self):
        path = os.path.join(os.path.dirname(__file__), "passwords.txt")
        lines = [
            "===== L WIFI SECURITY LAB REPORT =====",
            "Date: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "",
            "PROJECT: L WiFi Security Lab",
            "STATUS: Educational simulation",
            "",
            "FEATURES: PMK, MIC, WPA2 theory, password analysis,",
            "generator, dictionary statistics, hash comparison."
        ]

        try:
            with open(path, "r") as file:
                words = [line.strip() for line in file if line.strip()]
            lines.extend([
                "",
                "DICTIONARY STATISTICS",
                "Total entries: " + str(len(words)),
                "Unique entries: " + str(len(set(words))),
                "Duplicates: " + str(len(words) - len(set(words)))
            ])
        except FileNotFoundError:
            lines.append("\nDictionary file not found.")

        lines.extend([
            "",
            "Educational security report.",
            "No tested passwords are stored in this report."
        ])

        report_path = os.path.join(
            App.get_running_app().user_data_dir, "security_report.txt"
        )
        with open(report_path, "w") as file:
            file.write("\n".join(lines))

        self.show("Security Report",
                  "Report created successfully:\n\n" + report_path)


if __name__ == "__main__":
    SecurityLabApp().run()
