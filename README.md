# ResourceGuard

Empowering efficiency and precision in manufacturing resource management.

## Project Overview
ResourceGuard is a comprehensive web application designed to streamline resource management within the manufacturing industry. This application focuses on managing raw materials, products, and human resources, addressing challenges such as inventory tracking, employee management, and production monitoring.

## Features
- **Employee Management**: Create profiles, track attendance, and calculate payroll.
- **Raw Material Management**: Track suppliers, inventory, and purchase orders for raw materials.
- **Product Management**: Manage product catalog, monitor production processes, and inventory levels.
- **Inventory Management**: Real-time tracking of stock levels and adjustments.
- **Dynamic Frontend**: A responsive and interactive user interface built with AJAX and jQuery.

## Tech Stack
- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript, jQuery, AJAX
- **Database**: MySQL
- **Version Control**: Git
- **Deployment**: ALX environment

## Project Structure

- **api/**: Contains the API endpoints for creating, updating, and retrieving data. This folder handles requests related to employees, products, and raw materials.
  
- **models/**: Defines the database models for ResourceGuard, including tables for employees, materials, products, and transactions.
  
- **tests/**: Contains test cases for validating the functionality of models and APIs.
  
- **web_dynamic/**: Houses dynamic scripts that enhance user interactivity, leveraging AJAX for seamless data retrieval and updates without page reloads.
  
- **web_flask/**: Includes Flask views for managing the interaction between the frontend and backend, such as rendering HTML templates and handling form submissions.
  
- **web_static/**: Contains static files, including CSS and JavaScript, which are essential for styling and front-end functionality.

## Getting Started

### Prerequisites
- Python 3.x
- Flask
- MySQL
- Git

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/solomonferede1/resource_gaurd.git
   ```
2. Navigate into the project directory:
   ```bash
   cd resource_gaurd
   ```
3. Set up the virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
4. Install required packages:
   ```bash
   pip3 install -r requirements.txt
   ```
5. Set up the MySQL database using `setup_mysql_rs.sql`.

### Running the Application
1. Start the Flask server:
   ```bash
   flask run
   ```
2. Open a web browser and go to `http://127.0.0.1:5000` to access ResourceGuard.

## Usage

1. **Add Employees**: Use the Employee Management section to add and manage employee profiles and payroll.
2. **Track Inventory**: Access Raw Material and Product Management to track inventory, and production processes.
3. **Monitor Production**: View production reports and manage stock levels.

## Contributing
Feel free to open issues or submit pull requests for improvements or bug fixes.
