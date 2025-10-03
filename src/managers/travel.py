"""
Travel Management System
"""
import json
import os
from datetime import datetime
from src.config.constants import DATA_FILES


class TravelManager:
    def __init__(self):
        self.trips = []
        self.bookings = []
        self.preferences = []
        self.travel_services = {
            'expedia': {
                'name': 'Expedia',
                'website': 'https://www.expedia.com',
                'api_available': True,
                'features': ['Flight Booking', 'Hotel Booking', 'Car Rental', 'Vacation Packages', 'Travel Insurance'],
                'rating': 4.1,
                'description': 'One-stop travel booking platform with comprehensive options',
                'mobile_app': True,
                'loyalty_program': 'Expedia Rewards',
                'customer_support': '24/7 Support'
            },
            'booking': {
                'name': 'Booking.com',
                'website': 'https://www.booking.com',
                'api_available': True,
                'features': ['Hotel Booking', 'Flight Booking', 'Car Rental', 'Airport Taxis', 'Restaurant Reservations'],
                'rating': 4.3,
                'description': 'Leading hotel booking platform with great deals and user reviews',
                'mobile_app': True,
                'loyalty_program': 'Genius',
                'customer_support': '24/7 Support'
            },
            'airbnb': {
                'name': 'Airbnb',
                'website': 'https://www.airbnb.com',
                'api_available': True,
                'features': ['Unique Stays', 'Experiences', 'Long-term Rentals', 'Host Services', 'Travel Insurance'],
                'rating': 4.2,
                'description': 'Unique accommodations and experiences from local hosts',
                'mobile_app': True,
                'loyalty_program': 'Airbnb Plus',
                'customer_support': '24/7 Support'
            },
            'kayak': {
                'name': 'Kayak',
                'website': 'https://www.kayak.com',
                'api_available': True,
                'features': ['Flight Search', 'Hotel Search', 'Car Rental', 'Price Alerts', 'Travel Guides'],
                'rating': 4.0,
                'description': 'Travel search engine with price comparison and booking options',
                'mobile_app': True,
                'loyalty_program': 'Kayak Rewards',
                'customer_support': 'Email Support'
            }
        }
        self.load_data()
    
    def load_data(self):
        """Load travel data from storage"""
        try:
            if os.path.exists('travel_data.json'):
                with open('travel_data.json', 'r') as f:
                    data = json.load(f)
                    self.trips = data.get('trips', [])
                    self.bookings = data.get('bookings', [])
                    self.preferences = data.get('preferences', [])
        except Exception as e:
            print(f"Error loading travel data: {e}")
    
    def save_data(self):
        """Save travel data to storage"""
        try:
            data = {
                'trips': self.trips,
                'bookings': self.bookings,
                'preferences': self.preferences
            }
            with open('travel_data.json', 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving travel data: {e}")
    
    def add_trip(self, destination, start_date, end_date, trip_type, budget):
        """Add a new travel trip"""
        trip = {
            'id': len(self.trips) + 1,
            'destination': destination,
            'start_date': start_date,
            'end_date': end_date,
            'type': trip_type,
            'budget': budget,
            'status': 'planned',
            'created_date': datetime.now().strftime('%Y-%m-%d')
        }
        self.trips.append(trip)
        self.save_data()
        return trip
    
    def get_trips(self):
        """Get all travel trips"""
        return self.trips
    
    def get_service_info(self, service_key):
        """Get travel service information"""
        return self.travel_services.get(service_key, {})
    
    def get_available_services(self):
        """Get list of available travel services"""
        return list(self.travel_services.keys())
