import tkinter as tk
from datetime import datetime
from PIL import ImageGrab, ImageTk
import pytesseract

class SnippingTool:
    def __init__(self, master, text_area=None):
        self.master = master
        self.master.title("Snipping Tool")

        self.frame_buttons = tk.Frame(master)
        self.frame_buttons.pack(side=tk.TOP, fill=tk.X)

        self.button_container = tk.Frame(self.frame_buttons)
        self.button_container.pack(side=tk.TOP, pady=10)

        self.new_button = tk.Button(self.button_container, text="New", command=self.start_snipping)
        self.new_button.pack(side=tk.LEFT, padx=5, fill=tk.BOTH, expand=True)

        self.to_text_button = tk.Button(self.button_container, text="ToText", command=self.convert_to_text, state=tk.DISABLED)
        self.to_text_button.pack(side=tk.LEFT, padx=5, fill=tk.BOTH, expand=True)

        self.screenshot_label = tk.Label(master)
        self.screenshot_label.pack()

        self.snip_window = None
        self.screenshot = None

        self.text = ""
        self.text_area = text_area

        # Hide the ToText button initially
        self.to_text_button.pack_forget()

    def get_captured_text(self):
        return self.text

    def start_snipping(self):
        if self.snip_window:
            self.snip_window.destroy()

        self.master.withdraw()  # Hide the main window
        self.transparent_main_window()  # Make the main window transparent

        self.snip_window = tk.Toplevel(self.master)
        self.snip_window.attributes('-fullscreen', True)  # Set the new window to fullscreen
        self.setup_snip_canvas()

    def setup_snip_canvas(self):
        self.snip_window.wm_attributes("-alpha", 0.4)  # Set transparency for the snipping window

        # Get the screen dimensions
        screen_width = self.snip_window.winfo_screenwidth()
        screen_height = self.snip_window.winfo_screenheight()

        # Create a canvas covering the entire screen
        self.snip_canvas = tk.Canvas(self.snip_window, cursor="cross")

        self.screenshot = ImageGrab.grab()
        image_tk = ImageTk.PhotoImage(self.screenshot)

        self.snip_canvas.create_image(0, 0, anchor="nw", image=image_tk)
        self.snip_canvas.pack(fill=tk.BOTH, expand=True)

        self.snip_canvas.bind("<ButtonPress-1>", self.on_press)
        self.snip_canvas.bind("<B1-Motion>", self.on_drag)
        self.snip_canvas.bind("<ButtonRelease-1>", self.on_release)

        self.start_x = self.start_y = self.end_x = self.end_y = 0

    def on_press(self, event):
        self.start_x, self.start_y = event.x, event.y
        self.rect = self.snip_canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y, outline="red"
        )

    def on_drag(self, event):
        self.end_x, self.end_y = event.x, event.y
        self.snip_canvas.coords(self.rect, self.start_x, self.start_y, self.end_x, self.end_y)

    def on_release(self, event):
        canvas_width = self.snip_canvas.winfo_width()
        canvas_height = self.snip_canvas.winfo_height()
        self.start_x, self.start_y = self.start_x*(self.screenshot.width/canvas_width), self.start_y*(self.screenshot.height/canvas_height)
        self.end_x, self.end_y = event.x*(self.screenshot.width/canvas_width), event.y*(self.screenshot.height/canvas_height)

        self.snip_canvas.destroy()

        x, y = min(self.start_x, self.end_x) , min(self.start_y, self.end_y)
        width, height = abs(self.start_x - self.end_x), abs(self.start_y - self.end_y)

        screenshot = self.screenshot.crop((x, y, x + width, y + height))
        self.screenshot = screenshot
        self.save_screenshot(screenshot)

        self.restore_main_window()
        self.to_text_button.config(state=tk.NORMAL)  # Enable ToText button
        self.to_text_button.pack(side=tk.LEFT, padx=5, fill=tk.BOTH, expand=True)  # Show the ToText button

    def save_screenshot(self, screenshot):
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"screenshot_{timestamp}.png"
        screenshot.save(filename)
        print(f"Screenshot saved as {filename}")

        screenshot_tk = ImageTk.PhotoImage(screenshot)
        self.screenshot_label.config(image=screenshot_tk)
        self.screenshot_label.image = screenshot_tk

    def transparent_main_window(self):
        self.master.wm_attributes("-alpha", 0.0)

    def restore_main_window(self):
        self.master.wm_attributes("-alpha", 1.0)
        self.master.deiconify()

    def convert_to_text(self):
        if self.screenshot:
            self.text = self.image_to_text(self.screenshot)
            print("Text from image:\n", self.text)
            self.text_area.insert(tk.END, self.text)

    def image_to_text(self, image):
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        text = pytesseract.image_to_string(image)
        return text

def main():
    root = tk.Tk()
    root.geometry("800x600")
    app = SnippingTool(root)
    root.geometry("+%d+%d" % ((root.winfo_screenwidth() - root.winfo_reqwidth()) // 2, 0))
    root.mainloop()

if __name__ == "__main__":
    main()
