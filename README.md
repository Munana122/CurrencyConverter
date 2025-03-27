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
   git clone https://github.com/your-repo/currency-converter.git
   cd currency-converter
