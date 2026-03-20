#!/usr/bin/env python3
"""
Script to add sample active employees to demonstrate the active employees list
"""
import sqlite3
from datetime import date, timedelta

DB = "database.db"

def add_sample_employees():
    """Add sample active employees"""
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    
    # Sample employees data
    sample_employees = [
        ("John Smith", "IT", "Software Engineer", "2024-01-15"),
        ("Sarah Johnson", "HR", "HR Manager", "2024-02-01"),
        ("Mike Chen", "Finance", "Financial Analyst", "2024-01-20"),
        ("Emily Davis", "Marketing", "Marketing Specialist", "2024-02-10"),
        ("David Wilson", "Sales", "Sales Representative", "2024-01-25"),
        ("Lisa Brown", "IT", "DevOps Engineer", "2024-02-05"),
        ("James Miller", "Finance", "Accountant", "2024-01-30"),
        ("Anna Garcia", "HR", "Recruiter", "2024-02-15"),
        ("Robert Taylor", "Marketing", "Content Manager", "2024-01-18"),
        ("Jennifer Lee", "Sales", "Account Manager", "2024-02-08")
    ]
    
    # Check if employees already exist
    existing = c.execute("SELECT COUNT(*) FROM employees").fetchone()[0]
    if existing > 0:
        print(f"Found {existing} existing employees. Skipping sample data insertion.")
        conn.close()
        return
    
    # Insert sample employees
    for name, dept, position, start_date in sample_employees:
        c.execute("INSERT INTO employees(name, department, position, start_date) VALUES(?, ?, ?, ?)",
                 (name, dept, position, start_date))
        eid = c.lastrowid
        
        # Add default policies
        for policy in ["Code of Conduct", "Data Privacy Policy", "IT Security Policy"]:
            c.execute("INSERT INTO policies(employee_id, policy) VALUES(?, ?)", (eid, policy))
        
        # Add default training
        for course in [("Orientation", "Pending"), ("Safety Training", "Pending"), ("Role-Specific Training", "Not Started")]:
            c.execute("INSERT INTO training(employee_id, course, status, due_date) VALUES(?, ?, ?, ?)",
                     (eid, course[0], course[1], str(date.today())))
        
        # Add welcome notification
        c.execute("INSERT INTO notifications(employee_id, message, created_at) VALUES(?, ?, ?)",
                 (eid, f"Welcome {name}! Please complete your onboarding checklist.", str(date.today())))
    
    conn.commit()
    conn.close()
    print(f"Successfully added {len(sample_employees)} sample employees")

if __name__ == "__main__":
    print("Adding sample active employees...")
    add_sample_employees()
    print("Done!")