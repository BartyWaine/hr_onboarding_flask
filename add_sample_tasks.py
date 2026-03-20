#!/usr/bin/env python3
"""
Script to add sample tasks for employees to demonstrate the complete onboarding workflow
"""
import sqlite3
import random

DB = "database.db"

def add_sample_tasks():
    """Add sample tasks for employees"""
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    
    # Get all employees (except the first one which has no policies/training)
    employees = c.execute("SELECT id, name, department, position FROM employees WHERE id > 1").fetchall()
    
    # Sample tasks by department
    department_tasks = {
        'IT': [
            'Set up development environment',
            'Complete security training',
            'Review code standards',
            'Set up VPN access',
            'Install required software',
            'Meet with team lead',
            'Review project documentation'
        ],
        'HR': [
            'Review employee handbook',
            'Complete HRIS training',
            'Set up employee files',
            'Review recruitment process',
            'Complete compliance training',
            'Meet with HR director',
            'Review benefits package'
        ],
        'Finance': [
            'Set up accounting software access',
            'Review financial procedures',
            'Complete expense reporting training',
            'Meet with finance manager',
            'Review budget processes',
            'Set up banking access',
            'Complete audit training'
        ],
        'Marketing': [
            'Review brand guidelines',
            'Set up marketing tools access',
            'Complete social media training',
            'Meet with marketing team',
            'Review campaign processes',
            'Set up analytics access',
            'Complete content training'
        ],
        'Sales': [
            'Set up CRM access',
            'Review sales process',
            'Complete product training',
            'Meet with sales manager',
            'Review territory assignment',
            'Set up customer database access',
            'Complete negotiation training'
        ]
    }
    
    # General tasks for all employees
    general_tasks = [
        'Complete office tour',
        'Set up workstation',
        'Meet with supervisor',
        'Review company policies',
        'Complete emergency procedures training',
        'Set up email and calendar',
        'Complete first week check-in'
    ]
    
    print("Adding sample tasks for employees...")
    
    for emp_id, name, dept, position in employees:
        # Add 3-5 general tasks
        num_general = random.randint(3, 5)
        selected_general = random.sample(general_tasks, num_general)
        
        # Add 2-4 department-specific tasks
        if dept in department_tasks:
            num_dept = random.randint(2, 4)
            selected_dept = random.sample(department_tasks[dept], min(num_dept, len(department_tasks[dept])))
        else:
            selected_dept = []
        
        all_tasks = selected_general + selected_dept
        
        # Insert tasks with random status
        for task in all_tasks:
            # 30% chance of being done, 50% pending, 20% not started
            rand = random.random()
            if rand < 0.3:
                status = 'Done'
            elif rand < 0.8:
                status = 'Pending'
            else:
                status = 'Not Started'
            
            c.execute("INSERT INTO tasks(employee_id, task, status) VALUES(?, ?, ?)",
                     (emp_id, task, status))
        
        print(f"Added {len(all_tasks)} tasks for {name}")
    
    # Randomly acknowledge some policies
    print("\nRandomly acknowledging some policies...")
    policies = c.execute("SELECT id, employee_id FROM policies").fetchall()
    for policy_id, emp_id in policies:
        # 40% chance of being acknowledged
        if random.random() < 0.4:
            c.execute("UPDATE policies SET acknowledged = 1 WHERE id = ?", (policy_id,))
    
    # Randomly complete some training
    print("Randomly completing some training...")
    training = c.execute("SELECT id, employee_id FROM training").fetchall()
    for train_id, emp_id in training:
        # 25% chance of being completed, 60% pending, 15% not started
        rand = random.random()
        if rand < 0.25:
            status = 'Completed'
        elif rand < 0.85:
            status = 'Pending'
        else:
            status = 'Not Started'
        
        c.execute("UPDATE training SET status = ? WHERE id = ?", (status, train_id))
    
    # Mark some notifications as read
    print("Marking some notifications as read...")
    notifications = c.execute("SELECT id FROM notifications").fetchall()
    for notif_id, in notifications:
        # 60% chance of being read
        if random.random() < 0.6:
            c.execute("UPDATE notifications SET is_read = 1 WHERE id = ?", (notif_id,))
    
    conn.commit()
    
    # Show updated statistics
    print("\n=== UPDATED STATISTICS ===")
    total_tasks = c.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
    done_tasks = c.execute("SELECT COUNT(*) FROM tasks WHERE status='Done'").fetchone()[0]
    pending_tasks = c.execute("SELECT COUNT(*) FROM tasks WHERE status='Pending'").fetchone()[0]
    
    total_policies = c.execute("SELECT COUNT(*) FROM policies").fetchone()[0]
    ack_policies = c.execute("SELECT COUNT(*) FROM policies WHERE acknowledged=1").fetchone()[0]
    
    total_training = c.execute("SELECT COUNT(*) FROM training").fetchone()[0]
    completed_training = c.execute("SELECT COUNT(*) FROM training WHERE status='Completed'").fetchone()[0]
    pending_training = c.execute("SELECT COUNT(*) FROM training WHERE status='Pending'").fetchone()[0]
    
    total_notifications = c.execute("SELECT COUNT(*) FROM notifications").fetchone()[0]
    unread_notifications = c.execute("SELECT COUNT(*) FROM notifications WHERE is_read=0").fetchone()[0]
    
    print(f"TASKS: {total_tasks} total | {done_tasks} done | {pending_tasks} pending")
    print(f"POLICIES: {total_policies} total | {ack_policies} acknowledged | {total_policies - ack_policies} pending")
    print(f"TRAINING: {total_training} total | {completed_training} completed | {pending_training} pending")
    print(f"NOTIFICATIONS: {total_notifications} total | {unread_notifications} unread")
    
    conn.close()

if __name__ == "__main__":
    add_sample_tasks()