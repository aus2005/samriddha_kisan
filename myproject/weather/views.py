import requests
from django.shortcuts import render
from .districts import DISTRICTS
import os


API_KEY = os.environ.get("OPENWEATHERMAP_API_KEY", "80a37ac3ff742b2cdd854dc33974c4e7")



def translate_weather_desc(desc):
    translations = {
        'clear sky': 'स्पष्ट आकाश',
        'few clouds': 'थोरै बादल',
        'scattered clouds': 'छरिएका बादल',
        'broken clouds': 'चुँडिएका बादल',
        'shower rain': 'अत्यधिक वर्षा',
        'rain': 'वर्षा',
        'light rain': 'हल्का वर्षा',
        'moderate rain': 'मध्यम वर्षा',
        'heavy intensity rain': 'भारी वर्षा',
        'thunderstorm': 'मेघ गर्जन',
        'snow': 'हिउँ',
        'mist': 'कुहिरो',
        'overcast clouds': 'घना बादल',
        'haze': 'धुम्म वातावरण',
        'smoke': 'धुवाँ',
        'fog': 'हुस्सु',
    }
    return translations.get(desc.lower(), desc) 



def get_farming_tip(description):
    tip_map = {
        'clear sky': 'खेतीका लागि राम्रो समय।',
        'few clouds': 'खेतीका लागि उपयुक्त।',
        'scattered clouds': 'पानी पर्ने सम्भावना कम।',
        'overcast clouds': 'कृषि काम गर्न सकिने।',
        'light rain': 'सिचाइ रोक्नुहोस्। हल्का वर्षा भइरहेको छ।',
        'moderate rain': 'सिचाइ नगरौं, वर्षा भइरहेको छ।',
        'heavy intensity rain': 'भारी वर्षा! सिचाइ नगर्नुहोस्।',
        'rain': 'सावधानी अपनाउनुहोस्। पानी परिरहेको छ।',
        'thunderstorm': 'काम रोकिने सम्भावना। सतर्क रहनुहोस्।',
        'snow': 'चिसो धेरै! कृषिका लागि उपयुक्त होइन।',
        'mist': 'कम दृश्यता। काम गर्दा ध्यान दिनुहोस्।',
        'haze': 'हावा प्रदूषित हुन सक्छ। मास्क लगाउनुहोस्।',
    }
    return tip_map.get(description.lower(), "सामान्य अवस्था। कृषिकर्म गर्न सकिने।")



def get_weather_for_district(district_obj):
    district_en = district_obj["en"]
    district_np = district_obj["np"]

    url = f"https://api.openweathermap.org/data/2.5/weather?q={district_en},NP&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()

        description_en = data['weather'][0]['description']
        description_np = translate_weather_desc(description_en)
        tip = get_farming_tip(description_en)

        return {
            'district': district_np,
            'temperature': data['main']['temp'],
            'description': description_en,
            'description_np': description_np,
            'humidity': data['main']['humidity'],
            'wind': data['wind']['speed'],
            'icon': data['weather'][0]['icon'],
            'farming_tip': tip
        }
    except Exception:
        return {
            'district': district_np,
            'error': 'माफ गर्नुहोस्, मौसम जानकारी उपलब्ध छैन।'
        }

def weather_dashboard(request):
    selected_district = request.GET.get('district', '')

    # Get list of district names for dropdown
    district_names = [(d["en"], d["np"]) for d in DISTRICTS]

    if selected_district:
        district_obj = next((d for d in DISTRICTS if d["en"] == selected_district), None)
        if not district_obj:
            return HttpResponseBadRequest("Invalid district.")
        weather_data = [get_weather_for_district(district_obj)]
    else:
        weather_data = []

    return render(request, 'weather_dashboard.html', {
        'weather_data': weather_data,
        'district_names': district_names,
        'selected_district': selected_district,
    })

