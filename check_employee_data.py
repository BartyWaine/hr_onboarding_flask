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
    print(f"Total Active Employees: {len(employees)}\n")
    
    for emp_id, name, dept, position in employees:
        print(f"👤 {name} (ID: {emp_id})")
        print(f"   Department: {dept} | Position: {position}")
        
        # Check tasks
        tasks = c.execute("SELECT id, task, status FROM tasks WHERE employee_id = ?", (emp_id,)).fetchall()
        print(f"   📋 Tasks ({len(tasks)}):")
        if tasks:
            for task_id, task, status in tasks:
                status_icon = "✅" if status == "Done" else "⏳" if status == "Pending" else "❌"
                print(f"      {status_icon} {task} ({status})")
        else:
            print(f"      No tasks assigned")
        
        # Check policies
        policies = c.execute("SELECT id, policy, acknowledged FROM policies WHERE employee_id = ?", (emp_id,)).fetchall()
        print(f"   📄 Policies ({len(policies)}):")
        if policies:
            for policy_id, policy, ack in policies:
                ack_icon = "✅" if ack == 1 else "⏳"
                print(f"      {ack_icon} {policy} ({'Acknowledged' if ack == 1 else 'Pending'})")
        else:
            print(f"      No policies assigned")
        
        # Check training
        training = c.execute("SELECT id, course, status, due_date FROM training WHERE employee_id = ?", (emp_id,)).fetchall()
        print(f"   🎓 Training ({len(training)}):")
        if training:
            for train_id, course, status, due_date in training:
                status_icon = "✅" if status == "Completed" else "⏳" if status == "Pending" else "❌"
                print(f"      {status_icon} {course} ({status}) - Due: {due_date}")
        else:
            print(f"      No training assigned")
        
        # Check notifications
        notifications = c.execute("SELECT id, message, created_at, is_read FROM notifications WHERE employee_id = ?", (emp_id,)).fetchall()
        print(f"   🔔 Notifications ({len(notifications)}):")
        if notifications:
            for notif_id, message, created, is_read in notifications:
                read_icon = "📖" if is_read == 1 else "📩"
                print(f"      {read_icon} {message[:50]}... ({created})")
        else:
            print(f"      No notifications")
        
        print("-" * 60)
    
    # Summary statistics
    print(f"\n=== SUMMARY STATISTICS ===")
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
    
    print(f"📋 Tasks: {total_tasks} total | {done_tasks} done | {pending_tasks} pending")
    print(f"📄 Policies: {total_policies} total | {ack_policies} acknowledged | {total_policies - ack_policies} pending")
    print(f"🎓 Training: {total_training} total | {completed_training} completed | {pending_training} pending")
    print(f"🔔 Notifications: {total_notifications} total | {unread_notifications} unread")
    
    conn.close()

if __name__ == "__main__":
    check_employee_data()