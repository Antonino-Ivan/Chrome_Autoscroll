import tkinter as tk
import subprocess
import pyautogui
import threading
import time
import os

class ChromeAutoScroll:
    def __init__(self, root):
        self.root = root
        self.root.title("Chrome Auto-Scroll")
        self.root.geometry("360x280")
        self.scrolling = False
        self.scroll_thread = None

        # UI: URL Input
        tk.Label(root, text="Target URL:").pack(pady=(10, 0))
        self.url_entry = tk.Entry(root, width=45)
        self.url_entry.insert(0, "enter the url where you want to scroll")
        self.url_entry.pack(pady=5)

        # UI: Scroll Speed (much smaller increments for smoothness)
        tk.Label(root, text="Scroll Amount (1-50 pixels):").pack()
        self.speed_scale = tk.Scale(root, from_=1, to=50, orient=tk.HORIZONTAL)
        self.speed_scale.set(3)  # Much slower default
        self.speed_scale.pack(pady=5)

        # UI: Scroll Interval (controls smoothness)
        tk.Label(root, text="Scroll Interval (0.01-0.5 seconds):").pack()
        self.interval_scale = tk.Scale(root, from_=1, to=50, orient=tk.HORIZONTAL)
        self.interval_scale.set(10)  # 0.10 seconds default
        self.interval_scale.configure(label="Speed")
        self.interval_scale.pack(pady=5)

        # UI: Buttons
        self.btn_frame = tk.Frame(root)
        self.btn_frame.pack(pady=10)

        self.start_btn = tk.Button(self.btn_frame, text="Open & Start Scrolling", command=self.start_scrolling)
        self.start_btn.pack(side=tk.LEFT, padx=5)

        self.stop_btn = tk.Button(self.btn_frame, text="Stop Scrolling", command=self.stop_scrolling, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)

        # UI: Status
        self.status_label = tk.Label(root, text="Status: Idle", fg="gray")
        self.status_label.pack()
        
        # Info label
        tk.Label(root, text="Lower values = smoother scroll", fg="gray", font=("Arial", 8)).pack(pady=(5, 0))

    def start_scrolling(self):
        if self.scrolling:
            return

        url = self.url_entry.get().strip()
        if not url:
            self.status_label.config(text="Error: Please enter a URL", fg="red")
            return

        self.status_label.config(text="Opening Chrome ...", fg="blue")
        self.start_btn.config(state=tk.DISABLED)
        self.root.update()

        # Launch Chrome in Incognito mode
        cmd = ["open", "-a", "Google Chrome", "--args", url]
        try:
            subprocess.Popen(cmd)
        except Exception as e:
            self.status_label.config(text=f"Error launching Chrome: {e}", fg="red")
            self.start_btn.config(state=tk.NORMAL)
            return

        # Wait for Chrome to open, then bring it to front
        time.sleep(2)
        os.system('osascript -e \'tell application "Google Chrome" to activate\'')
        time.sleep(0.5)

        # Start scrolling in background thread
        self.scrolling = True
        self.scroll_thread = threading.Thread(target=self._scroll_loop, daemon=True)
        self.scroll_thread.start()

        self.stop_btn.config(state=tk.NORMAL)
        self.status_label.config(text="Status: Auto-scrolling (smooth)...", fg="green")

    def _scroll_loop(self):
        scroll_amount = -self.speed_scale.get()  # Negative = scroll down
        interval = self.interval_scale.get() / 100.0  # Convert to seconds (0.01 to 0.50)
        
        while self.scrolling:
            try:
                pyautogui.scroll(scroll_amount)
                time.sleep(interval)
            except Exception:
                break

    def stop_scrolling(self):
        self.scrolling = False
        if self.scroll_thread:
            self.scroll_thread.join(timeout=1.0)
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.status_label.config(text="Status: Stopped", fg="gray")

if __name__ == "__main__":
    pyautogui.FAILSAFE = True  # Move mouse to top-left corner to abort (safety feature)
    
    root = tk.Tk()
    app = ChromeAutoScroll(root)
    root.mainloop()