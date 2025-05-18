# calendar_app/views.py
from django.shortcuts import render
from datetime import date, timedelta
from calendar import monthrange, month_name

CROP_GUIDE = {
    'टमाटर': {
        'sowing_time': 'फागुन - चैत',
        'harvesting_days': 90,
        'watering_interval': 5,
        'fertilizing_interval': 15,
        'seed_date': date(2025, 2, 1)
    },
    'बन्दा': {
        'sowing_time': 'माघ - फागुन',
        'harvesting_days': 75,
        'watering_interval': 4,
        'fertilizing_interval': 12,
        'seed_date': date(2025, 1, 20)
    },
    'भण्टा': {
        'sowing_time': 'चैत - वैशाख',
        'harvesting_days': 85,
        'watering_interval': 6,
        'fertilizing_interval': 18,
        'seed_date': date(2025, 3, 15)
    }
}

def get_calendar_month(seed_date, month_offset, watering_interval, fertilizing_interval, harvesting_day):
    month_date = seed_date.replace(day=1) + timedelta(days=30 * month_offset)
    year, month = month_date.year, month_date.month
    first_weekday, num_days = monthrange(year, month)

    calendar = []
    week = [''] * first_weekday
    for day in range(1, num_days + 1):
        current_date = date(year, month, day)
        diff = (current_date - seed_date).days
        emoji = ''
        if diff == 0:
            emoji = '🌱'
        elif diff > 0:
            if diff % watering_interval == 0:
                emoji += '💧'
            if diff % fertilizing_interval == 0:
                emoji += '🧪'
            if diff == harvesting_day:
                emoji += '🌾'
        week.append(f'{day}<br>{emoji}')
        if len(week) == 7:
            calendar.append(week)
            week = []
    if week:
        week += [''] * (7 - len(week))
        calendar.append(week)
    return {
        'year': year,
        'month': month,
        'month_name': month_name[month],
        'weeks': calendar
    }

def crop_calendar_view(request):
    crop_name = request.GET.get('crop')
    calendars = []

    context = {
        'crops': list(CROP_GUIDE.keys()),
        'selected_crop': crop_name
    }

    if crop_name and crop_name in CROP_GUIDE:
        guide = CROP_GUIDE[crop_name]
        seed_date = guide['seed_date']

        context.update({
            'sowing_time': guide['sowing_time'],
            'harvesting_days': guide['harvesting_days'],
            'watering_interval': guide['watering_interval'],
            'fertilizing_interval': guide['fertilizing_interval']
        })

        for i in range(3):  # Next 3 months
            calendars.append(get_calendar_month(
                seed_date, i,
                guide['watering_interval'],
                guide['fertilizing_interval'],
                guide['harvesting_days']
            ))

    context['calendars'] = calendars
    return render(request, 'calendar_app/calendar.html', context)
