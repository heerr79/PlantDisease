# 🌿 Plant Disease Detection System
<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Django](https://img.shields.io/badge/Django-4.0+-green.svg)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.0+-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**AI-Powered Plant Disease Detection with Regional Recommendations**

[🚀 Live Demo](#) • [📖 Documentation](#) • [🐛 Report Issues](#)

</div>

---

## 🌟 Features

### 🔬 **Advanced AI Detection**
- **Deep Learning Model**: Powered by TensorFlow/Keras with CNN architecture
- **Multi-Disease Classification**: Detects 4 different plant conditions:
  - 🌱 **Healthy** - Confirms plant wellness
  - 🦠 **Bacterial Spot** - Identifies bacterial infections
  - 🍃 **Leaf Mold** - Detects fungal leaf mold
  - ⚪ **Powdery Mildew** - Recognizes powdery mildew fungus
- **High Accuracy**: Real-time prediction with confidence scores

### 📱 **User-Friendly Interface**
- **Drag & Drop Upload**: Easy image upload functionality
- **Camera Capture**: Direct photo capture from device camera
- **Real-time Processing**: Instant disease detection and analysis
- **Responsive Design**: Works seamlessly on desktop and mobile devices

### 🗺️ **Regional Intelligence**
- **Maharashtra-Specific Recommendations**: Tailored advice for different regions:
  - 🏙️ **Mumbai**: Coastal climate considerations
  - 🏔️ **Pune**: Moderate climate adaptations
  - 🌞 **Nagpur**: Hot climate management
  - 🏘️ **Other Maharashtra Regions**: General regional guidance

### 💡 **Smart Recommendations**
Each detection provides comprehensive care advice:
- **🌤️ Weather Management**: Climate-specific guidance
- **💧 Watering Instructions**: Optimal watering practices
- **🌱 Soil Care**: Soil improvement recommendations
- **🔧 Treatment Steps**: Detailed treatment procedures

---

## 🛠️ Technology Stack

| Component | Technology | Version |
|-----------|------------|---------|
| **Backend** | Django | 4.0+ |
| **AI/ML** | TensorFlow/Keras | 2.0+ |
| **Frontend** | HTML5, CSS3, JavaScript | - |
| **Database** | SQLite | - |
| **Image Processing** | PIL/Pillow | - |
| **Deployment** | Django Development Server | - |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/plant-disease-detection.git
   cd plant-disease-detection
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Start the development server**
   ```bash
   python manage.py runserver
   ```

6. **Open your browser**
   ```
   http://127.0.0.1:8000/
   ```

---

## 📁 Project Structure

```
plant_disease_det/
├── 📁 disease_detection/          # Main Django app
│   ├── 📁 templates/             # HTML templates
│   │   ├── base.html            # Base template
│   │   ├── home.html            # Homepage
│   │   ├── upload.html          # Upload interface
│   │   └── result.html          # Results display
│   ├── views.py                 # Main application logic
│   ├── urls.py                  # URL routing
│   ├── models.py                # Database models
│   └── leaf_disease_model.h5    # Trained AI model
├── 📁 plant_disease_det/        # Django project settings
│   ├── settings.py              # Project configuration
│   ├── urls.py                  # Main URL configuration
│   └── wsgi.py                  # WSGI configuration
├── 📁 media/                    # Uploaded images
├── manage.py                    # Django management script
└── README.md                    # This file
```

---

## 🎯 How It Works

### 1. **Image Upload/Capture**
   - Users can upload images or capture photos directly
   - Supports multiple image formats (JPG, PNG, etc.)

### 2. **AI Processing**
   - Images are preprocessed to 224x224 pixels
   - Deep learning model analyzes the image
   - Returns disease classification with confidence score

### 3. **Regional Analysis**
   - System considers user's selected region
   - Provides climate-specific recommendations
   - Adapts advice for local weather conditions

### 4. **Comprehensive Results**
   - Disease diagnosis with confidence percentage
   - Detailed care recommendations
   - Treatment procedures and prevention tips

---

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the root directory:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Model Configuration
The AI model is pre-trained and ready to use. The model file `leaf_disease_model.h5` contains:
- **Architecture**: Convolutional Neural Network
- **Input Size**: 224x224x3 (RGB images)
- **Classes**: 4 disease categories
- **Training**: Optimized for plant leaf images

---

## 📊 Supported Diseases

| Disease | Description | Symptoms | Treatment |
|---------|-------------|----------|-----------|
| **Healthy** | Plant is in good condition | Normal green leaves, no spots | Maintain current care routine |
| **Bacterial Spot** | Bacterial infection | Dark spots with yellow halos | Remove infected parts, apply copper fungicide |
| **Leaf Mold** | Fungal infection | Yellow spots with gray mold | Improve air circulation, apply fungicide |
| **Powdery Mildew** | Fungal disease | White powdery spots | Apply sulfur-based fungicide, improve ventilation |

---

## 🌍 Regional Support

### Maharashtra Regions
- **Mumbai**: Coastal climate with high humidity
- **Pune**: Moderate climate with distinct seasons
- **Nagpur**: Hot and dry climate
- **Other Regions**: General Maharashtra guidance

### Climate Considerations
- **Monsoon Season** (June-September): Special watering and ventilation advice
- **Summer Months**: Heat stress management
- **Winter Period**: Cold protection measures

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit your changes**
   ```bash
   git commit -m 'Add amazing feature'
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open a Pull Request**

### Development Guidelines
- Follow PEP 8 Python style guide
- Add tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting

---

## 🐛 Troubleshooting

### Common Issues

**Model Loading Error**
```bash
# Ensure the model file exists
ls disease_detection/leaf_disease_model.h5
```

**Django Import Error**
```bash
# Activate virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

**Image Upload Issues**
- Check file permissions in media directory
- Ensure image format is supported (JPG, PNG)
- Verify file size is reasonable (< 10MB)

---

## 📈 Performance

- **Processing Time**: < 2 seconds per image
- **Accuracy**: > 90% on test dataset
- **Supported Formats**: JPG, PNG, JPEG
- **Max File Size**: 10MB
- **Concurrent Users**: Limited by server capacity

---

## 🔒 Security

- **File Upload Validation**: Secure image processing
- **CSRF Protection**: Django's built-in security
- **Input Sanitization**: Prevents malicious uploads
- **Error Handling**: Graceful failure management

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Dataset**: PlantVillage dataset for training
- **Framework**: Django for web framework
- **AI Library**: TensorFlow/Keras for deep learning
- **UI Components**: Modern web technologies

---

## 📞 Support

- **Email**: support@plantdisease.com
- **Issues**: [GitHub Issues](https://github.com/yourusername/plant-disease-detection/issues)
- **Documentation**: [Wiki](https://github.com/yourusername/plant-disease-detection/wiki)

---

<div align="center">

**Made with ❤️ for better plant care**

[⬆️ Back to Top](#-plant-disease-detection-system)

</div> 
