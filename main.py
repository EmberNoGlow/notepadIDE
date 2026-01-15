import os
import subprocess
import win32gui
import win32con
import time
import sys

def launch_application(app_path, app_name):
    """Launch an application and return its process."""
    try:
        process = subprocess.Popen([app_path])
        return process
    except Exception as e:
        print(f"Failed to launch {app_name}: {e}")
        sys.exit(1)

def find_window_by_class_and_title(class_name, title=None):
    """Find a window by its class name and optional title."""
    def callback(hwnd, hwnds):
        if win32gui.GetClassName(hwnd) == class_name:
            if title is None or win32gui.GetWindowText(hwnd) == title:
                hwnds.append(hwnd)
        return True

    hwnds = []
    win32gui.EnumWindows(callback, hwnds)
    return hwnds[0] if hwnds else None

def modify_window(hwnd, new_title, x, y, width=600, height=400):
    """Modify the window properties and position."""
    try:
        # Change the window title
        win32gui.SetWindowText(hwnd, new_title)

        # Remove minimize, maximize, and close buttons
        style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
        style = style & ~win32con.WS_MINIMIZEBOX & ~win32con.WS_MAXIMIZEBOX & ~win32con.WS_SYSMENU
        style = style & ~win32con.WS_THICKFRAME  # Remove resizable border
        style = style & ~win32con.WS_CAPTION     # Remove title bar
        win32gui.SetWindowLong(hwnd, win32con.GWL_STYLE, style)

        # Set window position and size
        win32gui.SetWindowPos(hwnd, None, x, y, width, height,
                              win32con.SWP_NOZORDER)

        # Force the window to update
        win32gui.SetWindowPos(hwnd, None, 0, 0, 0, 0,
                              win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_FRAMECHANGED)
    except Exception as e:
        print(f"Failed to modify window: {e}")

def main():
    """Launch and modify both Notepad and Explorer windows."""
    # Launch Notepad
    notepad_process = launch_application("C:\\Windows\\System32\\notepad.exe", "Notepad")
    notepad_hwnd = None
    while notepad_hwnd is None:
        notepad_hwnd = find_window_by_class_and_title("Notepad", None)
        if notepad_hwnd is None:
            time.sleep(0.1)
    modify_window(notepad_hwnd, "NotepadWindow", 100, 100, 600, 400)

    # Launch Explorer
    explorer_process = launch_application("C:\\Windows\\explorer.exe", "Explorer")
    explorer_hwnd = None
    while explorer_hwnd is None:
        explorer_hwnd = find_window_by_class_and_title("CabinetWClass", None)
        if explorer_hwnd is None:
            time.sleep(0.1)
    modify_window(explorer_hwnd, "ExplorerWindow", 800, 100, 600, 400)

    print("Both windows are now visible. Press Ctrl+C to close them.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Closing applications...")
        notepad_process.terminate()
        explorer_process.terminate()

if __name__ == "__main__":
    main()
