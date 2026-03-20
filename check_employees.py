#!/usr/bin/env python3
"""
Script to check existing employees and add more samples
"""
import sqlite3
from datetime import date

DB = "database.db"

def check_and_add_employees():
    """Check existing employees and add more samples"""
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    
    # Check existing employees
    existing = c.execute("SELECT * FROM employees").fetchall()
    print(f"Existing employees: {len(existing)}")
    for emp in existing:
        print(f"  - {emp[1]} ({emp[2]}, {emp[3]})")
    
    # Add more sample employees
    additional_employees = [
        ("John Smith", "IT", "Software Engineer", "2024-01-15"),
        ("Sarah Johnson", "HR", "HR Manager", "2024-02-01"),
        ("Mike Chen", "Finance", "Financial Analyst", "2024-01-20"),
        ("Emily Davis", "Marketing", "Marketing Specialist", "2024-02-10"),
        ("David Wilson", "Sales", "Sales Representative", "2024-01-25"),
        ("Lisa Brown", "IT", "DevOps Engineer", "2024-02-05"),
        ("James Miller", "Finance", "Accountant", "2024-01-30"),
        ("Anna Garcia", "HR", "Recruiter", "2024-02-15"),
        ("Robert Taylor", "Marketing", "Content Manager", "2024-01-18"),
        ("Jennifer Lee", "Sales", "Account Manager", "2024-02-08"),
        ("Alex Rodriguez", "IT", "Data Scientist", "2024-02-12"),
        ("Maria Gonzalez", "Marketing", "Digital Marketing Manager", "2024-01-28"),
        ("Kevin Wang", "Finance", "Budget Analyst", "2024-02-03"),
        ("Rachel Green", "HR", "Training Coordinator", "2024-01-22"),
        ("Tom Anderson", "Sales", "Regional Sales Manager", "2024-02-07")
    ]
    
    # Insert additional employees
    added = 0
    for name, dept, position, start_date in additional_employees:
        # Check if employee already exists
        exists = c.execute("SELECT COUNT(*) FROM employees WHERE name = ?", (name,)).fetchone()[0]
        if exists == 0:
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
            added += 1
            print(f"Added: {name}")
    
    conn.commit()
    
    # Show final count
    final_count = c.execute("SELECT COUNT(*) FROM employees").fetchone()[0]
    print(f"\nTotal employees now: {final_count}")
    print(f"Added {added} new employees")
    
    conn.close()

if __name__ == "__main__":
    check_and_add_employees()