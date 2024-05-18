import sys
from unittest import TestCase

from PyQt5.QtWidgets import QLineEdit, QCheckBox, QSpinBox, QComboBox, QApplication
from qfluentwidgets import DatePicker

from lib.utility.UtilityClasses import DatetimeUtils
from lib.validation.FormField import CheckBoxFormField, SpinBoxFormField, ComboBoxFormField, \
    DatePickerFormField, LineEditValidatableFormField
from lib.validation.FormManager import FormManager
from lib.validation.ValidationRule import ValidationRule

app = QApplication(sys.argv)


class FormManagerTestCase(TestCase):

    def setUp(self) -> None:
        # Inizializza i campi di input
        self.line_edit = QLineEdit("Testo del QLineEdit")
        self.line_edit.setObjectName("line edit widget")

        self.check_box = QCheckBox()
        self.check_box.setChecked(True)
        self.check_box.setObjectName("check box widget")

        self.spin_box = QSpinBox()
        self.spin_box.setValue(15)
        self.spin_box.setRange(10, 50)
        self.spin_box.setObjectName("spin box widget")

        self.combo_box = QComboBox()
        self.combo_box.addItem("Primo item", True)
        self.combo_box.addItem("Secondo item", -27.5)
        self.combo_box.addItem("Terzo item", None)
        self.combo_box.setCurrentIndex(1)
        self.combo_box.setObjectName("combo box widget")

        self.date_picker = DatePicker()
        self.date_picker.setDate(DatetimeUtils.format("17/05/2024"))
        self.date_picker.setObjectName("date picker widget")

        # Inizializza il FormManager
        self.form_manager = FormManager([
            LineEditValidatableFormField(self.line_edit),
            CheckBoxFormField(self.check_box),
            SpinBoxFormField(self.spin_box),
            ComboBoxFormField(self.combo_box),
            DatePickerFormField(self.date_picker)
        ], "Token di prova")

    def test_data_extraction(self) -> None:
        # Estrae i dati dai campi della form
        extracted_data = self.form_manager.data()

        # Controlla che i dati estratti siano corretti
        self.assertEqual(extracted_data.get("form_token"), "Token di prova")
        self.assertEqual(extracted_data.get("field_count"), 5)
        self.assertEqual(extracted_data.get("line edit widget"), "Testo del QLineEdit")
        self.assertEqual(extracted_data.get("check box widget"), True)
        self.assertEqual(extracted_data.get("spin box widget"), 15)
        self.assertEqual(extracted_data.get("combo box widget"), -27.5)
        self.assertEqual(extracted_data.get("date picker widget"), "17/05/2024")

    def test_validation(self) -> None:
        self.assertEqual(self.form_manager.validate(), True)

        self.line_edit.setValidator(ValidationRule.IVANumber().validator)
        self.assertEqual(self.form_manager.validate(), False)

        self.line_edit.setText("10391823745")
        self.assertEqual(self.form_manager.validate(), True)

        self.line_edit.setText("103918237458")
        self.assertEqual(self.form_manager.validate(), False)

    def test_clear(self) -> None:
        # Svouta i campi
        self.form_manager.clear_fields()

        # Estrae i dati dai campi della form
        extracted_data = self.form_manager.data()

        # Controlla che i dati estratti siano corretti
        self.assertEqual(extracted_data.get("form_token"), "Token di prova")
        self.assertEqual(extracted_data.get("field_count"), 5)
        self.assertEqual(extracted_data.get("line edit widget"), "")
        self.assertEqual(extracted_data.get("check box widget"), False)
        self.assertEqual(extracted_data.get("spin box widget"), 10)
        self.assertEqual(extracted_data.get("combo box widget"), True)
        self.assertEqual(extracted_data.get("date picker widget"), DatetimeUtils.current_date())
