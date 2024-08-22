from flask import Flask, request, jsonify
import os
import socket
import getpass
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Bepaal het pad naar het bureaublad
desktop_path = os.path.join(os.environ['USERPROFILE'], 'Desktop')
file_path = os.path.join(desktop_path, 'ip_addresses.txt')

# Verkrijg de naam van de computer en de gebruiker
computer_name = socket.gethostname()
user_name = getpass.getuser()

# Functie om het bestand te initialiseren
def initialize_file():
    try:
        with open(file_path, 'w') as file:
            file.write(f"Computernaam: {computer_name}\n")
            file.write(f"Gebruikersnaam: {user_name}\n")
            file.write("\nIP-adressen:\n")
    except Exception as e:
        logging.error(f"Fout bij het initialiseren van het bestand: {e}")

# Controleer of het bestand bestaat, anders initialiseer het
if not os.path.exists(file_path):
    initialize_file()

@app.route('/api/store_ip', methods=['POST'])
def store_ip():
    try:
        data = request.get_json()
        if data is None:
            logging.error("Geen JSON-gegevens ontvangen.")
            return jsonify({"message": "Geen JSON-gegevens ontvangen."}), 400
        
        ip = data.get('ip')
        if ip:
            with open(file_path, 'a') as file:
                file.write(f"{ip}\n")
            return jsonify({"message": "IP-adres opgeslagen!", "ip": ip}), 200
        logging.error("Geen IP-adres gevonden in de JSON-gegevens.")
        return jsonify({"message": "Geen IP-adres ontvangen."}), 400
    except Exception as e:
        logging.error(f"Fout bij het opslaan van IP-adres: {e}")
        return jsonify({"message": f"Fout bij het opslaan van IP-adres: {e}"}), 500

@app.route('/api/get_ips', methods=['GET'])
def get_ips():
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                ip_list = file.readlines()
            return jsonify([ip.strip() for ip in ip_list if ip.strip() and not ip.startswith("Computernaam:") and not ip.startswith("Gebruikersnaam:")]), 200
        return jsonify([]), 200
    except Exception as e:
        logging.error(f"Fout bij het ophalen van IP-adressen: {e}")
        return jsonify({"message": f"Fout bij het ophalen van IP-adressen: {e}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)  # Zet debug=True voor ontwikkelingsdoeleinden
