from flask import Flask, jsonify, request
import os
import json

app = Flask(__name__)

# Path to the JSON file
json_file_path = 'tech_assess.json'


# Helper function to get the server load and disk space
def get_system_info():
    # Get the system's average load over 1, 5, and 15 minutes
    load1, load5, load15 = os.getloadavg()
    
    # Get the available disk space
    statvfs = os.statvfs('/')
    free_disk_space = statvfs.f_frsize * statvfs.f_bavail  # Available disk space in bytes
    
    return {
        'load_avg_1m': load1,
        'load_avg_5m': load5,
        'load_avg_15m': load15,
        'available_disk_space_bytes': free_disk_space
    }


# GET endpoint to return server load and available disk space
@app.route('/system-info', methods=['GET'])
def get_system_info_endpoint():
    system_info = get_system_info()
    return jsonify(system_info)


# GET endpoint to return the value of "return_value" from tech_assess.json
@app.route('/return-value', methods=['GET'])
def get_return_value():
    try:
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)
            return_value = data['tech']['return_value']
            return jsonify({'return_value': return_value})
    except FileNotFoundError:
        return jsonify({'error': 'JSON file not found'}), 404
    except KeyError:
        return jsonify({'error': 'Key "return_value" not found in JSON file'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# POST endpoint to overwrite the value of "return_value" in tech_assess.json
@app.route('/return-value', methods=['POST'])
def update_return_value():
    try:
        new_value = request.json.get('return_value')
        
        if new_value is None:
            return jsonify({'error': 'No value provided'}), 400
        
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)
        
        data['tech']['return_value'] = new_value
        
        with open(json_file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        
        return jsonify({'message': 'Value updated successfully', 'new_return_value': new_value})
    except FileNotFoundError:
        return jsonify({'error': 'JSON file not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
