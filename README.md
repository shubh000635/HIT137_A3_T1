# HIT137_A3_T1
a comprehensive desktop image processing application that demonstrates excellent Object-Oriented Programming principles, professional GUI development, and advanced image processing capabilities
# Image Processing Desktop Application

A professional desktop application for image processing built with Python, Tkinter, and OpenCV. Features interactive cropping, real-time resizing, and comprehensive image manipulation tools.

## Features

### Core Functionality
- **Image Loading**: Load images from local device with file dialog
- **Interactive Cropping**: Click and drag to select crop areas with visual feedback
- **Real-time Resizing**: Slider control for instant image scaling (0.1x to 3.0x)
- **Save Options**: Save original, cropped, or resized images in multiple formats

### User Interface
- **Multi-Panel Layout**: Organized display with original, cropped, and resized views
- **Control Panel**: Intuitive controls with grouped functionality
- **Status Bar**: Real-time feedback and operation status
- **Responsive Design**: Adapts to window resizing

### Advanced Features
- **Visual Feedback**: Real-time selection rectangle during cropping
- **Smart Scaling**: Automatic image fitting with proper aspect ratio
- **Error Handling**: Comprehensive error checking and user notifications
- **Multiple Formats**: Support for PNG, JPEG, BMP, TIFF formats

## Requirements

```bash
pip install opencv-python pillow numpy
```

Note: `tkinter` is included with Python by default.

## How to Run

1. Ensure Python 3.7+ is installed
2. Install required packages:
   ```bash
   pip install opencv-python pillow numpy
   ```
3. Run the application:
   ```bash
   python image_processing_app.py
   ```

## User Guide

### Loading Images
1. Click "Load Image" button
2. Select an image file from the file dialog
3. Image will display in the main panel with size information

### Cropping Images
1. Load an image first
2. Click and drag on the original image to select crop area
3. Red dashed rectangle shows selection in real-time
4. Release mouse to complete crop
5. Cropped image appears in the left bottom panel

### Resizing Images
1. Crop an image first (resizing works on cropped images)
2. Use the scale slider to adjust size (0.1x to 3.0x)
3. Resized image updates in real-time in the right bottom panel
4. Scale factor displays next to slider

### Saving Images
- **Save Original**: Saves the loaded image
- **Save Cropped**: Saves the cropped version
- **Save Resized**: Saves the final resized image
- Choose format (PNG recommended for quality)

### Additional Controls
- **Clear Selection**: Remove current crop selection
- **Reset All**: Clear all images and start over

## Technical Implementation

### Object-Oriented Architecture

#### ImageProcessor Class
- Encapsulates all OpenCV image operations
- Handles loading, cropping, resizing, and saving
- Manages image format conversions

#### ImageCanvas Class
- Custom Tkinter Canvas with image display capabilities
- Handles mouse interactions for cropping
- Manages image scaling and positioning

#### ImageProcessingApp Class
- Main application controller
- Coordinates GUI components and image processing
- Manages application state and user interactions

### Key Technologies
- **OpenCV**: Core image processing operations
- **Tkinter**: GUI framework with professional styling
- **PIL/Pillow**: Image format handling and display
- **NumPy**: Efficient array operations

## Supported Image Formats

### Input Formats
- JPEG (.jpg, .jpeg)
- PNG (.png)
- BMP (.bmp)
- TIFF (.tiff, .tif)

### Output Formats
- PNG (recommended for quality)
- JPEG (smaller file size)

## File Structure

```
image_processing_app.py   # Main application file
README.md                 # This file
```

## Features Demonstration

### OOP Principles
- **Encapsulation**: Image processing logic separated from GUI
- **Inheritance**: Custom canvas extends Tkinter Canvas
- **Polymorphism**: Flexible image handling methods

### GUI Development
- Professional multi-panel layout
- Real-time user feedback
- Intuitive control organization
- Responsive design patterns

### Image Processing
- Interactive selection tools
- Real-time preview updates
- Quality-preserving operations
- Multiple format support

## Troubleshooting

### Common Issues
1. **Import Error**: Ensure all required packages are installed
2. **Image Won't Load**: Check file format is supported
3. **Slow Performance**: Large images may take time to process
4. **Save Failed**: Check file permissions and disk space

### Performance Tips
- Use PNG format for best quality
- Crop before resizing for better performance
- Close and reload for very large images

## Development Notes

This application demonstrates:
- Professional desktop application development
- Advanced Tkinter GUI programming
- OpenCV image processing integration
- Clean object-oriented design patterns
- User experience best practices

## License

Educational project - free to use and modify.
