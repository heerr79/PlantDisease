import os
import numpy as np
import tensorflow as tf
from django.shortcuts import render
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import tensorflow.keras as keras
import base64
import uuid
import re
from io import BytesIO
from PIL import Image

# Load the model
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'leaf_disease_model.h5')

# Define disease labels
DISEASE_LABELS = ['Healthy', 'Bacterial Spot', 'Leaf Mold', 'Powdery Mildew']

# Create a simple fallback model if the real one isn't available
def create_fallback_model():
    model = keras.Sequential([
        keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
        keras.layers.MaxPooling2D((2, 2)),
        keras.layers.Flatten(),
        keras.layers.Dense(128, activation='relu'),
        keras.layers.Dense(len(DISEASE_LABELS), activation='softmax')
    ])
    model.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    return model

# Try to load the model, use fallback if it fails
try:
    if os.path.exists(MODEL_PATH) and os.path.getsize(MODEL_PATH) > 0:
        model = load_model(MODEL_PATH)
        # Verify the model has layers
        if len(model.layers) == 0:
            print("Warning: Model has no layers, using fallback model")
            model = create_fallback_model()
    else:
        print(f"Warning: Model file not found at {MODEL_PATH}, using fallback model")
        model = create_fallback_model()
except Exception as e:
    print(f"Error loading model: {e}")
    model = create_fallback_model()

def home(request):
    return render(request, 'home.html')

def preprocess_image(img_path):
    img = image.load_img(img_path, target_size=(224, 224))  # Ensure the right size
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    img_array /= 255.0  # Normalize
    return img_array

def get_regional_recommendations(disease, region=None):
    """Get region-specific recommendations for Maharashtra districts."""
    regional_advice = {}
    
    # Default recommendations (already implemented in get_care_recommendations)
    if not region:
        return {}
    
    # Region-specific recommendations for Maharashtra
    if region == "Mumbai":
        regional_advice = {
            'Healthy': {
                'weather': 'Mumbai\'s coastal climate is generally good for plants. Monitor during monsoon season.',
                'watering': 'Reduce watering during monsoon (June-September). Increase during hot summer months.',
                'soil': 'Add sand to improve drainage in Mumbai\'s often clayey soil.'
            },
            'Bacterial Spot': {
                'weather': 'Mumbai\'s high humidity increases risk. Ensure extra ventilation during monsoon.',
                'watering': 'Strictly avoid overhead watering in Mumbai\'s already humid climate.',
                'soil': 'Add organic compost to improve soil health and plant resistance.'
            },
            'Leaf Mold': {
                'weather': 'Critical to improve air circulation during Mumbai\'s monsoon season.',
                'watering': 'Minimal watering during monsoon months. Focus on soil drainage.',
                'soil': 'Mix in coarse sand to improve drainage in Mumbai\'s heavy soils.'
            },
            'Powdery Mildew': {
                'weather': 'Common in Mumbai\'s pre-monsoon humidity. Ensure plants get morning sun.',
                'watering': 'Water early morning to allow leaves to dry completely before evening.',
                'soil': 'Avoid excessive fertilization in Mumbai\'s already nutrient-rich soils.'
            }
        }
    elif region == "Pune":
        regional_advice = {
            'Healthy': {
                'weather': 'Pune\'s moderate climate is excellent for most plants. Protect from afternoon sun in summer.',
                'watering': 'Regular watering needed in Pune\'s dry winter months. Reduce during monsoon.',
                'soil': 'Pune\'s soil tends to be rocky - add compost to improve fertility.'
            },
            'Bacterial Spot': {
                'weather': 'Pune\'s relatively dry climate helps control bacterial spot. Monitor during monsoon.',
                'watering': 'Water at soil level, especially during Pune\'s monsoon season.',
                'soil': 'Add organic matter to improve Pune\'s often mineral-heavy soil.'
            },
            'Leaf Mold': {
                'weather': 'Primarily a concern during Pune\'s monsoon months. Ensure good spacing between plants.',
                'watering': 'Minimal watering during monsoon. Resume normal schedule in October.',
                'soil': 'Improve drainage with coarse sand in Pune\'s sometimes clayey soil.'
            },
            'Powdery Mildew': {
                'weather': 'Common in Pune\'s dry winter. Ensure adequate spacing for air circulation.',
                'watering': 'Avoid wetting leaves, especially in Pune\'s cooler winter months.',
                'soil': 'Balanced fertilization suitable for Pune\'s moderate soil conditions.'
            }
        }
    elif region == "Nagpur":
        regional_advice = {
            'Healthy': {
                'weather': 'Protect plants from Nagpur\'s extreme summer heat. Provide afternoon shade.',
                'watering': 'Consistent watering essential in Nagpur\'s hot, dry climate. Increase frequency in summer.',
                'soil': 'Add organic matter to improve water retention in Nagpur\'s often sandy soil.'
            },
            'Bacterial Spot': {
                'weather': 'Nagpur\'s dry climate helps control spread. Monitor during brief monsoon period.',
                'watering': 'Water early morning to allow complete drying before evening.',
                'soil': 'Add compost to improve soil health and plant resistance.'
            },
            'Leaf Mold': {
                'weather': 'Primarily a concern during Nagpur\'s brief but intense monsoon.',
                'watering': 'Reduce watering during monsoon months. Focus on soil drainage.',
                'soil': 'Improve soil structure with organic matter for better drainage.'
            },
            'Powdery Mildew': {
                'weather': 'Risk increases in Nagpur\'s winter months. Ensure plants receive morning sun.',
                'watering': 'Water at the base of plants, especially in cooler months.',
                'soil': 'Moderate fertilization to avoid excessive tender growth.'
            }
        }
    # Add more regions as needed
    else:
        # For other regions in Maharashtra, provide general Maharashtra recommendations
        regional_advice = {
            'Healthy': {
                'weather': 'Maharashtra\'s climate varies by region. Monitor local weather patterns.',
                'watering': 'Adjust watering based on monsoon intensity in your area.',
                'soil': 'Maharashtra soils vary widely. Test your soil and amend accordingly.'
            },
            'Bacterial Spot': {
                'weather': 'Ensure good ventilation, especially during Maharashtra\'s monsoon season.',
                'watering': 'Avoid overhead watering during humid monsoon months.',
                'soil': 'Improve soil drainage to prevent water stagnation.'
            },
            'Leaf Mold': {
                'weather': 'Provide adequate spacing between plants during monsoon season.',
                'watering': 'Reduce watering during monsoon months (June-September).',
                'soil': 'Add coarse materials to improve drainage in heavy soils.'
            },
            'Powdery Mildew': {
                'weather': 'Common in Maharashtra\'s pre-monsoon and winter periods. Ensure good air circulation.',
                'watering': 'Water early in the day so leaves can dry before evening.',
                'soil': 'Avoid excessive nitrogen fertilization which promotes susceptible new growth.'
            }
        }
    
    # Return recommendations for the specific disease if available
    return regional_advice.get(disease, {})

def get_care_recommendations(disease, region=None):
    """Generate care recommendations based on the detected disease and region."""
    recommendations = {
        'weather': '',
        'watering': '',
        'soil': '',
        'additional': []
    }
    
    # Base recommendations (unchanged from your existing code)
    if disease == 'Healthy':
        recommendations['weather'] = 'Maintain current conditions with good air circulation.'
        recommendations['watering'] = 'Regular watering, avoiding wetting the leaves.'
        recommendations['soil'] = 'Well-draining soil with appropriate nutrients for your plant type.'
        recommendations['additional'] = [
            'Continue your current care routine',
            'Monitor for any changes in leaf appearance',
            'Ensure adequate sunlight for your specific plant'
        ]
    
    elif disease == 'Bacterial Spot':
        recommendations['weather'] = 'Dry conditions with good air circulation. Avoid high humidity.'
        recommendations['watering'] = 'Water at the base of plants, keep foliage dry. Reduce watering frequency.'
        recommendations['soil'] = 'Well-draining soil. Consider adding organic matter to improve drainage.'
        recommendations['additional'] = [
            'Remove and destroy infected plant parts',
            'Avoid overhead watering',
            'Ensure good air circulation around plants',
            'Apply copper-based fungicides as a preventative measure',
            'Rotate crops in the affected area for the next season'
        ]
    
    elif disease == 'Leaf Mold':
        recommendations['weather'] = 'Increase air circulation and reduce humidity. Avoid damp, cloudy conditions.'
        recommendations['watering'] = 'Reduce watering frequency. Water at the base to keep foliage dry.'
        recommendations['soil'] = 'Well-draining soil with good aeration. Avoid compacted soil.'
        recommendations['additional'] = [
            'Improve air circulation around plants',
            'Remove and destroy infected leaves',
            'Water at the base of plants to keep foliage dry',
            'Apply fungicides containing chlorothalonil or mancozeb',
            'Space plants adequately to improve airflow'
        ]
    
    elif disease == 'Powdery Mildew':
        recommendations['weather'] = 'Increase air circulation. Powdery mildew thrives in humid conditions with moderate temperatures.'
        recommendations['watering'] = 'Water in the morning so leaves can dry during the day. Avoid overhead watering.'
        recommendations['soil'] = 'Well-draining soil. Avoid excessive nitrogen fertilization which promotes susceptible new growth.'
        recommendations['additional'] = [
            'Remove and destroy infected plant parts',
            'Ensure good air circulation',
            'Avoid overhead watering',
            'Apply fungicides containing sulfur or potassium bicarbonate',
            'Use neem oil as an organic alternative',
            'Prune plants to improve air circulation'
        ]
    
    # Override with region-specific recommendations if available
    if region:
        regional_recs = get_regional_recommendations(disease, region)
        if regional_recs:
            if 'weather' in regional_recs:
                recommendations['weather'] = regional_recs['weather']
            if 'watering' in regional_recs:
                recommendations['watering'] = regional_recs['watering']
            if 'soil' in regional_recs:
                recommendations['soil'] = regional_recs['soil']
            # We keep the additional recommendations from the base set
    
    return recommendations

def predict_disease(request):
    if request.method == 'POST':
        try:
            # Check if we have a file upload or base64 image data
            if request.FILES.get('image'):
                # Handle file upload
                image_file = request.FILES['image']
                file_name = default_storage.save(f'media/{image_file.name}', image_file)
                image_path = default_storage.path(file_name)
            elif request.POST.get('image_data'):
                # Handle base64 image data
                image_data = request.POST.get('image_data')
                # Remove the data URL prefix if present
                if 'data:image' in image_data:
                    format, imgstr = image_data.split(';base64,')
                else:
                    imgstr = image_data
                
                # Decode base64 string to image
                imgdata = base64.b64decode(imgstr)
                file_name = f'media/capture_{uuid.uuid4().hex}.jpg'
                
                # Save the image
                path = default_storage.save(file_name, ContentFile(imgdata))
                image_path = default_storage.path(path)
            else:
                return render(request, 'result.html', {'error': 'No image provided'})
            
            # Get the selected region (if any)
            region = request.POST.get('region', '')
            
            # Preprocess the image
            img_array = preprocess_image(image_path)
            
            # Get model predictions
            predictions = model.predict(img_array)
            predicted_class = DISEASE_LABELS[np.argmax(predictions)]
            
            # Add confidence score
            confidence = float(np.max(predictions)) * 100
            
            # Get care recommendations based on the detected disease and region
            care_recommendations = get_care_recommendations(predicted_class, region)
            
            context = {
                'result': predicted_class,
                'confidence': f"{confidence:.2f}%",
                'image_url': default_storage.url(file_name),
                'weather': care_recommendations['weather'],
                'watering': care_recommendations['watering'],
                'soil': care_recommendations['soil'],
                'additional_recommendations': care_recommendations['additional'],
                'selected_region': region
            }
            
            return render(request, 'result.html', context)
            
        except Exception as e:
            error_message = f"Error during prediction: {str(e)}"
            print(f"Error details: {e}")
            return render(request, 'result.html', {'error': error_message})

    return render(request, 'upload.html')
