"""
Image Processing Desktop Application
Demonstrates OOP principles, GUI development with Tkinter, and image processing with OpenCV

Features:
- Image loading from local device
- Interactive image cropping with mouse
- Real-time image resizing with slider
- Save modified images
- Professional GUI with multiple panels
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import cv2
import numpy as np
from PIL import Image, ImageTk
import os

class ImageProcessor:
    """
    Core image processing class handling OpenCV operations
    Demonstrates encapsulation of image processing logic
    """

    def __init__(self):
        self.original_image = None
        self.current_image = None
        self.cropped_image = None

    def load_image(self, file_path):
        """Load image from file path using OpenCV"""
        try:
            # Load image using OpenCV (BGR format)
            self.original_image = cv2.imread(file_path)
            if self.original_image is None:
                raise ValueError("Could not load image")

            # Convert BGR to RGB for display
            self.current_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB)
            return True
        except Exception as e:
            print(f"Error loading image: {e}")
            return False

    def crop_image(self, x1, y1, x2, y2):
        """Crop image based on coordinates"""
        if self.current_image is None:
            return None

        # Ensure coordinates are within image bounds
        h, w = self.current_image.shape[:2]
        x1, y1 = max(0, min(x1, w)), max(0, min(y1, h))
        x2, y2 = max(0, min(x2, w)), max(0, min(y2, h))

        # Ensure x1 < x2 and y1 < y2
        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y2, y1

        # Crop the image
        self.cropped_image = self.current_image[y1:y2, x1:x2]
        return self.cropped_image.copy()

    def resize_image(self, image, scale_factor):
        """Resize image by scale factor"""
        if image is None:
            return None

        h, w = image.shape[:2]
        new_w = int(w * scale_factor)
        new_h = int(h * scale_factor)

        # Use appropriate interpolation based on scaling
        interpolation = cv2.INTER_CUBIC if scale_factor > 1 else cv2.INTER_AREA
        resized = cv2.resize(image, (new_w, new_h), interpolation=interpolation)
        return resized

    def save_image(self, image, file_path):
        """Save image to file"""
        try:
            # Convert RGB back to BGR for OpenCV saving
            bgr_image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            cv2.imwrite(file_path, bgr_image)
            return True
        except Exception as e:
            print(f"Error saving image: {e}")
            return False

    def get_original_image(self):
        """Get original image (RGB format)"""
        return self.current_image

    def get_cropped_image(self):
        """Get cropped image"""
        return self.cropped_image

class ImageCanvas(tk.Canvas):
    """
    Custom Canvas class for image display and interaction
    Demonstrates inheritance and polymorphism
    """

    def __init__(self, parent, width=400, height=300, **kwargs):
        super().__init__(parent, width=width, height=height, bg='white', **kwargs)

        self.image_item = None
        self.photo_image = None
        self.selection_rect = None
        self.start_x = None
        self.start_y = None
        self.scale_factor = 1.0
        self.image_offset_x = 0
        self.image_offset_y = 0

        # Bind mouse events for cropping
        self.bind("<Button-1>", self.start_selection)
        self.bind("<B1-Motion>", self.update_selection)
        self.bind("<ButtonRelease-1>", self.end_selection)

        # Callback for crop completion
        self.crop_callback = None

    def set_crop_callback(self, callback):
        """Set callback function for when cropping is completed"""
        self.crop_callback = callback

    def display_image(self, cv_image, fit_to_canvas=True):
        """Display OpenCV image on canvas"""
        if cv_image is None:
            return

        # Convert OpenCV image to PIL format
        pil_image = Image.fromarray(cv_image)

        if fit_to_canvas:
            # Calculate scale to fit image in canvas
            canvas_width = self.winfo_width()
            canvas_height = self.winfo_height()

            if canvas_width <= 1 or canvas_height <= 1:
                canvas_width, canvas_height = 400, 300

            img_width, img_height = pil_image.size

            scale_x = canvas_width / img_width
            scale_y = canvas_height / img_height
            self.scale_factor = min(scale_x, scale_y, 1.0)  # Don't upscale

            new_width = int(img_width * self.scale_factor)
            new_height = int(img_height * self.scale_factor)

            pil_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Center the image
            self.image_offset_x = (canvas_width - new_width) // 2
            self.image_offset_y = (canvas_height - new_height) // 2
        else:
            self.image_offset_x = 0
            self.image_offset_y = 0

        # Convert to PhotoImage for Tkinter
        self.photo_image = ImageTk.PhotoImage(pil_image)

        # Clear previous image and display new one
        self.delete("all")
        self.image_item = self.create_image(
            self.image_offset_x, self.image_offset_y, 
            anchor=tk.NW, image=self.photo_image
        )

    def start_selection(self, event):
        """Start rectangle selection for cropping"""
        self.start_x = event.x
        self.start_y = event.y

        # Remove previous selection
        if self.selection_rect:
            self.delete(self.selection_rect)

    def update_selection(self, event):
        """Update selection rectangle while dragging"""
        if self.start_x is None or self.start_y is None:
            return

        # Remove previous rectangle
        if self.selection_rect:
            self.delete(self.selection_rect)

        # Draw new rectangle
        self.selection_rect = self.create_rectangle(
            self.start_x, self.start_y, event.x, event.y,
            outline='red', width=2, dash=(5, 5)
        )

    def end_selection(self, event):
        """End selection and trigger crop"""
        if self.start_x is None or self.start_y is None:
            return

        # Calculate actual image coordinates
        img_x1 = int((self.start_x - self.image_offset_x) / self.scale_factor)
        img_y1 = int((self.start_y - self.image_offset_y) / self.scale_factor)
        img_x2 = int((event.x - self.image_offset_x) / self.scale_factor)
        img_y2 = int((event.y - self.image_offset_y) / self.scale_factor)

        # Trigger crop callback if set
        if self.crop_callback and abs(img_x2 - img_x1) > 10 and abs(img_y2 - img_y1) > 10:
            self.crop_callback(img_x1, img_y1, img_x2, img_y2)

        # Reset selection
        self.start_x = None
        self.start_y = None

    def clear_selection(self):
        """Clear current selection rectangle"""
        if self.selection_rect:
            self.delete(self.selection_rect)
            self.selection_rect = None

class ImageProcessingApp:
    """
    Main application class demonstrating OOP principles
    Manages GUI components and coordinates image processing operations
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Image Processing Application")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)

        # Initialize image processor
        self.processor = ImageProcessor()

        # Current state
        self.current_cropped_image = None
        self.current_resized_image = None

        # Setup GUI
        self.setup_gui()

        # Setup styles
        self.setup_styles()

    def setup_styles(self):
        """Setup custom styles for the application"""
        style = ttk.Style()
        style.theme_use('clam')

        # Configure custom styles
        style.configure('Title.TLabel', font=('Arial', 12, 'bold'))
        style.configure('Info.TLabel', font=('Arial', 10))

    def setup_gui(self):
        """Setup the main GUI layout"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # Setup control panel
        self.setup_control_panel(main_frame)

        # Setup image display area
        self.setup_image_display(main_frame)

        # Setup status bar
        self.setup_status_bar(main_frame)

    def setup_control_panel(self, parent):
        """Setup left control panel"""
        control_frame = ttk.LabelFrame(parent, text="Controls", padding="10")
        control_frame.grid(row=0, column=0, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))

        # Load Image Section
        load_frame = ttk.LabelFrame(control_frame, text="Image Loading", padding="5")
        load_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Button(
            load_frame, text="Load Image", 
            command=self.load_image
        ).pack(fill=tk.X)

        self.image_info_label = ttk.Label(load_frame, text="No image loaded", style='Info.TLabel')
        self.image_info_label.pack(fill=tk.X, pady=(5, 0))

        # Cropping Section
        crop_frame = ttk.LabelFrame(control_frame, text="Image Cropping", padding="5")
        crop_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(crop_frame, text="Click and drag on the original image\nto select crop area", 
                 style='Info.TLabel').pack()

        ttk.Button(
            crop_frame, text="Clear Selection", 
            command=self.clear_crop_selection
        ).pack(fill=tk.X, pady=(5, 0))

        # Resizing Section
        resize_frame = ttk.LabelFrame(control_frame, text="Image Resizing", padding="5")
        resize_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(resize_frame, text="Scale Factor:", style='Info.TLabel').pack()

        self.scale_var = tk.DoubleVar(value=1.0)
        self.scale_slider = ttk.Scale(
            resize_frame, from_=0.1, to=3.0, 
            variable=self.scale_var, orient=tk.HORIZONTAL,
            command=self.on_scale_change
        )
        self.scale_slider.pack(fill=tk.X, pady=(5, 0))

        self.scale_label = ttk.Label(resize_frame, text="1.0x", style='Info.TLabel')
        self.scale_label.pack()

        # Save Section
        save_frame = ttk.LabelFrame(control_frame, text="Save Image", padding="5")
        save_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Button(
            save_frame, text="Save Original", 
            command=lambda: self.save_image("original")
        ).pack(fill=tk.X, pady=(0, 2))

        ttk.Button(
            save_frame, text="Save Cropped", 
            command=lambda: self.save_image("cropped")
        ).pack(fill=tk.X, pady=(0, 2))

        ttk.Button(
            save_frame, text="Save Resized", 
            command=lambda: self.save_image("resized")
        ).pack(fill=tk.X)

        # Reset Section
        reset_frame = ttk.LabelFrame(control_frame, text="Reset", padding="5")
        reset_frame.pack(fill=tk.X)

        ttk.Button(
            reset_frame, text="Reset All", 
            command=self.reset_all
        ).pack(fill=tk.X)

    def setup_image_display(self, parent):
        """Setup image display area with multiple panels"""
        display_frame = ttk.Frame(parent)
        display_frame.grid(row=0, column=1, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        display_frame.columnconfigure(0, weight=1)
        display_frame.columnconfigure(1, weight=1)
        display_frame.rowconfigure(1, weight=1)
        display_frame.rowconfigure(3, weight=1)

        # Original Image
        ttk.Label(display_frame, text="Original Image", style='Title.TLabel').grid(
            row=0, column=0, columnspan=2, pady=(0, 5)
        )

        self.original_canvas = ImageCanvas(display_frame, width=500, height=300)
        self.original_canvas.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        self.original_canvas.set_crop_callback(self.on_crop_selection)

        # Cropped and Resized Images
        ttk.Label(display_frame, text="Cropped Image", style='Title.TLabel').grid(
            row=2, column=0, pady=(10, 5), sticky=tk.W
        )

        ttk.Label(display_frame, text="Resized Image", style='Title.TLabel').grid(
            row=2, column=1, pady=(10, 5), sticky=tk.W
        )

        self.cropped_canvas = ImageCanvas(display_frame, width=250, height=200)
        self.cropped_canvas.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))

        self.resized_canvas = ImageCanvas(display_frame, width=250, height=200)
        self.resized_canvas.grid(row=3, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))

    def setup_status_bar(self, parent):
        """Setup status bar at bottom"""
        self.status_var = tk.StringVar(value="Ready - Load an image to begin")
        status_bar = ttk.Label(parent, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))

    def load_image(self):
        """Load image from file dialog"""
        file_types = [
            ("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff *.tif"),
            ("JPEG files", "*.jpg *.jpeg"),
            ("PNG files", "*.png"),
            ("All files", "*.*")
        ]

        file_path = filedialog.askopenfilename(
            title="Select an image",
            filetypes=file_types
        )

        if file_path:
            if self.processor.load_image(file_path):
                # Display original image
                original_img = self.processor.get_original_image()
                self.original_canvas.display_image(original_img)

                # Update info label
                h, w = original_img.shape[:2]
                file_name = os.path.basename(file_path)
                self.image_info_label.config(text=f"{file_name}\n{w}x{h} pixels")

                # Reset other displays
                self.cropped_canvas.delete("all")
                self.resized_canvas.delete("all")
                self.current_cropped_image = None
                self.current_resized_image = None

                # Reset scale
                self.scale_var.set(1.0)
                self.scale_label.config(text="1.0x")

                self.status_var.set(f"Loaded: {file_name}")
            else:
                messagebox.showerror("Error", "Failed to load image. Please check the file format.")
                self.status_var.set("Error loading image")

    def on_crop_selection(self, x1, y1, x2, y2):
        """Handle crop selection from canvas"""
        cropped_img = self.processor.crop_image(x1, y1, x2, y2)
        if cropped_img is not None:
            self.current_cropped_image = cropped_img
            self.cropped_canvas.display_image(cropped_img)

            # Reset resize scale and update resized image
            self.scale_var.set(1.0)
            self.scale_label.config(text="1.0x")
            self.update_resized_image()

            h, w = cropped_img.shape[:2]
            self.status_var.set(f"Cropped to {w}x{h} pixels")

    def clear_crop_selection(self):
        """Clear crop selection"""
        self.original_canvas.clear_selection()
        self.status_var.set("Crop selection cleared")

    def on_scale_change(self, value):
        """Handle scale slider change"""
        scale = float(value)
        self.scale_label.config(text=f"{scale:.1f}x")
        self.update_resized_image()

    def update_resized_image(self):
        """Update resized image display"""
        if self.current_cropped_image is not None:
            scale = self.scale_var.get()
            resized_img = self.processor.resize_image(self.current_cropped_image, scale)
            if resized_img is not None:
                self.current_resized_image = resized_img
                self.resized_canvas.display_image(resized_img)

                h, w = resized_img.shape[:2]
                self.status_var.set(f"Resized to {w}x{h} pixels (scale: {scale:.1f}x)")

    def save_image(self, image_type):
        """Save specified image type"""
        if image_type == "original":
            image_to_save = self.processor.get_original_image()
            default_name = "original_image.png"
        elif image_type == "cropped":
            image_to_save = self.current_cropped_image
            default_name = "cropped_image.png"
        elif image_type == "resized":
            image_to_save = self.current_resized_image
            default_name = "resized_image.png"
        else:
            return

        if image_to_save is None:
            messagebox.showwarning("Warning", f"No {image_type} image available to save.")
            return

        file_path = filedialog.asksaveasfilename(
            title=f"Save {image_type} image",
            defaultextension=".png",
            initialfile=default_name,
            filetypes=[
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg"),
                ("All files", "*.*")
            ]
        )

        if file_path:
            if self.processor.save_image(image_to_save, file_path):
                messagebox.showinfo("Success", f"{image_type.capitalize()} image saved successfully!")
                self.status_var.set(f"Saved {image_type} image: {os.path.basename(file_path)}")
            else:
                messagebox.showerror("Error", f"Failed to save {image_type} image.")
                self.status_var.set(f"Error saving {image_type} image")

    def reset_all(self):
        """Reset all images and controls"""
        # Clear processor
        self.processor = ImageProcessor()

        # Clear canvases
        self.original_canvas.delete("all")
        self.cropped_canvas.delete("all")
        self.resized_canvas.delete("all")

        # Reset variables
        self.current_cropped_image = None
        self.current_resized_image = None
        self.scale_var.set(1.0)
        self.scale_label.config(text="1.0x")

        # Reset labels
        self.image_info_label.config(text="No image loaded")
        self.status_var.set("Reset complete - Load an image to begin")

def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = ImageProcessingApp(root)

    # Center window on screen
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")

    root.mainloop()

if __name__ == "__main__":
    main()
