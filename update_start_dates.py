#!/usr/bin/env python3
"""
Script to update existing employees with start dates
"""
import sqlite3
from datetime import date, timedelta
import random

DB = "database.db"

def update_employee_start_dates():
    """Update existing employees with start dates"""
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    
    # Add start_date column if it doesn't exist
    try:
        c.execute("ALTER TABLE employees ADD COLUMN start_date TEXT")
        print("Added start_date column to employees table")
    except:
        print("start_date column already exists")
    
    # Get employees without start dates
    employees = c.execute("SELECT id, name FROM employees WHERE start_date IS NULL OR start_date = ''").fetchall()
    print(f"Found {len(employees)} employees without start dates")
    
    # Update with random start dates in the last 3 months
    base_date = date.today() - timedelta(days=90)
    
    for emp_id, name in employees:
        # Generate random start date within last 90 days
        random_days = random.randint(0, 90)
        start_date = base_date + timedelta(days=random_days)
        
        c.execute("UPDATE employees SET start_date = ? WHERE id = ?", (str(start_date), emp_id))
        print(f"Updated {name} with start date: {start_date}")
    
    conn.commit()
    
    # Show all employees with their start dates
    all_employees = c.execute("SELECT id, name, department, position, start_date FROM employees ORDER BY start_date DESC").fetchall()
    print(f"\nAll employees ({len(all_employees)}):")
    for emp in all_employees:
        print(f"  {emp[1]} - {emp[2]} ({emp[3]}) - Started: {emp[4]}")
    
    conn.close()

if __name__ == "__main__":
    update_employee_start_dates()