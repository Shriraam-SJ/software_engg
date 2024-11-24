from pymongo import MongoClient
from datetime import datetime
import urllib.parse
# MongoDB connection setup
username = "shriraamsj21"
password = "Sharan@123"
encoded_password = urllib.parse.quote_plus(password)

uri = f"mongodb+srv://{username}:{encoded_password}@cluster21.jhxmf.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
db = client.get_database('banking_system')
users_collection = db['users']

# Functions for various operations:

def add_user(user_id, username, password, mpin):
    """Function to add a new user to the database."""
    user_data = {
        'user_id': user_id,
        'username': username,
        'password': password,
        'mpin': mpin,
        'balance': 0,
        'transaction_history': []
    }
    users_collection.insert_one(user_data)

def authenticate_user(username, password):
    """Authenticate the user based on username and password."""
    user = users_collection.find_one({'username': username, 'password': password})
    return user

def update_balance(user_id, amount, transaction_type):
    """
    Update the user's balance in the database.

    Parameters:
        user_id (str): The ID of the user.
        amount (float): The transaction amount.
        transaction_type (str): Type of transaction ('debit' or 'credit').

    Returns:
        tuple: (success: bool, message: str)
    """
    # Fetch the user from the database
    user = users_collection.find_one({"user_id": user_id})
    if not user:
        return False, "User not found."

    current_balance = user.get('balance', 0)

    # Handle debit transaction
    if transaction_type == 'debit':
        if amount > current_balance:
            return False, "Insufficient balance for debit transaction."
        new_balance = current_balance - amount

    # Handle credit transaction
    elif transaction_type == 'credit':
        new_balance = current_balance + amount

    else:
        return False, "Invalid transaction type."

    # Update the user's balance and record the transaction
    users_collection.update_one(
        {"user_id": user_id},
        {
            "$set": {"balance": new_balance},
            "$push": {
                "transaction_history": {
                    "type": transaction_type,
                    "amount": amount,
                    "date": datetime.now()
                }
            }
        }
    )

    return True, f"{transaction_type.capitalize()} successful. New balance: {new_balance:.2f}"


def record_transaction(user_id, transaction_type, amount):
    """Record the transaction history."""
    user = users_collection.find_one({'user_id': user_id})
    transaction_data = {
        'type': transaction_type,
        'amount': amount,
        'date': datetime.now()
    }
    users_collection.update_one(
        {'user_id': user_id},
        {'$push': {'transaction_history': transaction_data}}
    )

def get_balance(user_id):
    """Get the current balance of a user."""
    user = users_collection.find_one({'user_id': user_id})
    return user['balance'] if user else None

def get_transaction_history(user_id):
    """Get the transaction history of a user."""
    user = users_collection.find_one({'user_id': user_id})
    return user['transaction_history'] if user else []

def change_password(user_id, old_password, new_password):
    """Change the user's password."""
    user = users_collection.find_one({'user_id': user_id, 'password': old_password})
    
    if user:
        users_collection.update_one(
            {'user_id': user_id},
            {'$set': {'password': new_password}}
        )
        return "Password changed successfully"
    else:
        return "Old password is incorrect"

def change_mpin(user_id, old_mpin, new_mpin):
    """Change the user's MPIN."""
    user = users_collection.find_one({'user_id': user_id, 'mpin': old_mpin})
    
    if user:
        users_collection.update_one(
            {'user_id': user_id},
            {'$set': {'mpin': new_mpin}}
        )
        return "MPIN changed successfully"
    else:
        return "Old MPIN is incorrect"
