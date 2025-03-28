# Currency Converter Application

## Overview

This is a **Currency Converter** web application that allows users to convert between different currencies using real-time exchange rates. The application features a user-friendly interface with dropdowns for currency selection, an input field for amount entry, and dynamic results displayed without reloading the page.

The application is deployed on **two web servers** with a **load balancer** distributing incoming traffic for improved reliability and scalability.

## Features

- Fetches real-time exchange rates from the **ExchangeRate-API**.
- Supports multiple currencies with dropdown selection.
- Converts entered amounts dynamically without requiring page reloads.
- Deployed on **two servers** with a **load balancer** for traffic management.

## Technologies Used

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Flask (Python)
- **Database:** N/A (uses an external API for exchange rates)
- **Server Management:** Nginx, Gunicorn, Systemd
- **Deployment:** Ubuntu servers with a load balancer

---

## Running the Application Locally

1. **Clone the Repository:**
   ```sh
   git clone https://github.com/Munana122/CurrencyConverter.git
   cd currencyConverter
   ```

2. **Set Up Virtual Environment:**
   ```sh
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Create .env to store your API Key:**
   ```sh
   API_KEY="your_api_key_from Exchange-Rate API"
   FLASK_ENV=production
   ```

5. **Run the Application:**
   ```sh
   python3 app.py
   ```

6. **Access the App in Browser:**
   ```
   http://127.0.0.1:5000
   ```

---

## API Integration

This project uses the **ExchangeRate-API** to fetch real-time currency conversion rates.

- **API Used:** [ExchangeRate-API](https://www.exchangerate-api.com/)
- **Endpoint Example:**
  ```
  https://v6.exchangerate-api.com/v6/YOUR_API_KEY/latest/USD
  ```
- The backend fetches exchange rates and provides conversion results through a `/convert` endpoint.

---

## Deployment Steps

### **1. Setting Up Web Servers**
The application is deployed on **two web servers** (Web01 & Web02) and managed using a **load balancer**.

- **SSH into each server:**
  ```sh
  ssh ubuntu@54.166.191.144
  ```

- **Clone the repository:**
  ```sh
  git clone https://github.com/Munana122/CurrencyConverter.git
  cd currencyConverter
  ```

- **Set up the virtual environment:**
  ```sh
  python3 -m venv venv
  source venv/bin/activate
  ```

- **Install dependencies:**
  ```sh
  pip install -r requirements.txt
  ```

### **2. Configuring Gunicorn & Systemd**
- Create a **Gunicorn service** file:
  ```sh
  sudo nano /etc/systemd/system/myapp.service
  ```
- Add the following:
  ```ini
  [Unit]
  Description=Gunicorn instance to serve myapp
  After=network.target

  [Service]
  User=ubuntu
  Group=ubuntu
  WorkingDirectory=/home/ubuntu/currencyConverter
  Environment="PATH=/home/ubuntu/currencyConverter/venv/bin"
  ExecStart=/home/ubuntu/currencyConverter/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:5000 app:app

  [Install]
  WantedBy=multi-user.target
  ```

- **Restart Gunicorn service:**
  ```sh
  sudo systemctl daemon-reload
  sudo systemctl start myapp
  sudo systemctl enable myapp
  ```

### **3. Configuring Nginx**
- Create an **Nginx configuration file**:
  ```sh
  sudo nano /etc/nginx/sites-available/myapp
  ```
- Add:
  ```nginx
  upstream app_servers {
    server 10.227.78.219:5000;
    server 10.227.17.67:5000;
  }
  server {
      listen 80;

      location / {
          proxy_pass http://app_servers;
          proxy_set_header Host $host;
          proxy_set_header X-Real-IP $remote_addr;
          proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      }
  }
  ```

- **Enable site and restart Nginx:**
  ```sh
  sudo ln -s /etc/nginx/sites-available/myapp /etc/nginx/sites-enabled
  sudo systemctl restart nginx
  ```

### **4. Setting Up the Load Balancer**
- SSH into the **load balancer server**:
  ```sh
  ssh ubuntu@35.175.148.205
  ```

- Configure **Nginx load balancer**:
  ```sh
  sudo nano /etc/nginx/sites-available/loadbalancer
  ```
- Add:
  ```nginx
  upstream backend_servers {
      server 10.227.78.219:5000;
      server 10.227.17.67:5000;
  }

  server {
      listen 80;

      location / {
          proxy_pass http://backend_servers;
          proxy_set_header Host $host;
          proxy_set_header X-Real-IP $remote_addr;
          proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      }
  }
  ```

- **Enable site and restart Nginx:**
  ```sh
  sudo ln -s /etc/nginx/sites-available/loadbalancer /etc/nginx/sites-enabled
  sudo systemctl restart nginx
  ```

### **5. Testing Deployment**
- Access the application via:
  ```
  http://35.175.148.205
  ```

- Check load balancing:
  ```sh
  curl http://35.175.148.205
  ```

---

## Challenges & Solutions

- **Issue:** Nginx failed to start due to an incorrect upstream host in load balancer.
  - **Solution:** Fixed the configuration by using correct Web01 and Web02 IPs.

- **Issue:** CORS errors when calling the API from frontend.
  - **Solution:** Added CORS headers to the Flask app.

- **Issue:** Gunicorn service failed due to a missing working directory.
  - **Solution:** Ensured the correct project path in the systemd file.

---

## Credits & Acknowledgements

- **ExchangeRate-API** for real-time currency exchange rates.
- **Flask** for backend API.
- **Gunicorn & Nginx** for server deployment.
- **Ubuntu Servers** for hosting the application.

---

## Future Improvements

- Implement user authentication.
- Add support for historical exchange rates.
- Improve UI with additional animations.

---

## Author

- **MUNANA Merveille**
- **GitHub:** [munana122](https://github.com/munana122)
