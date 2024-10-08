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

print(ResourceManager.image_path("access_background.jpg"))

ACCESS_MAIN_WINDOW = """/* Set style for MainWindow */\n
                QMainWindow {\n
                    border-image: url(""" + ResourceManager.image_path("access_background.jpg") + """);\n
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
                QPushButton {
                    background-color: """ + Colors.WHITE + """;
                    border: 1px solid """ + Colors.GREY + """;
                    color: """ + Colors.BLACK + """;
                    border-radius: 5px;
                    padding: 5px;
                    margin-top: 4px;
                    width: 100px;
                    height: 30px;
                }
                QPushButton:hover {
                    background-color: """ + Colors.EXTRA_LIGHT_GREY + """;
                    border: 1px solid """ + Colors.GREY + """;
                }
                QPushButton:pressed {
                    background-color: """ + Colors.LIGHT_GREY + """;
                    border: 1px solid """ + Colors.GREY + """;
                    color: """ + Colors.GREY + """;
                }"""

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

# Sezione Titolo e Sottotiolo di SubInterfaceWidget
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
                                border-bottom: 2px solid #28A2A2\n
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
                    color: #ff3300;\n
                    border: 2px solid #ff8566;\n
                }\n"""

# BaseWidget
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

BASE_WIDGET_TAB = """/* Set style for sub interface */\n
                #central_frame {\n
                    border: none;\n
                }\n
                #sidebar_frame {\n
                    background-color: #FFF;\n
                    border: 1px solid black;\n
                    border-top: none;\n
                    border-bottom: none;\n
                    border-right: none;\n
                }\n"""

# Standard Table
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

STANDARD_TABLE_NO_ITEM = """/* Set style for QTableWidget e QTableWidgetItem */\n
                QTableWidget {\n
                    selection-background-color: white;\n
                }\n
                QTableWidget::item:selected {\n 
                    background-color: #00A2A2;\n
                }\n
                QHeaderView {\n
                    background-color: #dddddd;\n
                    font-size: """ + str(FontSize.TABLE_HEADER) + """pt;\n
                    font-weight: bold;\n
                }\n"""

PROFILE_TABLE = """/* Set style for QTableWidget e QTableWidgetItem */\n
                QTableWidget {\n
                    selection-background-color: white;\n
                }\n
                QTableWidget::item {\n
                    ;\n
                }\n
                QTableWidget::item:selected {\n 
                    ;\n
                }\n
                QHeaderView {\n
                    background-color: #dddddd;\n
                    font-size: """ + str(FontSize.TABLE_HEADER) + """pt;\n
                    font-weight: bold;\n
                }\n"""

# PriceCatalogTable
PRICE_CATALOG_TABLE = """/* Set style for QTableWidget e QTableWidgetItem */\n
                QTableWidget {\n
                    selection-background-color: white;\n
                    gridline-color: black;\n
                }\n
                QTableWidget::item:selected {\n 
                    background-color: #72aa53;\n
                }\n"""

# ProgressBar
PROGRESS_BAR = """/* Set style for QProgressBar */
                QProgressBar {
                    border: 1px solid black;
                    background-color: white;
                }

                QProgressBar::chunk {
                    background-color: """ + Colors.LIGHT_GREEN + """;
                }"""

# Custom Button Styles
DISABLED_BUTTON = """/* Set style for PushButton */
                PushButton:disabled {
                    background-color: """ + Colors.GREY + """;
                    color: """ + Colors.EXTRA_LIGHT_GREY + """;
                    border: 1px solid """ + Colors.GREY + """;
                }"""

WHITE_BUTTON = """/* Set style for PushButton */
                PushButton {
                    background-color: """ + Colors.WHITE + """;
                    border: 1px solid """ + Colors.GREY + """;
                    color: """ + Colors.BLACK + """;
                    border-radius: 5px;
                    padding: 6px;
                }
                PushButton:hover {
                    background-color: """ + Colors.EXTRA_LIGHT_GREY + """;
                    border: 1px solid """ + Colors.GREY + """;
                }
                PushButton:pressed {
                    background-color: """ + Colors.LIGHT_GREY + """;
                    border: 1px solid """ + Colors.GREY + """;
                    color: """ + Colors.GREY + """;
                }""" + DISABLED_BUTTON

CYAN_BUTTON = """/* Set style for PushButton */
                PushButton {
                    background-color: """ + Colors.CYAN + """;
                    border: 1px solid """ + Colors.CYAN + """;
                    color: """ + Colors.WHITE + """;
                    border-radius: 5px;
                    padding: 6px;
                }
                PushButton:hover {
                    background-color: """ + Colors.LIGHT_CYAN + """;
                    border: 1px solid """ + Colors.LIGHT_CYAN + """;
                }
                PushButton:pressed {
                    background-color: """ + Colors.GRAYISH_CYAN + """;
                    border: 1px solid """ + Colors.GRAYISH_CYAN + """;
                    color: """ + Colors.VERY_LIGHT_GRAYISH_CYAN + """;
                }""" + DISABLED_BUTTON

ORANGE_BUTTON = """/* Set style for PushButton */
                PushButton {
                    background-color: """ + Colors.ORANGE + """;
                    border: 1px solid """ + Colors.ORANGE + """;
                    color: """ + Colors.WHITE + """;
                    border-radius: 5px;
                    padding: 6px;
                }
                PushButton:hover {
                    background-color: """ + Colors.LIGHT_ORANGE + """;
                    border: 1px solid """ + Colors.LIGHT_ORANGE + """;
                }
                PushButton:pressed {
                    background-color: """ + Colors.GRAYISH_ORANGE + """;
                    border: 1px solid """ + Colors.GRAYISH_ORANGE + """;
                    color: """ + Colors.VERY_LIGHT_GRAYISH_ORANGE + """;
                }""" + DISABLED_BUTTON

RED_BUTTON = """/* Set style for PushButton */
                PushButton {
                    background-color: """ + Colors.DARK_RED + """;
                    border: 1px solid """ + Colors.DARK_RED + """;
                    color: """ + Colors.WHITE + """;
                    border-radius: 5px;
                    padding: 7px;
                }
                PushButton:hover {
                    background-color: """ + Colors.RED + """;
                    border: 1px solid """ + Colors.RED + """;
                }
                PushButton:pressed {
                    background-color: """ + Colors.GRAYISH_DARK_RED + """;
                    border: 1px solid """ + Colors.GRAYISH_DARK_RED + """;
                    color: """ + Colors.VERY_LIGHT_GRAYISH_DARK_RED + """;
                }""" + DISABLED_BUTTON

