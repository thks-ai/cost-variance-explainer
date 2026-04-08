from app.database.crud import create_tables

if __name__ == "__main__":
    create_tables()
    print("SQLite tables created successfully.")
