# Questo file contiene gli stili usati per personalizzare i Widget
from lib.utility.ResourceManager import ResourceManager
from res import Colors
from res.Dimensions import FontSize
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
                    border-image: url(""" + ResourceManager.image("access_background.jpg") + """);\n
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

# Sezione DIALOG
DIALOG_WINDOW = """/* Set style for QPushButton */\n
                QInputDialog {\n
                    background-color: #FFF;\n
                    width: 300px;\n
                    heigth: 150px;\n
                }\n"""

DIALOG_PUSH_BUTTON = """/* Set style for QPushButton */\n
                QPushButton {\n
                    background-color: white;\n
                    border: 1px solid black;\n
                    color: black;\n
                    border-radius: 5px;\n
                    padding: 8px;\n
                    margin: 5px;\n
                    width: 80px;\n
                }\n
                QPushButton:hover {\n
                    background-color: #0B5ED7;\n
                    color: white;\n
                    border: 2px solid #9AC3FE;\n
                }\n
                QPushButton:pressed {\n
                    background-color: #FFF;\n
                    color: white;\n
                    color: #0B5ED7;\n
                    border: 2px solid #9AC3FE;\n
                }\n"""

DIALOG = DIALOG_PUSH_BUTTON

# Sezione ERROR
ERROR_LABEL = """/* Set style for QLabel */
                QLabel {\n
                    color: """ + Colors.ERROR_RED + """;\n
                }\n"""

ERROR_LABEL_INPUT = """/* Set style for QLabel */
                QLabel {\n
                    color: """ + Colors.ERROR_RED + """;\n
                    margin-top: 4px;\n
                }\n"""

LABEL_TITLE = """/* Set style for Qlabel */
                QLabel {\n
                    font-size: """ + str(FontSize.SUB_INTERFACE_TITLE) + """pt;\n
                    color: black;\n
                }\n"""

LABEL_SUBTITLE = """/* Set style for Qlabel */
                QLabel {\n
                    font-size: """ + str(FontSize.SUB_INTERFACE_SUBTITLE) + """pt;\n
                }\n"""

PAGE_TITLE_FRAME = """/* Set style for QFrame */
                QFrame {\n
                    background-color: #ffffff;
                }\n"""

PROFILE_PAGE = """ /* Set style for QFrame */
                QFrame {\n
                    background-color: #EBEBEB;
                }\n"""

EDIT_PROFILE_PAGE = """ /* Set style for QFrame */
                    QMainWindow {\n
                        background-color: white;
                    }\n"""

EDIT_PROFILE_LABEL = """/* Set style for QLabel */\n
                        QLabel {\n
                            color: #767E89;\n
                        }\n
                        #bottom_label {\n
                        }\n
                        #bottom_label:hover {\n
                            text-decoration: underline;\n
                        }\n"""

EDIT_PROFILE_LINE_EDIT = """/* Set style for QLineEdit */\n
                            QLineEdit {\n
                                border: none;\n
                                border-bottom: 2px solid #CCCCCC;\n
                                height: 30px;\n
                            }\n
                            QLineEdit:focus {\n
                                border-bottom: 2px solid #28A2A2;\n
                            }\n"""

EDIT_PROFILE_PAGE = EDIT_PROFILE_PAGE + EDIT_PROFILE_LINE_EDIT + EDIT_PROFILE_LABEL

PROFILE_INFO_NAME = """ /* Set style for QLabel */
                QLabel {\n
                    font-size: 36px;"""

LABEL_PROFILE_INFO = """/* Set style for Qlabel */
                QLabel {\n
                    font-size: 16;
                    background-color: #FFFFFF;
                    border-style: solid;
                    border-width: 1px;\n
                }\n"""

TABLE_HEADER = """/* Set style for Qlabel */
                QLabel {\n
                    font-size: 18;
                    background-color: """ + Colors.GREY + """;
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

EDIT_WORKER_BUTTON = """/* Set style for QPushButton */\n
                        QPushButton {\n
                            background-color: #0D6EFD;\n
                            border: 2px solid #FFF;\n
                            color: #FFF;\n
                            border-radius: 5px;\n
                            padding: 10px;\n
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
                    background-color: #FFF;\n
                    border: 1px solid black;\n
                    border-right: none;\n
                }\n
                #central_frame {\n
                    background-color: #FFF;\n
                    border: 1px solid black;\n
                    border-top: none;\n
                    border-bottom: none;\n
                    border-right: none;\n
                }\n
                #sidebar_frame {\n
                    background-color: #FFF;\n
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

STANDARD_TABLE = """/* Set style for QTableWidget e QTableWidgetItem */\n
                QTableWidget {\n
                    selection-background-color: white;\n
                }\n
                QTableWidget::item {\n
                    border-bottom: 2px solid #dddddd;\n
                }\n
                QTableWidget::item:selected {\n 
                    background-color: #00A2A2;\n
                }\n
                QHeaderView {\n
                    background-color: #dddddd;\n
                    font-size: """ + str(FontSize.TABLE_HEADER) + """pt;\n
                    font-weight: bold;\n
                }\n"""

PRICE_CATALOG_TABLE = """/* Set style for QTableWidget e QTableWidgetItem */\n
                QTableWidget {\n
                    selection-background-color: white;\n
                    gridline-color: black;\n
                }\n
                QTableWidget::item:selected {\n 
                    background-color: #72aa53;\n
                }\n"""

