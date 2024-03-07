# Questo file contiene gli stili usati per personalizzare i Widget
from res.Strings import Config

# Sezione ACCESS
ACCESS_LABEL = """/* Set style for QLabel */\n
                QLabel {\n
                    color: #767E89\n
                }\n
                #bottom_label {\n
                }\n
                #bottom_label:hover {\n
                    text-decoration: underline;\n
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
                #main_widget {\n
                    background: #FFF;\n
                    border-radius: 20px\n
                }\n"""

ACCESS_PUSH_BUTTON = """/* Set style for QPushButton */\n
                QPushButton {\n
                    background-color: #0D6EFD;\n
                    border: 2px solid #FFF;\n
                    color: #FFF;\n
                    border-radius: 5px;\n
                    padding: 10px;\n
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

ERROR_COLOR = "color: #FF0000;"

ERROR_LABEL = """/* Set style for QLabel */
                QLabel {\n
                    """ + ERROR_COLOR + """\n
                }\n"""

ERROR_LABEL_INPUT = """/* Set style for QLabel */
                QLabel {\n
                    """ + ERROR_COLOR + """\n
                    margin-top: 4px;\n
                }\n"""

LABEL_TITLE = """/* Set style for Qlabel */
                QLabel {\n
                    font-size: 26px;\n
                }\n"""

LABEL_SUBTITLE = """/* Set style for Qlabel */
                QLabel {\n
                    font-size: 12px;\n
                }\n"""

PAGE_TITLE_FRAME = """/* Set style for QFrame */
                QFrame {\n
                    background-color: #ffffff;
                }\n"""

PROFILE_PAGE = """ /* Set style for QFrame */
                QFrame {\n
                    background-color: #ebebeb;
                }\n"""

PROFILE_INFO_NAME = """ /* Set style for QLabel */
                QLabel {\n
                    font-size: 36px;               
                }\n"""

LABEL_PROFILE_INFO = """/* Set style for Qlabel */
                QLabel {\n
                    font-size: 16;
                    background-color: #ffffff;
                    border-style: solid;
                    border-width: 1px;\n
                }\n"""

TABLE_HEADER = """/* Set style for Qlabel */
                QLabel {\n
                    font-size: 18;
                    background-color: #c0c0c0;
                    border-style: solid;
                    border-width: 1px;\n
                }\n"""

EDIT_BUTTON = """/* Set style for QPushButton */\n
                QPushButton {\n
                    background-color: #0D6EFD;\n
                    border: 2px solid #FFF;\n
                    color: #FFF;\n
                    border-radius: 5px;\n
                    padding: 10px;\n
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


DELETE_BUTTON = """/* Set style for QPushButton */\n
                QPushButton {\n
                    background-color: #ff471a;\n
                    border: 2px solid #FFF;\n
                    color: #FFF;\n
                    border-radius: 5px;\n
                    padding: 10px;\n
                    margin-top: 10px\n
                }\n
                QPushButton:hover {\n
                    background-color: #ff3300;\n
                    border: 2px solid #ff8566;\n
                }\n
                QPushButton:pressed {\n
                    background-color: #FFF;\n
                    color: #0B5ED7;\n
                    border: 2px solid #ff8566;\n
                }\n"""


BASE_WIDGET = """/* Set style for sub interface */\n
                #header_frame {\n
                    background-color: #fff;\n
                    border: 1px solid black;\n
                    border-right: none;\n
                }\n
                #central_frame {\n
                    background-color: #fff;\n
                    border: 1px solid black;\n
                    border-top: none;\n
                    border-bottom: none;\n
                    border-right: none;\n
                }\n
                #sidebar_frame {\n
                    background-color: #fff;\n
                    border: 1px solid black;\n
                    border-top: none;\n
                    border-bottom: none;\n
                    border-right: none;\n
                }\n"""

BASE_WIDGET_2 = """/* Set style for sub interface */\n
                #header_frame {\n
                    border: 1px solid;\n
                    border-right: none;\n
                }\n
                #central_frame {\n
                    border: 1px solid;\n
                    border-top: none;\n
                    border-bottom: none;\n
                    border-right: none;\n
                }\n
                #sidebar_frame {\n
                    border: 1px solid;\n
                    border-top: none;\n
                    border-bottom: none;\n
                    border-right: none;\n
                }\n"""

TABLE = """/* Set style for QTableWidget e QTableWidgetItem */\n
                QTableWidget {\n
                
                }\n
                QTableWidget::item {\n
                    border-bottom: 2px solid #dddddd;\n
                }\n
                QHeaderView {\n
                    background-color: #dddddd;\n
                    font-size: 11pt;\n
                    font-weight: bold;\n
                }\n"""