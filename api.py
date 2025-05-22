from flask import Flask, jsonify
from flask_cors import CORS
import fastf1
import pandas as pd
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Enable cache to speed up subsequent calls
if not os.path.exists('cache'):
    os.makedirs('cache')
fastf1.Cache.enable_cache('cache')

@app.route('/api/current-season', methods=['GET'])
def get_current_season():
    """Get current season information including schedule"""
    try:
        current_year = datetime.now().year
        schedule = fastf1.get_event_schedule(current_year)
        
        # Convert to dict for JSON serialization
        events = []
        for _, event in schedule.iterrows():
            event_date = event['EventDate']
            if isinstance(event_date, pd.Timestamp):
                event_date = event_date.strftime('%Y-%m-%d')
                
            events.append({
                'name': event['EventName'],
                'round': int(event['RoundNumber']),
                'date': event_date,
                'country': event['Country'],
                'location': event['Location'],
                'is_completed': datetime.strptime(event_date, '%Y-%m-%d').date() < datetime.now().date()
            })
        
        return jsonify({
            'year': current_year,
            'events': events
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/driver-standings', methods=['GET'])
def get_driver_standings():
    """Get current driver standings for the entire season"""
    try:
        # Hardcoded 2025 driver standings
        drivers = [
            {
                'position': 1,
                'driver_code': 'PIA',
                'driver_number': '81',
                'full_name': 'Oscar Piastri',
                'team': 'McLaren Mercedes',
                'points': 146
            },
            {
                'position': 2,
                'driver_code': 'NOR',
                'driver_number': '4',
                'full_name': 'Lando Norris',
                'team': 'McLaren Mercedes',
                'points': 133
            },
            {
                'position': 3,
                'driver_code': 'VER',
                'driver_number': '1',
                'full_name': 'Max Verstappen',
                'team': 'Red Bull Racing Honda RBPT',
                'points': 124
            },
            {
                'position': 4,
                'driver_code': 'RUS',
                'driver_number': '63',
                'full_name': 'George Russell',
                'team': 'Mercedes',
                'points': 99
            },
            {
                'position': 5,
                'driver_code': 'LEC',
                'driver_number': '16',
                'full_name': 'Charles Leclerc',
                'team': 'Ferrari',
                'points': 61
            },
            {
                'position': 6,
                'driver_code': 'HAM',
                'driver_number': '44',
                'full_name': 'Lewis Hamilton',
                'team': 'Ferrari',
                'points': 53
            },
            {
                'position': 7,
                'driver_code': 'ANT',
                'driver_number': '87',
                'full_name': 'Kimi Antonelli',
                'team': 'Mercedes',
                'points': 48
            },
            {
                'position': 8,
                'driver_code': 'ALB',
                'driver_number': '23',
                'full_name': 'Alexander Albon',
                'team': 'Williams Mercedes',
                'points': 40
            },
            {
                'position': 9,
                'driver_code': 'OCO',
                'driver_number': '31',
                'full_name': 'Esteban Ocon',
                'team': 'Haas Ferrari',
                'points': 14
            },
            {
                'position': 10,
                'driver_code': 'STR',
                'driver_number': '18',
                'full_name': 'Lance Stroll',
                'team': 'Aston Martin Aramco Mercedes',
                'points': 14
            },
            {
                'position': 11,
                'driver_code': 'SAI',
                'driver_number': '55',
                'full_name': 'Carlos Sainz',
                'team': 'Williams Mercedes',
                'points': 11
            },
            {
                'position': 12,
                'driver_code': 'TSU',
                'driver_number': '22',
                'full_name': 'Yuki Tsunoda',
                'team': 'Red Bull Racing Honda RBPT',
                'points': 10
            },
            {
                'position': 13,
                'driver_code': 'GAS',
                'driver_number': '10',
                'full_name': 'Pierre Gasly',
                'team': 'Alpine Renault',
                'points': 7
            },
            {
                'position': 14,
                'driver_code': 'HAD',
                'driver_number': '36',
                'full_name': 'Isack Hadjar',
                'team': 'Racing Bulls Honda RBPT',
                'points': 7
            },
            {
                'position': 15,
                'driver_code': 'HUL',
                'driver_number': '27',
                'full_name': 'Nico Hulkenberg',
                'team': 'Kick Sauber Ferrari',
                'points': 6
            },
            {
                'position': 16,
                'driver_code': 'BEA',
                'driver_number': '50',
                'full_name': 'Oliver Bearman',
                'team': 'Haas Ferrari',
                'points': 6
            },
            {
                'position': 17,
                'driver_code': 'ALO',
                'driver_number': '14',
                'full_name': 'Fernando Alonso',
                'team': 'Aston Martin Aramco Mercedes',
                'points': 0
            },
            {
                'position': 18,
                'driver_code': 'LAW',
                'driver_number': '40',
                'full_name': 'Liam Lawson',
                'team': 'Racing Bulls Honda RBPT',
                'points': 0
            },
            {
                'position': 19,
                'driver_code': 'DOO',
                'driver_number': '6',
                'full_name': 'Jack Doohan',
                'team': 'Alpine Renault',
                'points': 0
            },
            {
                'position': 20,
                'driver_code': 'BOR',
                'driver_number': '35',
                'full_name': 'Gabriel Bortoleto',
                'team': 'Kick Sauber Ferrari',
                'points': 0
            },
            {
                'position': 21,
                'driver_code': 'COL',
                'driver_number': '15',
                'full_name': 'Franco Colapinto',
                'team': 'Alpine Renault',
                'points': 0
            }
        ]
        
        return jsonify(drivers)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/constructor-standings', methods=['GET'])
def get_constructor_standings():
    """Get current constructor standings for the entire season"""
    try:
        # Use 2025 as the current year for our simulation
        current_year = 2025
        
        # Get all completed events for the season up to Imola (May 18, 2025)
        schedule = fastf1.get_event_schedule(current_year)
        reference_date = pd.Timestamp('2025-05-19')  # Day after Imola
        completed_events = schedule[schedule['EventDate'] < reference_date]
        
        if completed_events.empty:
            return jsonify({'error': 'No completed events found for current season'}), 404
        
        # Initialize team points dictionary
        team_points = {}
        
        # Loop through all completed events to accumulate points
        for _, event in completed_events.iterrows():
            try:
                # Only process actual races (not testing or sprint events)
                if event['EventFormat'] != 'testing':
                    event_name = event['EventName']
                    
                    # Load the race session
                    session = fastf1.get_session(current_year, event_name, 'R')
                    session.load(telemetry=False, weather=False)
                    
                    # Add points from this race to team totals
                    if hasattr(session, 'results') and session.results is not None:
                        for _, driver in session.results.iterrows():
                            team = driver['TeamName']
                            points = float(driver['Points']) if not pd.isna(driver['Points']) else 0
                            
                            if team in team_points:
                                team_points[team] += points
                            else:
                                team_points[team] = points
            except Exception as e:
                # Skip events that fail to load
                print(f"Could not load data for {event['EventName']}: {str(e)}")
                continue
        
        # Convert to list and sort by points
        constructors = [{'team': team, 'points': points} for team, points in team_points.items()]
        constructors.sort(key=lambda x: x['points'], reverse=True)
        
        # Add position
        for i, constructor in enumerate(constructors):
            constructor['position'] = i + 1
        
        return jsonify(constructors)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/next-race', methods=['GET'])
def get_next_race():
    """Get information about the next race"""
    try:
        # Hardcoded next race on May 25, 2025
        next_race = {
            'name': 'Monaco Grand Prix',
            'round': 8,
            'date': '2025-05-25',
            'country': 'Monaco',
            'location': 'Monte Carlo',
            'days_until': 6,  # 6 days from May 19 to May 25
            'time': '09:00:00',
            'timezone': 'EST'
        }
        
        return jsonify(next_race)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/last-race-podium', methods=['GET'])
def get_last_race_podium():
    """Get top 3 drivers from the last race"""
    try:
        # Create podium data for 2025 Imola race
        podium = [
            {
                'position': 1,
                'driver_code': 'VER',
                'driver_number': '1',
                'full_name': 'Max Verstappen',
                'team': 'Red Bull Racing Honda RBPT',
                'race_name': 'Emilia Romagna Grand Prix',
                'time': '1:31:33.199'
            },
            {
                'position': 2,
                'driver_code': 'NOR',
                'driver_number': '4',
                'full_name': 'Lando Norris',
                'team': 'McLaren Mercedes',
                'race_name': 'Emilia Romagna Grand Prix',
                'time': '+6.109s'
            },
            {
                'position': 3,
                'driver_code': 'PIA',
                'driver_number': '81',
                'full_name': 'Oscar Piastri',
                'team': 'McLaren Mercedes',
                'race_name': 'Emilia Romagna Grand Prix',
                'time': '+12.956s'
            }
        ]
        
        return jsonify({
            'race_name': 'Emilia Romagna Grand Prix',
            'race_date': '2025-05-18',
            'podium': podium
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)