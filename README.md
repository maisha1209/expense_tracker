<img width="1470" alt="Screenshot 2024-11-26 at 4 28 03 PM" src="https://github.com/user-attachments/assets/c76b1aeb-9fe9-42d7-b89c-5c9c4302abdc">Expense Tracker – Organize Your Finances More Intellectually

📖 Description
Expense Tracker is a web app built using Django to help graduate students and anyone who has been through the hustle of financial constraints. The goal of the application is to make expense tracking simple, budgeting easier, and goal-based saving achievable. All these will empower users toward financial stability, saving effectively, and working towards entrepreneurial ventures or personal financial goals.

🚀 Features
Expense Tracker: Fetch and show all transaction details and real-time account balances by integrating Plaid API.
Savings Goals: Set and track savings goals, such as saving $5,000 in 6 months, with automated progress updates.
Budget Insights: Identify spending patterns and suggest ways to reduce unnecessary expenses.
Account Integration: Link bank accounts securely to view detailed account summaries and transactions.
Intuitive UI: User-friendly interface, responsive design, developed with HTML, CSS, and JavaScript.
PostgreSQL Database: Reliable and safe storage for users' data, transactions, and saving goals.

🎯 Motivation
The Expense Tracker project was specifically designed for graduate students entering the workforce. Immediately after school, most graduates face financial constraints: low income coupled with increasing expenses. This tool will help them understand their spending habits and make informed financial decisions about saving for big goals, such as starting a business or tackling student loans. It's meant to empower users to take charge of their finances and improve financial literacy.

🛠️ Tech Stack
Frontend: HTML, CSS, JavaScript 
Backend: Python (Django framework)
Database: PostgreSQL
Integration: Plaid API for Real-Time Financial Data
Version Control: Git and GitHub for Collaborative Development

💾 Installation Instructions
Clone the repository:
git clone https://github.com/maisha1209/expense_tracker.git
cd expense_tracker



Set up a virtual environment:
python -m venv env
source env/bin/activate # For Mac/Linux
env\Scripts\activate # For Windows

Install dependencies:
pip install -r requirements.txt


Create a PostgreSQL database and update the DATABASES setting in settings.py.
Add your Plaid API credentials in the .env file:
Makefile
Copy code
PLAID_CLIENT_ID='672924b0d8987c001a775095'
PLAID_SECRET='0272d6d9647bbe839c1386c6b7abec'
PLAID_ENV=sandbox

Run database migrations:
python manage.py migrate

Start the development server:
python manage.py runserver

Open your web browser and go to:
http://127.0.0.1:8000/

 
 🌟 Usage
Sign up or log in: Create an account or log in to access your dashboard.
Link accounts: Tap the "Link Account" button to securely link your bank accounts.
View transactions: Track spending and group expenses by category.
Set savings goals: Identify savings goals and give updates on your progress regularly.
Track spending: From the information collected, pinpoint wasteful spending so as to save more.


📸 Screenshots

<img width="1470" alt="Screenshot 2024-11-26 at 4 26 26 PM" src="https://github.com/user-attachments/assets/e3f7a623-9a00-4b49-b761-06e3aa287119">

<img width="1470" alt="Screenshot 2024-11-26 at 4 26 30 PM" src="https://github.com/user-attachments/assets/49274a02-0302-4bad-bb2c-72fdd64dda06">
<img width="1470" alt="Screenshot 2024-11-26 at 4 26 44 PM" src="https://github.com/user-attachments/assets/cf79d971-7473-414a-92da-772d4ba07b4b">
<img width="1470" alt="Screenshot 2024-11-26 at 4 26 54 PM" src="https://github.com/user-attachments/assets/74694466-07b4-44d6-badb-01e5d617223e">
<img width="1470" alt="Screenshot 2024-11-26 at 4 27 54 PM" src="https://github.com/user-attachments/assets/8afc8799-8542-450b-acff-71a058fcd674">
![Uploading Screenshot 2024-11-<img width="1470" alt="Screenshot 2024-11-26 at 4 28 13 PM" src="https://github.com/user-attachments/assets/e0c3d56a-2f56-4c93-a8ea-4df340a0c7a1">
26 at 4.28.03 PM.png…]()
<img width="1470" alt="Screenshot 2024-11-26 at 4 28 18 PM" src="https://github.com/user-attachments/assets/07a09ad7-0400-4302-96a7-4e562f4733b7">

<img width="1470" alt="Screenshot 2024-11-26 at 4 28 13 PM" src="https://github.com/user-attachments/assets/5a8a3509-e093-4d42-9332-54e4f54c171c">
<img width="1470" alt="Screenshot 2024-11-26 at 4 28 18 PM" src="https://github.com/user-attachments/assets/6dcdc09a-a873-4feb-ae93-ae7f7adb63de">
<img width="1470" alt="Screenshot 2024-11-26 at 4 28 25 PM" src="https://github.com/user-attachments/assets/cf88518c-a828-4087-b177-58d49554fed3">
<img width="1470" alt="Screenshot 2024-11-26 at 4 28 39 PM" src="https://github.com/user-attachments/assets/c68a18ea-a685-4c92-8262-b858a9e254d3">
![Uploading Screenshot 2024-11-26 at 4.28.43 PM.png…]()
<img width="1470" alt="Screenshot 2024-11-26 at 4 28 49 PM" src="https://github.com/user-attachments/assets/e8ebb6bc-8b4b-4f70-8759-3066a4237bc6">

🤝 Contributing
Contributions are welcome! If you have any feature ideas, improvements, or bug fixes, feel free to:
Fork the repository Create a new feature branch (feature/new-feature) Open a pull request ??

✨ Acknowledgments Plaid API to enable real-time financial data integration. Django and PostgreSQL communities for their solid frameworks. Motivation from students and individuals looking for financial stability.
