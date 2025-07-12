
# AI Image Drawer and Sketch Converter

<img width="2048" height="2048" alt="Gemini_Generated_Image_efdehnefdehnefde" src="https://github.com/user-attachments/assets/9f2e276f-aec9-424d-90bc-69b19c258d62" />

An interactive Python application that allows users to draw, convert images to sketches, and automatically recreate images using AI-powered drawing techniques.

<img width="800" height="600" alt="image" src="https://github.com/user-attachments/assets/8ae91872-12a9-4f88-ac8f-b49f0c6250c4" />
<img width="800" height="600" alt="image" src="https://github.com/user-attachments/assets/5601606c-a3d9-4bdb-b6e8-d11c67bd8c57" />
<img width="800" height="600" alt="image" src="https://github.com/user-attachments/assets/762d893e-098c-459c-a54b-30ba04333602" />

## Features

- 🎨 **Free-hand Drawing**
  - Customizable brush size
  - Color picker with real-time preview
  - Smooth line drawing with anti-aliasing

- 🖼️ **Image Processing**
  - Load and display images
  - Convert images to sketch style
  - Auto-draw feature using edge detection and shading
  - Intelligent contour detection and reproduction

- 💾 **Drawing History**
  - Save drawings automatically
  - Browse previous drawings
  - Load and delete saved drawings
  - Timestamp-based organization

- 🛠️ **User Interface**
  - Clean and intuitive interface
  - Real-time color preview
  - Drawing tools panel
  - Image processing tools
  - Drawing history panel

## Installation

1. Clone the repository:
```bash
git clone https://github.com/tranhao-wq/Sketch-image-and-draw-Python.git
```

2. Install required packages:
```bash
pip install pillow numpy opencv-python
```

## Usage

1. Run the application:
```bash
python image_drawer.py
```

2. Features:
   - Click "Pick Color" to choose drawing color
   - Adjust brush size using the slider
   - Draw freely on the canvas
   - Load images using "Load Image"
   - Convert images to sketches with "Convert to Sketch"
   - Use "Auto Draw" to let AI recreate the image
   - Save your work with "Save Drawing"
   - Browse and load previous drawings from the history panel



## Technical Details

- **Image Processing**: Uses OpenCV for edge detection and contour finding
- **Drawing Algorithm**: 
  - Edge detection using Canny algorithm
  - Contour detection for precise line drawing
  - Intensity-based shading for depth and texture
  - Smooth line interpolation for natural drawing

- **Color Management**:
  - RGB and Hex color support
  - Alpha channel handling for shading
  - Dynamic color intensity based on image data

## Project Structure

```
.
├── image_drawer.py      # Main application file
├── drawing_history.py   # Drawing history management
├── drawings/           # Saved drawings directory
├── screenshots/        # Demo screenshots
└── README.md          # Documentation
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License

Copyright (c) 2025 Tran The Hao

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
