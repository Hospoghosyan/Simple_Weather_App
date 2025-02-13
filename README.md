# Simple Weather App

This is a simple Python weather application that runs automatically after installation. The setup process is easy and works on **Windows**, **macOS**, and **Linux**.

---

## **How to Download and Run the Project**
Follow the instructions below depending on your operating system.

### **Windows Users**
1. **Clone the repository**  
   - Open the folder where you want to download the project.  
   - Right-click inside the folder and select **"Git Bash Here"**.  
   - Run the following command:  
     ```bash
     git clone https://github.com/Hospoghosyan/Simple_Weather_App.git
     ```
   - Wait for the download to finish.

2. **Run the application**  
   - Open the downloaded project folder (`Simple_Weather_App`).  
   - Double-click the file **`Weather Application Windows.bat`**.  
   - A terminal window will open, install the necessary dependencies, and launch the application.  

---

### **macOS & Linux Users**
1. **Clone the repository**  
   - Open a terminal and navigate to the folder where you want to download the project.  
   - Run the following command:  
     ```bash
     git clone https://github.com/Hospoghosyan/Simple_Weather_App.git
     ```
   - Wait for the download to complete.

2. **Run the application**  
   - Navigate into the project folder:  
     ```bash
     cd Simple_Weather_App
     ```
   - Give execution permission to the scripts:
     ```bash
     sed -i '' $'s/\r$//' Weather_Application_Linux-macOS.sh
     ```
     ```bash
     chmod +x "Weather_Application_Linux-macOS.sh"
     ```
   - Run the script:  
     ```bash
     ./Weather_Application_Linux-macOS.sh
     ```
   - The application will start automatically.

---

## **What Happens When You Run the Project?**
1. A **virtual environment** is created inside the project folder (`venv`).
2. The required **dependencies** are installed from `requirements.txt`.
3. The **terminal is cleared** for better readability.
4. The **application (`app.py`) starts running automatically**.

---

## **Troubleshooting**
If you face any issues, try the following:  
- **On Windows:**
  - Ensure Python is installed and added to the system PATH.
  - If `Weather Application Windows.bat` closes immediately, try running it in Command Prompt (`cmd`):
    ```bash
    cd path\to\Simple_Weather_App
    "Weather Application Windows.bat"
    ```
  
- **On macOS/Linux:**
  - If you get a "Permission Denied" error, run:
    ```bash
    chmod +x "Weather_Application_Linux-macOS.sh"
    ```
  - If Python modules are missing, manually install them:
    ```bash
    pip install -r requirements.txt
    ```

---

## **Contact & Support**
If you need help, feel free to open an issue on this repository or contact me.

---
