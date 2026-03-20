#!/usr/bin/env python3
"""
Script to check table structure and add employees correctly
"""
import sqlite3
from datetime import date

DB = "database.db"

def check_table_structure():
    """Check the structure of employees table"""
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    
    # Get table structure
    structure = c.execute("PRAGMA table_info(employees)").fetchall()
    print("Employees table structure:")
    for col in structure:
        print(f"  {col[1]} ({col[2]})")
    
    # Check existing employees
    existing = c.execute("SELECT * FROM employees").fetchall()
    print(f"\nExisting employees: {len(existing)}")
    for emp in existing:
        print(f"  - ID: {emp[0]}, Name: {emp[1]}, Dept: {emp[2]}, Position: {emp[3]}")
    
    # Add more sample employees (using correct column names)
    additional_employees = [
        ("John Smith", "IT", "Software Engineer"),
        ("Sarah Johnson", "HR", "HR Manager"),
        ("Mike Chen", "Finance", "Financial Analyst"),
        ("Emily Davis", "Marketing", "Marketing Specialist"),
        ("David Wilson", "Sales", "Sales Representative"),
        ("Lisa Brown", "IT", "DevOps Engineer"),
        ("James Miller", "Finance", "Accountant"),
        ("Anna Garcia", "HR", "Recruiter"),
        ("Robert Taylor", "Marketing", "Content Manager"),
        ("Jennifer Lee", "Sales", "Account Manager"),
        ("Alex Rodriguez", "IT", "Data Scientist"),
        ("Maria Gonzalez", "Marketing", "Digital Marketing Manager"),
        ("Kevin Wang", "Finance", "Budget Analyst"),
        ("Rachel Green", "HR", "Training Coordinator"),
        ("Tom Anderson", "Sales", "Regional Sales Manager")
    ]
    
    # Insert additional employees
    added = 0
    for name, dept, position in additional_employees:
        # Check if employee already exists
        exists = c.execute("SELECT COUNT(*) FROM employees WHERE name = ?", (name,)).fetchone()[0]
        if exists == 0:
            c.execute("INSERT INTO employees(name, department, position) VALUES(?, ?, ?)",
                     (name, dept, position))
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
    check_table_structure()