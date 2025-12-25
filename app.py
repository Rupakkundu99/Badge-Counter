"""
Badge Counter Web Application
Flask backend API for counting Google Cloud Skills Boost badges from public profile URLs.
"""

from flask import Flask, render_template, request, jsonify
from badge_counter import count_badges_from_url
import re

app = Flask(__name__)


@app.route('/')
def index():
    """Serve the main frontend page."""
    return render_template('index.html')


@app.route('/count-badges', methods=['POST'])
def count_badges():
    """
    API endpoint to count badges from a profile URL.
    
    Expected JSON payload:
        {
            "profile_url": "https://www.cloudskillsboost.google/public_profiles/..."
        }
        
    Returns:
        JSON response with badge count or error message
    """
    try:
        data = request.get_json()
        profile_url = data.get('profile_url', '').strip()
        
        # Validate URL
        if not profile_url:
            return jsonify({
                'success': False,
                'error': 'Please provide a profile URL'
            }), 400
            
        if not profile_url.startswith('http'):
            return jsonify({
                'success': False,
                'error': 'Invalid URL format. URL must start with http:// or https://'
            }), 400
            
        # Check if it's a Google Cloud Skills Boost URL
        if 'cloudskillsboost.google' not in profile_url:
            return jsonify({
                'success': False,
                'error': 'URL must be a Google Cloud Skills Boost public profile URL'
            }), 400
        
        # Count badges
        badge_count = count_badges_from_url(profile_url)
        
        return jsonify({
            'success': True,
            'badge_count': badge_count,
            'profile_url': profile_url
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'An error occurred: {str(e)}'
        }), 500


if __name__ == '__main__':
    print("🚀 Starting Badge Counter Web Application...")
    print("📊 Open your browser and navigate to: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
