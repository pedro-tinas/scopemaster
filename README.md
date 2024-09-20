# Scope Master - A Rich Text Editor for Case Management

Scope Master is a Python-based rich text editor, built using PyQt5, designed to assist technical support professionals in documenting and managing support cases efficiently. It provides a well-structured interface to log case details, issue descriptions, troubleshooting steps, and action plans. You can also export the case content to HTML format and copy it to the clipboard for easy sharing.

## Features

- **Rich Text Editing**: Format text with bold, italic, and bullet lists.
- **Case Documentation**: Log critical case information such as issue description, troubleshooting steps, environment details, and action plans.
- **Customizable Layout**: Includes fields for capturing specific details like recent changes, frequency of the issue, environment type, and RDP methods.
- **Calendar Integration**: Select the next contact date using a calendar popup.
- **File Transfer Link**: Option to provide file transfer links directly within the case.
- **Clipboard Export**: Export your case details into an HTML format and copy them to your clipboard.
- **Platform-Specific Checkboxes**: Select from a list of common environments (e.g., Windows 10, Server 2019) and RDP methods (e.g., Direct RDP or Remote Desktop Services).
- **Simple, Intuitive UI**: Easy to use interface with grid-based layout for clear data entry.

## Prerequisites

Make sure you have Python installed on your machine, and you’ll need the following Python libraries:

- `PyQt5` 
- `sys`
- `os`

To install PyQt5, you can use:

```bash
pip install PyQt5

## More Info

How to Use
Clone the repository and navigate to the project directory:

bash
Copy code
git clone https://github.com/yourusername/scope-master.git
cd scope-master
Run the application:

bash
Copy code
python main.py
The main window will open with fields for entering case details. Fill in the required information such as the case title, issue description, troubleshooting steps, and more.

After completing the form, you can export the case details in HTML format by selecting "Export to Clipboard" from the toolbar.

Application Screenshot

File Structure
main.py: The main entry point of the application containing the RichTextEditor class.
assets/: Store image assets (icons for toolbar buttons like bold, italic, bullet points).
screenshot.png: A sample screenshot of the app.
Exported HTML Format
The case details are exported as an HTML table with sections like:

Case Title
Issue Description/Symptoms
Recent Changes
Frequency of the Issue
Workaround
Environment and RDP Methods
Troubleshooting Steps
Action Plans for Microsoft and Customer
File Transfer Links
How to Contribute
We welcome contributions! Feel free to fork the project and submit a pull request. You can contribute by:

Adding new features or improving existing ones.
Fixing bugs or reporting issues.
Optimizing the UI/UX.

Author
Pedro M

Feel free to reach out or open an issue for any feedback or questions.
