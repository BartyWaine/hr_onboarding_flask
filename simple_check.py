#!/usr/bin/env python3
"""
Script to check and display tasks, policies, and training data for all employees
"""
import sqlite3

DB = "database.db"

def check_employee_data():
    """Check tasks, policies, and training data for all employees"""
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    
    # Get all employees
    employees = c.execute("SELECT id, name, department, position FROM employees ORDER BY name").fetchall()
    print(f"=== EMPLOYEE DATA SUMMARY ===")
    print(f"Total Active Employees: {len(employees)}")
    print()
    
    for emp_id, name, dept, position in employees:
        print(f"EMPLOYEE: {name} (ID: {emp_id})")
        print(f"   Department: {dept} | Position: {position}")
        
        # Check tasks
        tasks = c.execute("SELECT id, task, status FROM tasks WHERE employee_id = ?", (emp_id,)).fetchall()
        print(f"   TASKS ({len(tasks)}):")
        if tasks:
            for task_id, task, status in tasks:
                status_icon = "[DONE]" if status == "Done" else "[PENDING]" if status == "Pending" else "[TODO]"
                print(f"      {status_icon} {task}")
        else:
            print(f"      No tasks assigned")
        
        # Check policies
        policies = c.execute("SELECT id, policy, acknowledged FROM policies WHERE employee_id = ?", (emp_id,)).fetchall()
        print(f"   POLICIES ({len(policies)}):")
        if policies:
            for policy_id, policy, ack in policies:
                ack_status = "[ACKNOWLEDGED]" if ack == 1 else "[PENDING]"
                print(f"      {ack_status} {policy}")
        else:
            print(f"      No policies assigned")
        
        # Check training
        training = c.execute("SELECT id, course, status, due_date FROM training WHERE employee_id = ?", (emp_id,)).fetchall()
        print(f"   TRAINING ({len(training)}):")
        if training:
            for train_id, course, status, due_date in training:
                status_label = f"[{status.upper()}]"
                print(f"      {status_label} {course} - Due: {due_date}")
        else:
            print(f"      No training assigned")
        
        # Check notifications
        notifications = c.execute("SELECT id, message, created_at, is_read FROM notifications WHERE employee_id = ?", (emp_id,)).fetchall()
        print(f"   NOTIFICATIONS ({len(notifications)}):")
        if notifications:
            for notif_id, message, created, is_read in notifications:
                read_status = "[READ]" if is_read == 1 else "[UNREAD]"
                print(f"      {read_status} {message[:50]}... ({created})")
        else:
            print(f"      No notifications")
        
        print("-" * 70)
    
    # Summary statistics
    print(f"=== SUMMARY STATISTICS ===")
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
    
    # Show department breakdown
    print(f"\n=== DEPARTMENT BREAKDOWN ===")
    dept_stats = c.execute("""
        SELECT department, COUNT(*) as emp_count,
               AVG(CASE WHEN t.status='Done' THEN 1.0 ELSE 0.0 END) * 100 as task_completion,
               AVG(CASE WHEN p.acknowledged=1 THEN 1.0 ELSE 0.0 END) * 100 as policy_ack
        FROM employees e
        LEFT JOIN tasks t ON e.id = t.employee_id
        LEFT JOIN policies p ON e.id = p.employee_id
        GROUP BY department
        ORDER BY emp_count DESC
    """).fetchall()
    
    for dept, emp_count, task_comp, policy_ack in dept_stats:
        print(f"{dept}: {emp_count} employees | Tasks: {task_comp:.1f}% | Policies: {policy_ack:.1f}%")
    
    conn.close()

if __name__ == "__main__":
    check_employee_data()