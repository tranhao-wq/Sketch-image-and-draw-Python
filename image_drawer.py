import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser, ttk
from PIL import Image, ImageTk, ImageDraw
import numpy as np
import cv2
import os
import io
from datetime import datetime
from drawing_history import DrawingHistory

class ImageDrawer:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Image Drawer")
        
        # Create main frame
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(padx=10, pady=10)
        
        # Create canvas
        self.canvas_width = 800
        self.canvas_height = 600
        self.canvas = tk.Canvas(self.main_frame, width=self.canvas_width, 
                              height=self.canvas_height, bg='white')
        self.canvas.pack(side=tk.LEFT)
        
        # Drawing variables
        self.current_color = '#000000'
        self.brush_size = 2
        self.drawing = False
        self.last_x = None
        self.last_y = None
        
        # Bind mouse events
        self.canvas.bind('<Button-1>', self.start_drawing)
        self.canvas.bind('<B1-Motion>', self.draw)
        self.canvas.bind('<ButtonRelease-1>', self.stop_drawing)
        
        # Create button frame
        self.button_frame = tk.Frame(self.main_frame)
        self.button_frame.pack(side=tk.RIGHT, padx=10)
        
        # Create control panel
        self.control_panel = tk.Frame(self.button_frame)
        self.control_panel.pack(pady=10)
        
        # Drawing tools
        self.drawing_tools = tk.LabelFrame(self.control_panel, text="Drawing Tools")
        self.drawing_tools.pack(pady=5, fill="x")
        
        # Color picker
        self.color_button = tk.Button(self.drawing_tools, text="Pick Color", 
                                    command=self.choose_color, bg=self.current_color)
        self.color_button.pack(pady=5)
        
        # Brush size
        tk.Label(self.drawing_tools, text="Brush Size:").pack()
        self.size_scale = tk.Scale(self.drawing_tools, from_=1, to=20, 
                                 orient="horizontal",
                                 command=self.update_brush_size)
        self.size_scale.set(2)
        self.size_scale.pack()
        
        # Image processing tools
        self.image_tools = tk.LabelFrame(self.control_panel, text="Image Tools")
        self.image_tools.pack(pady=5, fill="x")
        
        self.load_button = tk.Button(self.image_tools, text="Load Image", 
                                   command=self.load_image)
        self.load_button.pack(pady=5)
        
        self.sketch_button = tk.Button(self.image_tools, text="Convert to Sketch", 
                                     command=self.convert_to_sketch)
        self.sketch_button.pack(pady=5)
        
        self.draw_button = tk.Button(self.image_tools, text="Auto Draw", 
                                   command=self.draw_image)
        self.draw_button.pack(pady=5)
        
        self.clear_button = tk.Button(self.image_tools, text="Clear Canvas", 
                                    command=self.clear_canvas)
        self.clear_button.pack(pady=5)
        
        self.save_button = tk.Button(self.image_tools, text="Save Drawing", 
                                   command=self.save_drawing)
        self.save_button.pack(pady=5)
        
        # Initialize image variable
        self.image = None
        self.photo = None
        
        # Initialize drawing history
        self.history = DrawingHistory()
        
        # Create history panel
        self.create_history_panel()

    def load_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")])
        if file_path:
            try:
                self.image = Image.open(file_path)
                # Resize image to fit canvas while maintaining aspect ratio
                ratio = min(self.canvas_width/self.image.width, 
                          self.canvas_height/self.image.height)
                new_width = int(self.image.width * ratio)
                new_height = int(self.image.height * ratio)
                self.image = self.image.resize((new_width, new_height), 
                                             Image.Resampling.LANCZOS)
                self.photo = ImageTk.PhotoImage(self.image)
                self.canvas.create_image(self.canvas_width//2, 
                                       self.canvas_height//2, 
                                       image=self.photo)
            except Exception as e:
                messagebox.showerror("Error", f"Could not load image: {str(e)}")

    def draw_image(self):
        if self.image is None:
            messagebox.showwarning("Warning", "Please load an image first!")
            return
            
        self.clear_canvas()
        img_array = np.array(self.image)
        
        # Convert to grayscale if image is not already
        if len(img_array.shape) == 3:
            img_gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        else:
            img_gray = img_array
            
        height, width = img_gray.shape[:2]
        
        # Calculate starting position to center the drawing
        start_x = (self.canvas_width - width) // 2
        start_y = (self.canvas_height - height) // 2
        
        # Edge detection for better accuracy
        edges = cv2.Canny(img_gray, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        
        # Get RGB values from current color (hex to RGB)
        r = int(self.current_color[1:3], 16)
        g = int(self.current_color[3:5], 16)
        b = int(self.current_color[5:7], 16)
        
        # Draw contours with current color
        for contour in contours:
            points = []
            for point in contour:
                x, y = point[0]
                points.extend([start_x + x, start_y + y])
            
            if len(points) >= 4:  # Need at least 2 points to draw a line
                # Create line with current color and smooth edges
                self.canvas.create_line(points, 
                                     fill=self.current_color, 
                                     width=1.5,
                                     smooth=True,
                                     capstyle=tk.ROUND,
                                     joinstyle=tk.ROUND)
        
        # Add shading with transparency based on original image
        for y in range(0, height, 3):
            for x in range(0, width, 3):
                pixel_value = img_gray[y, x]
                if pixel_value < 200:  # Only shade darker areas
                    intensity = 1 - (pixel_value / 255.0)  # Convert to 0-1 range
                    
                    # Calculate semi-transparent color
                    alpha = intensity
                    shade_color = f'#{int(r*alpha):02x}{int(g*alpha):02x}{int(b*alpha):02x}'
                    
                    size = max(1, int(intensity * 3))
                    self.canvas.create_oval(
                        start_x + x, start_y + y,
                        start_x + x + size, start_y + y + size,
                        fill=shade_color,
                        outline=shade_color
                    )
        
        self.root.update()

    def clear_canvas(self):
        self.canvas.delete("all")

    def choose_color(self):
        color = colorchooser.askcolor(color=self.current_color)
        if color[1]:  # color[1] is the hex string
            self.current_color = color[1]
            # Update button color and text color for better visibility
            self.color_button.config(bg=self.current_color, 
                                   fg='white' if sum(int(self.current_color[i:i+2], 16) for i in (1,3,5)) < 384 else 'black')
    
    def update_brush_size(self, size):
        self.brush_size = int(size)
    
    def start_drawing(self, event):
        self.drawing = True
        self.last_x = event.x
        self.last_y = event.y
        # Draw initial point
        self.canvas.create_oval(self.last_x - self.brush_size/2,
                              self.last_y - self.brush_size/2,
                              self.last_x + self.brush_size/2,
                              self.last_y + self.brush_size/2,
                              fill=self.current_color,
                              outline=self.current_color)
    
    def draw(self, event):
        if self.drawing:
            x, y = event.x, event.y
            # Create smooth line with current color
            line = self.canvas.create_line(self.last_x, self.last_y, x, y,
                                         width=self.brush_size,
                                         fill=self.current_color,
                                         capstyle=tk.ROUND,
                                         joinstyle=tk.ROUND,
                                         smooth=True)
            # Draw circle at the current point for smoother lines
            self.canvas.create_oval(x - self.brush_size/2,
                                  y - self.brush_size/2,
                                  x + self.brush_size/2,
                                  y + self.brush_size/2,
                                  fill=self.current_color,
                                  outline=self.current_color)
            self.last_x = x
            self.last_y = y
    
    def stop_drawing(self, event):
        self.drawing = False
    
    def save_drawing(self):
        # Create drawings folder if it doesn't exist
        if not os.path.exists('drawings'):
            os.makedirs('drawings')
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"drawings/drawing_{timestamp}.png"
        
        # Create a PIL image from canvas
        img = Image.new('RGB', (self.canvas_width, self.canvas_height), 'white')
        draw = ImageDraw.Draw(img)
        
        # Get all canvas items and draw them
        for item in self.canvas.find_all():
            coords = self.canvas.coords(item)
            item_type = self.canvas.type(item)
            
            if item_type == 'line' and len(coords) >= 4:
                try:
                    color = self.canvas.itemcget(item, 'fill') or 'black'
                    width = int(float(self.canvas.itemcget(item, 'width') or '1'))
                    # Draw line segments
                    for i in range(0, len(coords)-2, 2):
                        draw.line([coords[i], coords[i+1], coords[i+2], coords[i+3]], 
                                 fill=color, width=width)
                except:
                    continue
            elif item_type == 'oval' and len(coords) >= 4:
                try:
                    color = self.canvas.itemcget(item, 'fill') or 'black'
                    draw.ellipse(coords, fill=color)
                except:
                    continue
        
        img.save(filename)
        
        # Add to history
        self.history.add_drawing(os.path.basename(filename))
        self.update_history_list()
        
        messagebox.showinfo("Success", f"Drawing saved as {filename}")

    def convert_to_sketch(self):
        if self.image is None:
            messagebox.showwarning("Warning", "Please load an image first!")
            return
            
        # Convert to grayscale
        img_gray = cv2.cvtColor(np.array(self.image), cv2.COLOR_RGB2GRAY)
        
        # Invert the grayscale image
        img_invert = cv2.bitwise_not(img_gray)
        
        # Apply Gaussian blur
        img_blur = cv2.GaussianBlur(img_invert, (21, 21), sigmaX=0, sigmaY=0)
        
        # Blend the grayscale image with the blurred inverse
        sketch = cv2.divide(img_gray, 255 - img_blur, scale=256)
        
        # Convert back to PIL Image
        self.image = Image.fromarray(sketch)
        self.photo = ImageTk.PhotoImage(self.image)
        self.clear_canvas()
        self.canvas.create_image(self.canvas_width//2, 
                               self.canvas_height//2, 
                               image=self.photo)

    def create_history_panel(self):
        # History panel
        self.history_frame = tk.LabelFrame(self.control_panel, text="Drawing History")
        self.history_frame.pack(pady=5, fill="both", expand=True)
        
        # History listbox with scrollbar
        list_frame = tk.Frame(self.history_frame)
        list_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.history_listbox = tk.Listbox(list_frame, height=8)
        scrollbar = tk.Scrollbar(list_frame, orient="vertical")
        self.history_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.history_listbox.yview)
        
        self.history_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # History buttons
        history_buttons = tk.Frame(self.history_frame)
        history_buttons.pack(fill="x", padx=5, pady=5)
        
        tk.Button(history_buttons, text="Load", command=self.load_from_history).pack(side="left", padx=2)
        tk.Button(history_buttons, text="Delete", command=self.delete_from_history).pack(side="left", padx=2)
        
        self.update_history_list()
    
    def update_history_list(self):
        self.history_listbox.delete(0, tk.END)
        for entry in self.history.get_recent(20):
            display_text = f"{entry['title']} - {entry['timestamp'][:16]}"
            self.history_listbox.insert(tk.END, display_text)
    
    def load_from_history(self):
        selection = self.history_listbox.curselection()
        if selection:
            index = selection[0]
            recent_history = self.history.get_recent(20)
            if index < len(recent_history):
                entry = recent_history[index]
                if os.path.exists(entry['path']):
                    self.image = Image.open(entry['path'])
                    self.photo = ImageTk.PhotoImage(self.image)
                    self.clear_canvas()
                    self.canvas.create_image(self.canvas_width//2, 
                                           self.canvas_height//2, 
                                           image=self.photo)
                else:
                    messagebox.showerror("Error", "File not found!")
    
    def delete_from_history(self):
        selection = self.history_listbox.curselection()
        if selection:
            index = selection[0]
            recent_history = self.history.get_recent(20)
            if index < len(recent_history):
                # Find actual index in full history
                entry = recent_history[index]
                full_history = self.history.get_history()
                actual_index = next(i for i, e in enumerate(full_history) if e == entry)
                
                if messagebox.askyesno("Confirm", "Delete this drawing?"):
                    self.history.delete_drawing(actual_index)
                    self.update_history_list()

def main():
    root = tk.Tk()
    app = ImageDrawer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
