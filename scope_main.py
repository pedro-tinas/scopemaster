import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTextEdit, QLineEdit, QAction, QFileDialog, QColorDialog, QFontDialog,
                             QVBoxLayout, QWidget, QMenuBar, QMenu, QCheckBox, QHBoxLayout, QDateEdit, QLabel, QGridLayout, QToolBar, QComboBox, QMessageBox, QRadioButton, QButtonGroup)
from PyQt5.QtGui import QTextCursor, QImage, QTextDocument, QTextImageFormat, QFont, QIcon, QPainter, QColor, QClipboard, QTextListFormat
from PyQt5.QtCore import QDate, Qt, QBuffer, QByteArray, QIODevice, QMimeData, QUrl
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QTextEdit
import os

class RichTextEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('Scope Master')
        self.setGeometry(100, 100, 1000, 800)

        # Central widget
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Layout
        self.layout = QGridLayout(self.central_widget)

        # Case Title
        self.case_title = QLineEdit(self)
        self.case_title.setMaxLength(250)

        # Text Edit Widgets
        self.issue_description = CustomTextEdit(self)
        self.issue_description.setPlaceholderText("""
Proper scoping is very important in order to fully understand the issue and to ​provide the customer the best possible support. It also binds you and the customer to focus on resolving one specific issue within a case.

        What is the exact issue?
         Are there any (error) messages displayed for the user?
          Are all users affected or only some of them?
            Has there been any preliminary research/troubleshooting done on customer side?
              How is the issue impacting the users and overall the business? What is the business context of the issue?
""")
        self.recent_changes = QLineEdit(self)
        self.recent_changes.setMaxLength(250)
        self.recent_changes.setPlaceholderText("Describe any recent changes that might have caused the issue.")
        self.workaround = QLineEdit(self)
        self.workaround.setMaxLength(250)
        self.workaround.setPlaceholderText("If there is a workaround, please describe it here.")
        self.troubleshooting = CustomTextEdit(self)

        self.troubleshooting.setPlaceholderText("""
Add here all the relevant troubleshooting done by you or the customer. This will help to avoid duplicate work and to provide a clear overview of the steps taken.
""")
        self.action_microsoft = QLineEdit(self)
        self.action_microsoft.setMaxLength(250)
        self.action_microsoft.setPlaceholderText("Describe the action that Microsoft needs to take.")
        self.action_customer = QLineEdit(self)
        self.action_customer.setMaxLength(250)
        self.action_customer.setPlaceholderText("Describe the action that the customer needs to take.")
        self.workspace = QLineEdit(self)
        self.workspace.setMaxLength(250)
        self.workspace.setPlaceholderText("www.filetransferlink.com")

        
        self.setup_ui_components()
        self.create_menus()
        self.create_toolbar()
        self.show()

    def setup_ui_components(self):
        labels = [
            ("Case Title", self.case_title),
            ("Issue Description/Symptoms", self.issue_description),
            ("Recent Changes", self.recent_changes),
            ("Frequency", None),
            ("Workaround", self.workaround),
            ("Environment", None),
            ("RDP Method", None),
            ("Troubleshooting", self.troubleshooting),
            ("Action on Microsoft", self.action_microsoft),
            ("Action on Customer", self.action_customer),
            ("Next Contact", None),
            ("File Transfer", self.workspace)
        ]

        # Adding Labels and Text Edits
        for i, (label_text, widget) in enumerate(labels):
            label = QLabel(label_text)
            self.layout.addWidget(label, i, 0)
            if widget:
                self.layout.addWidget(widget, i, 1, 1, 4)

        # Frequency checkboxes
        self.frequency_always = QCheckBox("Always", self)
        self.frequency_random = QCheckBox("Random", self)
        self.layout.addWidget(self.frequency_always, 3, 1)
        self.layout.addWidget(self.frequency_random, 3, 2)

        # Environment checkboxes
        self.environment_labels = ["Windows 10", "Windows 11", "Windows Server 2016", "Windows Server 2019", "Windows Server 2022"]
        self.environment_checkboxes = [QCheckBox(env, self) for env in self.environment_labels]
        for i, checkbox in enumerate(self.environment_checkboxes):
            self.layout.addWidget(checkbox, 5, i + 1)

        # RDP Method checkboxes
        self.rds_checkbox = QCheckBox("Remote Desktop Services", self)
        self.direct_rdp_checkbox = QCheckBox("Direct RDP", self)
        self.layout.addWidget(self.rds_checkbox, 6, 1)
        self.layout.addWidget(self.direct_rdp_checkbox, 6, 2)

        # Next Contact Date
        self.next_contact_calendar = QDateEdit(calendarPopup=True)
        self.next_contact_calendar.setDate(QDate.currentDate())
        self.layout.addWidget(self.next_contact_calendar, 10, 1)


        # Save Button
        self.save_action = QAction('Export to Clipboard', self)
        self.save_action.triggered.connect(self.save_data)
        self.layout.addWidget(QLabel(), 11, 0, 1, 5)  # Empty row for spacing

    
        # About Button
        self.about_action = QAction('About', self)
        self.layout.addWidget(QLabel(), 12, 0, 1, 5)

       
    def create_menus(self):
        # Menu bar
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('File')
        open_action = QAction('Open', self)
        open_action.triggered.connect(self.open_file)
        save_action = QAction('Export to Clipboard', self)
        save_action.triggered.connect(self.save_data)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)

        # Edit menu
        edit_menu = menubar.addMenu('Edit')
        copy_action = QAction('Copy', self)
        copy_action.triggered.connect(self.copy)
        paste_action = QAction('Paste', self)
        paste_action.triggered.connect(self.paste)
        cut_action = QAction('Cut', self)
        cut_action.triggered.connect(self.cut)
        edit_menu.addAction(copy_action)
        edit_menu.addAction(paste_action)
        edit_menu.addAction(cut_action)

        # About menu
        about_menu = menubar.addMenu('About')
        about_action = QAction('About', self)
        about_menu.addAction(about_action)

    def toggle_transfer_section(self, radio_button):
        self.transfer_section.setVisible(radio_button.isChecked())

    def toggle_language_section(self, radio_button):
        self.language_required_label.setVisible(radio_button.isChecked())
        self.language_required_textbox.setVisible(radio_button.isChecked())

    def toggle_meeting_section(self, radio_button):
        self.meeting_link_label.setVisible(radio_button.isChecked())
        self.meeting_link_textbox.setVisible(radio_button.isChecked())

    def create_toolbar(self):
        toolbar = QToolBar("Format Toolbar")
        self.addToolBar(toolbar)


        # Bold action
        bold_action = QAction(QIcon('bold.png'), 'Bold', self)
        bold_action.setCheckable(True)
        bold_action.triggered.connect(self.toggle_bold)
        toolbar.addAction(bold_action)

        # Italic action
        italic_action = QAction(QIcon('italic.png'), 'Italic', self)
        italic_action.setCheckable(True)
        italic_action.triggered.connect(self.toggle_italic)
        toolbar.addAction(italic_action)


        # Add bullet list action
        bullet_action = QAction(QIcon('bullet.png'), 'Bullets', self)
        bullet_action.setCheckable(True)
        bullet_action.triggered.connect(self.toggle_bullets)
        toolbar.addAction(bullet_action)

    def toggle_bullets(self):
        cursor = self.current_editor().textCursor()
        cursor.insertList(QTextListFormat.ListDisc)

    def copy(self):
        self.current_editor().copy()

    def paste(self):
        self.current_editor().paste()

    def cut(self):
        self.current_editor().cut()

    def toggle_bold(self):
        fmt = self.current_editor().currentCharFormat()
        fmt.setFontWeight(QFont.Bold if not fmt.fontWeight() == QFont.Bold else QFont.Normal)
        self.current_editor().setCurrentCharFormat(fmt)

    def toggle_italic(self):
        fmt = self.current_editor().currentCharFormat()
        fmt.setFontItalic(not fmt.fontItalic())
        self.current_editor().setCurrentCharFormat(fmt)




    

   

    def save_data(self):
        frequency = "Always" if self.frequency_always.isChecked() else "Random" if self.frequency_random.isChecked() else ""
        environments = [checkbox.text() for checkbox in self.environment_checkboxes if checkbox.isChecked()]
        rdp_method = "RDS" if self.rds_checkbox.isChecked() else "Direct RDP" if self.direct_rdp_checkbox.isChecked() else ""
        next_contact_date = self.next_contact_calendar.date().toString("yyyy-MM-dd")

        issue_description_html = self.issue_description.toHtml()
        troubleshooting_html = self.troubleshooting.toHtml()


        # Clean up the HTML content to ensure it fits within the table
        def clean_html(html):
            body_start = html.find('<body>') + len('<body>')
            body_end = html.find('</body>')
            return html[body_start:body_end].strip()

        issue_description_content = clean_html(issue_description_html)
        troubleshooting_content = clean_html(troubleshooting_html)
        
        

        # Create HTML content
        html_content = """
        <html>
            <head>
                <style>
                    table {{
                        border-collapse: collapse;
                        width: 60%;
                    }}
                    th, td {{
                        border: 1px solid black;
                        padding: 4px;
                        text-align: left;
                    }}
                    th {{
                        background-color: #1F4E79;
                        color: white;
                        font-weight: bold;
                        font-size: 12pt;
                    }}
                    .section-header {{
                        background-color: #92dde8;
                        font-weight: bold;
                        font-size: 13pt;
                    }}         
                    .section-header1 {{
                        background-color: #b8daf2;
                        font-weight: bold;
                        font-size: 12pt;
                    }}

                    .section-header2 {{
                        background-color: #f7e5c8;
                        font-weight: bold;
                        font-size: 12pt;
                    }}

                    .section-header3 {{
                        background-color: #cef2a7;
                        font-weight: bold;
                        font-size: 12pt;
                    }}
                    .section-header4 {{
                        background-color: #f5dfe0;
                        font-weight: bold;
                        font-size: 12pt;
                    }}
                    .sub-section {{
                        background-color: #92dde8;
                        font-weight: bold;
                        font-size: 12pt;
                    }}
                </style>
            </head>
            <body>
                <table>
                    <tr><td class="section-header1">Case Title</td></tr>
                    <tr><td>{case_title}</td></tr>
                    <tr><td class="section-header2">Scope</td></tr>
                    <tr><td>
                        <p><strong>Issue description/symptoms:</strong>{issue_description}</p>
                        <p><strong>Recent changes:</strong> {recent_changes}</p>
                        <p><strong>Frequency:</strong> {frequency}</p>
                        <p><strong>Workaround:</strong> {workaround}</p>
                        <p><strong>Environment:</strong> {environment}</p>
                        <p><strong>RDP Method:</strong> {rdp_method}</p>
                    </td></tr>
                    <tr><td class="section-header3">Troubleshoot</td></tr>
                    <tr><td>{troubleshooting}</td></tr>
                    <tr><td class="section-header">Action Plan</td></tr>
                    <tr><td>
                        <p><strong>Action on Microsoft:</strong> {action_microsoft}</p>
                        <p><strong>Action on Customer:</strong> {action_customer}</p>
                        <p><strong>Next Contact:</strong> {next_contact}</p>
                    </td></tr>
                    <tr><td class="section-header4">File Transfer</td></tr>
                    <tr><td>https:\\filetransferlink.com</td></tr>
                </table>
            </body>
            </html>
            
        """.format(
            case_title=self.case_title.text(),
            issue_description=issue_description_html,
            recent_changes=self.recent_changes.text(),
            frequency=frequency,
            workaround=self.workaround.text(),
            environment=', '.join(environments),
            rdp_method=rdp_method,
            troubleshooting=troubleshooting_html,
            action_microsoft=self.action_microsoft.text(),
            action_customer=self.action_customer.text(),
            next_contact=next_contact_date
        )


        # Debugging output
        print("Final HTML Content:")
        print(html_content)


        # Copy to clipboard
        clipboard = QApplication.clipboard()
        mime_data = QMimeData()
        mime_data.setHtml(html_content)
        clipboard.setMimeData(mime_data)

        print("Content copied to clipboard.")

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*);;Text Files (*.txt)")
        if file_path:
            with open(file_path, 'r') as file:
                self.current_editor().setHtml(file.read())

    def current_editor(self):
        # Returns the currently focused QTextEdit widget
        if self.issue_description.hasFocus():
           return self.issue_description
        elif self.troubleshooting.hasFocus():
           return self.troubleshooting
        return self.issue_description  # Default return

    def show_about_popup(self):
        # Create a message box for the About pop-up
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("About")
        msg_box.setText("Created by Pedro M")
        msg_box.setStandardButtons(QMessageBox.Ok)


class CustomTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptRichText(True)
        self.setAcceptDrops(True)

    def insertFromMimeData(self, source):
        if source.hasImage():
            image = source.imageData()
            self.insert_image(image)
        else:
            super().insertFromMimeData(source)

    def insert_image(self, image):
        if not image.isNull():
            cursor = self.textCursor()
            document = self.document()
            image_format = QTextImageFormat()

            buffer = QBuffer()
            buffer.open(QIODevice.WriteOnly)
            image.save(buffer, "PNG")
            base64_data = buffer.data().toBase64().data().decode()
            buffer.close()

            image_format.setName(f"data:image/png;base64,{base64_data}")
            image_format.setWidth(image.width())
            image_format.setHeight(image.height())
            cursor.insertImage(image_format)

def main():
    app = QApplication(sys.argv)
    editor = RichTextEditor()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
