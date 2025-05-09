import os
from django.shortcuts import render, redirect
from .forms import ImageUploadForm

# Dummy data for demo
disease_info = {
    "Tomato___Late_blight": {
        "english": {
            "name": "Tomato Late Blight",
            "remedy": "Use fungicides with chlorothalonil or copper. Remove infected leaves."
        },
        "nepali": {
            "name": "टमाटर ढिलो झुल",
            "remedy": "क्लोरोथालोनिल वा तामा भएको फङ्गीसाइड प्रयोग गर्नुहोस्। संक्रमित पात हटाउनुहोस्।"
        }
    },
    "Potato___Early_blight": {
        "english": {
            "name": "Potato Early Blight",
            "remedy": "Use certified seeds, rotate crops, and apply fungicide."
        },
        "nepali": {
            "name": "आलुको चाँडो झुल",
            "remedy": "प्रमाणित बीउ प्रयोग गर्नुहोस्, बाली परिवर्तन गर्नुहोस्, फङ्गीसाइड प्रयोग गर्नुहोस्।"
        }
    }
}

# Dummy classifier
def dummy_predict(image_path):
    return "Tomato___Late_blight"

def upload_view(request):
    if request.method == "POST":
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data["image"]
            image_path = f"media/{image.name}"
            with open(image_path, "wb+") as f:
                for chunk in image.chunks():
                    f.write(chunk)

            prediction = dummy_predict(image_path)
            data = disease_info.get(prediction)

            if not data:
                return render(request, "crop_monitoring/result.html", {
                    "disease_english": "Unknown",
                    "remedy_english": "No remedy available.",
                    "disease_nepali": "अज्ञात",
                    "remedy_nepali": "उपचार उपलब्ध छैन।"
                })

            return render(request, "crop_monitoring/result.html", {
                "disease_english": data["english"]["name"],
                "remedy_english": data["english"]["remedy"],
                "disease_nepali": data["nepali"]["name"],
                "remedy_nepali": data["nepali"]["remedy"]
            })
    else:
        form = ImageUploadForm()
    return render(request, "crop_monitoring/upload.html", {"form": form})
