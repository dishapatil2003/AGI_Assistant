🚀 AGI Dashcam Assistant
🎯 Overview

AGI Dashcam Assistant is an AI-powered desktop automation tool that captures your screen activity, understands tasks, and executes them automatically using intelligent workflows.

🧩 Features

🎥 Capture Clip: Records user activity.

🧠 Understand Clip: Analyzes and generates workflow steps.

🤖 Execute Automation: Performs detected actions automatically.

📄 Show Summary: Displays task summary for review.

🖥️ Built with Tkinter, PyAutoGUI, and subprocess.

⚙️ Folder Structure
AGI_Dashcam/
├── scripts/
│   ├── capture_dashcam.py
│   ├── understand_clip.py
├── data/
│   ├── understood_actions.json
│   ├── summary.txt
├── models/
├── gui_dashboard.py
└── requirements.txt

💻 Installation
git clone https://github.com/dishapatil2003/AGI_Assistant.git
cd AGI_Assistant
pip install -r requirements.txt
python scripts/gui_dashboard.py

🧱 Build Executable
pyinstaller --onefile --noconsole --name gui_dashboard_final scripts/gui_dashboard.py


The executable will appear in the dist/ folder.

👩‍💻 Author

Disha Patil
