#!/usr/bin/env python3
"""
Comprehensive report of all inserted data in the HR system
"""
import sqlite3

DB = "database.db"

def generate_comprehensive_report():
    """Generate a comprehensive report of all data"""
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    
    print("=" * 80)
    print("                    HR ONBOARDING SYSTEM - DATA REPORT")
    print("=" * 80)
    
    # 1. HR Dataset Overview
    hr_count = c.execute("SELECT COUNT(*) FROM hr_data").fetchone()[0]
    if hr_count > 0:
        print(f"\n1. HR DATASET (Historical Data)")
        print(f"   Total Records: {hr_count:,}")
        
        # Department breakdown
        dept_breakdown = c.execute("SELECT department, COUNT(*) FROM hr_data GROUP BY department ORDER BY COUNT(*) DESC").fetchall()
        print(f"   Departments:")
        for dept, count in dept_breakdown:
            print(f"     - {dept}: {count} employees")
        
        # Key statistics
        avg_age = c.execute("SELECT AVG(age) FROM hr_data").fetchone()[0]
        avg_income = c.execute("SELECT AVG(monthly_income) FROM hr_data").fetchone()[0]
        attrition_rate = c.execute("SELECT COUNT(*) * 100.0 / (SELECT COUNT(*) FROM hr_data) FROM hr_data WHERE attrition='Yes'").fetchone()[0]
        avg_satisfaction = c.execute("SELECT AVG(job_satisfaction) FROM hr_data").fetchone()[0]
        
        print(f"   Key Metrics:")
        print(f"     - Average Age: {avg_age:.1f} years")
        print(f"     - Average Income: ${avg_income:,.0f}/month")
        print(f"     - Attrition Rate: {attrition_rate:.1f}%")
        print(f"     - Average Job Satisfaction: {avg_satisfaction:.1f}/5")
    
    # 2. Active Employees
    employees = c.execute("SELECT id, name, department, position, start_date FROM employees ORDER BY department, name").fetchall()
    print(f"\n2. ACTIVE EMPLOYEES ({len(employees)} total)")
    
    # Group by department
    dept_employees = {}
    for emp in employees:
        dept = emp[2]
        if dept not in dept_employees:
            dept_employees[dept] = []
        dept_employees[dept].append(emp)
    
    for dept, emp_list in sorted(dept_employees.items()):
        print(f"\n   {dept.upper()} DEPARTMENT ({len(emp_list)} employees):")
        for emp_id, name, _, position, start_date in emp_list:
            print(f"     - {name} ({position}) - Started: {start_date or 'N/A'}")
    
    # 3. Tasks Summary
    print(f"\n3. TASKS OVERVIEW")
    total_tasks = c.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
    done_tasks = c.execute("SELECT COUNT(*) FROM tasks WHERE status='Done'").fetchone()[0]
    pending_tasks = c.execute("SELECT COUNT(*) FROM tasks WHERE status='Pending'").fetchone()[0]
    not_started_tasks = c.execute("SELECT COUNT(*) FROM tasks WHERE status='Not Started'").fetchone()[0]
    
    print(f"   Total Tasks: {total_tasks}")
    print(f"   - Completed: {done_tasks} ({done_tasks/total_tasks*100:.1f}%)")
    print(f"   - Pending: {pending_tasks} ({pending_tasks/total_tasks*100:.1f}%)")
    print(f"   - Not Started: {not_started_tasks} ({not_started_tasks/total_tasks*100:.1f}%)")
    
    # Top 5 employees with most tasks
    top_tasks = c.execute("""
        SELECT e.name, COUNT(t.id) as task_count, 
               SUM(CASE WHEN t.status='Done' THEN 1 ELSE 0 END) as completed
        FROM employees e 
        LEFT JOIN tasks t ON e.id = t.employee_id 
        GROUP BY e.id, e.name 
        HAVING task_count > 0
        ORDER BY task_count DESC 
        LIMIT 5
    """).fetchall()
    
    print(f"\n   Top Employees by Task Count:")
    for name, task_count, completed in top_tasks:
        completion_rate = completed/task_count*100 if task_count > 0 else 0
        print(f"     - {name}: {task_count} tasks ({completed} completed, {completion_rate:.1f}%)")
    
    # 4. Policies Summary
    print(f"\n4. POLICIES OVERVIEW")
    total_policies = c.execute("SELECT COUNT(*) FROM policies").fetchone()[0]
    ack_policies = c.execute("SELECT COUNT(*) FROM policies WHERE acknowledged=1").fetchone()[0]
    
    print(f"   Total Policy Assignments: {total_policies}")
    print(f"   - Acknowledged: {ack_policies} ({ack_policies/total_policies*100:.1f}%)")
    print(f"   - Pending: {total_policies - ack_policies} ({(total_policies-ack_policies)/total_policies*100:.1f}%)")
    
    # Policy types
    policy_types = c.execute("SELECT policy, COUNT(*) FROM policies GROUP BY policy").fetchall()
    print(f"   Policy Types:")
    for policy, count in policy_types:
        ack_count = c.execute("SELECT COUNT(*) FROM policies WHERE policy=? AND acknowledged=1", (policy,)).fetchone()[0]
        print(f"     - {policy}: {count} assignments ({ack_count} acknowledged)")
    
    # 5. Training Summary
    print(f"\n5. TRAINING OVERVIEW")
    total_training = c.execute("SELECT COUNT(*) FROM training").fetchone()[0]
    completed_training = c.execute("SELECT COUNT(*) FROM training WHERE status='Completed'").fetchone()[0]
    pending_training = c.execute("SELECT COUNT(*) FROM training WHERE status='Pending'").fetchone()[0]
    not_started_training = c.execute("SELECT COUNT(*) FROM training WHERE status='Not Started'").fetchone()[0]
    
    print(f"   Total Training Assignments: {total_training}")
    print(f"   - Completed: {completed_training} ({completed_training/total_training*100:.1f}%)")
    print(f"   - Pending: {pending_training} ({pending_training/total_training*100:.1f}%)")
    print(f"   - Not Started: {not_started_training} ({not_started_training/total_training*100:.1f}%)")
    
    # Training courses
    training_courses = c.execute("SELECT course, COUNT(*) FROM training GROUP BY course").fetchall()
    print(f"   Training Courses:")
    for course, count in training_courses:
        completed_count = c.execute("SELECT COUNT(*) FROM training WHERE course=? AND status='Completed'", (course,)).fetchone()[0]
        print(f"     - {course}: {count} assignments ({completed_count} completed)")
    
    # 6. Notifications Summary
    print(f"\n6. NOTIFICATIONS OVERVIEW")
    total_notifications = c.execute("SELECT COUNT(*) FROM notifications").fetchone()[0]
    read_notifications = c.execute("SELECT COUNT(*) FROM notifications WHERE is_read=1").fetchone()[0]
    unread_notifications = c.execute("SELECT COUNT(*) FROM notifications WHERE is_read=0").fetchone()[0]
    
    print(f"   Total Notifications: {total_notifications}")
    print(f"   - Read: {read_notifications} ({read_notifications/total_notifications*100:.1f}%)")
    print(f"   - Unread: {unread_notifications} ({unread_notifications/total_notifications*100:.1f}%)")
    
    # 7. Department Performance Summary
    print(f"\n7. DEPARTMENT PERFORMANCE")
    dept_performance = c.execute("""
        SELECT e.department,
               COUNT(DISTINCT e.id) as emp_count,
               COUNT(t.id) as total_tasks,
               SUM(CASE WHEN t.status='Done' THEN 1 ELSE 0 END) as completed_tasks,
               COUNT(p.id) as total_policies,
               SUM(CASE WHEN p.acknowledged=1 THEN 1 ELSE 0 END) as ack_policies,
               COUNT(tr.id) as total_training,
               SUM(CASE WHEN tr.status='Completed' THEN 1 ELSE 0 END) as completed_training
        FROM employees e
        LEFT JOIN tasks t ON e.id = t.employee_id
        LEFT JOIN policies p ON e.id = p.employee_id
        LEFT JOIN training tr ON e.id = tr.employee_id
        WHERE e.id > 1  -- Exclude the first employee with no data
        GROUP BY e.department
        ORDER BY emp_count DESC
    """).fetchall()
    
    for dept, emp_count, total_tasks, completed_tasks, total_policies, ack_policies, total_training, completed_training in dept_performance:
        task_completion = completed_tasks/total_tasks*100 if total_tasks > 0 else 0
        policy_completion = ack_policies/total_policies*100 if total_policies > 0 else 0
        training_completion = completed_training/total_training*100 if total_training > 0 else 0
        
        print(f"\n   {dept.upper()}:")
        print(f"     - Employees: {emp_count}")
        print(f"     - Task Completion: {task_completion:.1f}% ({completed_tasks}/{total_tasks})")
        print(f"     - Policy Acknowledgment: {policy_completion:.1f}% ({ack_policies}/{total_policies})")
        print(f"     - Training Completion: {training_completion:.1f}% ({completed_training}/{total_training})")
    
    print("\n" + "=" * 80)
    print("                           END OF REPORT")
    print("=" * 80)
    
    conn.close()

if __name__ == "__main__":
    generate_comprehensive_report()