Organize Your Finances More Intellectually

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
<img width="1470" alt="Screenshot 2024-11-26 at 4 28 49 PM" src="https://github.com/user-attachments/assets/13ca9223-04f4-4266-be04-b64245ab7944">
<img width="1470" alt="Screenshot 2024-11-26 at 4 28 43 PM" src="https://github.com/user-attachments/assets/dff4593f-0d12-4fd9-8f61-37cde508ecd7">
<img width="1470" alt="Screenshot 2024-11-26 at 4 28 39 PM" src="https://github.com/user-attachments/assets/88deee6f-debe-4d7e-acda-ea536ce30a41">
<img width="1470" alt="Screenshot 2024-11-26 at 4 28 25 PM" src="https://github.com/user-attachments/assets/851fbcbd-e958-46ac-b47f-360d5b15a3a7">
<img width="1470" alt="Screenshot 2024-11-26 at 4 28 18 PM" src="https://github.com/user-attachments/assets/a8bddcac-d3d0-4f1b-aa30-691a3a8ce96c">
<img width="1470" alt="Screenshot 2024-11-26 at 4 28 13 PM" src="https://github.com/user-attachments/assets/cb281b94-6552-45f0-8fcc-3bdb93dcaea3">
<img width="1470" alt="Screenshot 2024-11-26 at 4 28 03 PM" src="https://github.com/user-attachments/assets/29a72dde-561d-4e18-a2d7-9021a02b9f1f">
<img width="1470" alt="Screenshot 2024-11-26 at 4 27 54 PM" src="https://github.com/user-attachments/assets/7720b8c5-cd46-483d-bc73-19361a29e8ec">
<img width="1470" alt="Screenshot 2024-11-26 at 4 26 54 PM" src="https://github.com/user-attachments/assets/b67588d1-2f66-4fc8-bbe2-5c43e4af4a3f">






<img width="1470" alt="Screenshot 2024-11-26 at 4 26 30 PM" src="https://github.com/user-attachments/assets/9d06f7a6-fe48-459a-9e9a-27df9eb1f524">
<img width="1470" alt="Screenshot 2024-11-26 at 4 26 26 PM" src="https://github.com/user-attachments/assets/5345db3e-ef27-4cfd-9327-58ad56f8c624">

🤝 Contributing
Contributions are welcome! If you have ideas for features, improvements, or bug fixes, feel free to:
Fork the repository
Create a new branch (feature/new-feature)
Submit a pull request


✨ Acknowledgments Plaid API to enable real-time financial data integration. Django and PostgreSQL communities for their solid frameworks. Motivation from students and individuals looking for financial stability.
