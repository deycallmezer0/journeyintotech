from django.shortcuts import render, redirect, get_object_or_404
from .models import Address
from .forms import AddressForm
import requests
import logging
import os
API_KEY = os.getenv('GOOGLE_API_KEY')

logging.basicConfig(level=logging.DEBUG, filename='debug.log')

def get_distance_and_duration(origin, destination):
    url = f'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins={origin}&destinations={destination}&key={API_KEY}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data['status'] == 'OK':
            element = data['rows'][0]['elements'][0]
            if element['status'] == 'OK':
                distance = element['distance']['text']
                duration = element['duration']['text']
                return distance, duration
            else:
                logging.error(f"Error calculating distance for {destination}: {element['status']}")
                return None, None
        else:
            logging.error(f"Error with Distance Matrix API for {destination}: {data['status']}")
            return None, None
    except requests.exceptions.RequestException as e:
        logging.error(f"HTTP request failed: {e}")
        return None, None

def add_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_address')
    else:
        form = AddressForm()
    addresses = Address.objects.all()
    return render(request, 'distance_tool/add_address.html', {'form': form, 'addresses': addresses})

def edit_address(request, address_id):
    address = get_object_or_404(Address, pk=address_id)
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect('add_address')
    else:
        form = AddressForm(instance=address)
    return render(request, 'distance_tool/edit_address.html', {'form': form})

def delete_address(request, address_id):
    address = get_object_or_404(Address, pk=address_id)
    if request.method == 'POST':
        address.delete()
        return redirect('add_address')
    return render(request, 'distance_tool/delete_address.html', {'address': address})

def show_distances(request):
    context = {'distances': {}, 'given_address': ''}
    if request.method == 'POST':
        given_address = request.POST.get('given_address')
        saved_addresses = Address.objects.all()
        distances = {}
        for address in saved_addresses:
            distance, duration = get_distance_and_duration(given_address, address.address)
            if distance is not None and duration is not None:
                distances[address.name] = {'address': address.address, 'distance': distance, 'duration': duration}
            else:
                distances[address.name] = {'address': address.address, 'distance': 'Distance calculation failed', 'duration': 'Time calculation failed'}
        context = {'distances': distances, 'given_address': given_address}
    return render(request, 'distance_tool/show_distances.html', context)
