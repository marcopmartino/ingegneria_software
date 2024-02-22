# Questo file contiene gli stili usati per personalizzare i Widget
from res.Strings import Config

# Sezione ACCESS
ACCESS_LABEL = """/* Set style for QLabel */\n
                QLabel {\n
                    color: #767E89\n
                }\n
                QLabel#title_label {\n
                    color: #000\n
                }\n"""

ACCESS_LINE_EDIT = """/* Set style for QLineEdit */\n
                QLineEdit {\n
                    border: none;\n
                    border-bottom: 2px solid #CCCCCC;\n
                    height: 30px;\n
                }\n
                QLineEdit:focus {\n
                    border-bottom: 2px solid #28A2A2\n
                }\n"""

ACCESS_MAIN_WINDOW = """/* Set style for MainWindow */\n
                QMainWindow {\n
                    border-image: """ + Config.image("access_background.jpg") + """;\n
                }\n
                /* Set style for QWidget */\n
                #widget {\n
                    background: #FFF;\n
                    border-radius: 20px\n
                }\n"""

ACCESS_PUSH_BUTTON = """/* Set style for QPushButton */\n
                QPushButton {\n
                    background-color: #0D6EFD;\n
                    border: 2px solid #FFF;\n
                    color: #FFF;\n
                    border-radius: 5px;\n
                    padding: 6px;\n
                    margin-top: 10px\n
                }\n
                QPushButton:hover {\n
                    background-color: #0B5ED7;\n
                    border: 2px solid #9AC3FE;\n
                }\n
                QPushButton:pressed {\n
                    background-color: #FFF;\n
                    color: #0B5ED7;\n
                    border: 2px solid #9AC3FE;\n
                }\n"""

ACCESS = ACCESS_LABEL + ACCESS_LINE_EDIT + ACCESS_MAIN_WINDOW + ACCESS_PUSH_BUTTON
