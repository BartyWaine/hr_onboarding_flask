from flask import Flask, render_template, request, redirect, session, flash
import sqlite3
import csv
import os
from datetime import date
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'devkey-change-in-production')
DB = os.getenv('DATABASE_URL', 'database.db')

# Remove sqlite:/// prefix if present
if DB.startswith('sqlite:///'):
    DB = DB[10:]

def get_db():
    return sqlite3.connect(DB)

def init_db():
    conn = get_db()
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username TEXT, password TEXT, role TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS employees(id INTEGER PRIMARY KEY, name TEXT, department TEXT, position TEXT, start_date TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS tasks(id INTEGER PRIMARY KEY, employee_id INTEGER, task TEXT, status TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS policies(id INTEGER PRIMARY KEY, employee_id INTEGER, policy TEXT, acknowledged INTEGER DEFAULT 0)")
    c.execute("CREATE TABLE IF NOT EXISTS training(id INTEGER PRIMARY KEY, employee_id INTEGER, course TEXT, status TEXT, due_date TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS notifications(id INTEGER PRIMARY KEY, employee_id INTEGER, message TEXT, created_at TEXT, is_read INTEGER DEFAULT 0)")
    c.execute("CREATE TABLE IF NOT EXISTS kpi(id INTEGER PRIMARY KEY, employee_id INTEGER, metric TEXT, value REAL, recorded_at TEXT)")
    # HR Dataset table
    c.execute("""CREATE TABLE IF NOT EXISTS hr_data(
        employee_id INTEGER PRIMARY KEY,
        department TEXT,
        gender TEXT,
        age INTEGER,
        education_level TEXT,
        job_role TEXT,
        monthly_income INTEGER,
        years_at_company INTEGER,
        years_in_current_role INTEGER,
        job_satisfaction INTEGER,
        performance_rating INTEGER,
        work_life_balance INTEGER,
        training_hours_last_year INTEGER,
        last_promotion_years_ago INTEGER,
        distance_from_home INTEGER,
        overtime TEXT,
        attrition TEXT,
        marital_status TEXT,
        number_of_companies_worked INTEGER,
        stock_option_level INTEGER
    )""")
    
    # Add start_date column to employees table if it doesn't exist
    try:
        c.execute("ALTER TABLE employees ADD COLUMN start_date TEXT")
    except:
        pass  # Column already exists
    
    conn.commit()
    conn.close()

def import_hr_data():
    """Import data from HR_Dataset.csv into hr_data table"""
    conn = get_db()
    c = conn.cursor()
    
    # Check if data already exists
    count = c.execute("SELECT COUNT(*) FROM hr_data").fetchone()[0]
    if count > 0:
        conn.close()
        return f"HR data already imported ({count} records)"
    
    try:
        with open('HR_Dataset.csv', 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            imported = 0
            for row in csv_reader:
                c.execute("""INSERT INTO hr_data (
                    employee_id, department, gender, age, education_level, job_role,
                    monthly_income, years_at_company, years_in_current_role, job_satisfaction,
                    performance_rating, work_life_balance, training_hours_last_year,
                    last_promotion_years_ago, distance_from_home, overtime, attrition,
                    marital_status, number_of_companies_worked, stock_option_level
                ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", (
                    row['Employee_ID'], row['Department'], row['Gender'], int(row['Age']),
                    row['Education_Level'], row['Job_Role'], int(row['Monthly_Income']),
                    int(row['Years_At_Company']), int(row['Years_In_Current_Role']),
                    int(row['Job_Satisfaction']), int(row['Performance_Rating']),
                    int(row['Work_Life_Balance']), int(row['Training_Hours_Last_Year']),
                    int(row['Last_Promotion_Years_Ago']), int(row['Distance_From_Home']),
                    row['Overtime'], row['Attrition'], row['Marital_Status'],
                    int(row['Number_Of_Companies_Worked']), int(row['Stock_Option_Level'])
                ))
                imported += 1
        
        conn.commit()
        conn.close()
        return f"Successfully imported {imported} HR records"
    except Exception as e:
        conn.close()
        return f"Error importing HR data: {str(e)}"

def login_required(f):
    from functools import wraps
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user" not in session:
            return redirect("/")
        return f(*args, **kwargs)
    return wrapper

# ── Auth ──────────────────────────────────────────────────────────────────────

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u, p = request.form["username"], request.form["password"]
        conn = get_db()
        row = conn.execute("SELECT role FROM users WHERE username=? AND password=?", (u, p)).fetchone()
        conn.close()
        if row:
            session["user"], session["role"] = u, row[0]
            return redirect("/dashboard")
        flash("Invalid credentials")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ── Dashboard ─────────────────────────────────────────────────────────────────

@app.route("/dashboard")
@login_required
def dashboard():
    conn = get_db()
    employees = conn.execute("SELECT * FROM employees").fetchall()
    total = len(employees)
    done_tasks = conn.execute("SELECT COUNT(*) FROM tasks WHERE status='Done'").fetchone()[0]
    pending_tasks = conn.execute("SELECT COUNT(*) FROM tasks WHERE status='Pending'").fetchone()[0]
    unread = conn.execute("SELECT COUNT(*) FROM notifications WHERE is_read=0").fetchone()[0]
    
    # HR Dataset statistics
    hr_total = conn.execute("SELECT COUNT(*) FROM hr_data").fetchone()[0]
    hr_attrition = conn.execute("SELECT COUNT(*) FROM hr_data WHERE attrition='Yes'").fetchone()[0] if hr_total > 0 else 0
    hr_departments = conn.execute("SELECT department, COUNT(*) FROM hr_data GROUP BY department").fetchall() if hr_total > 0 else []
    hr_avg_satisfaction = conn.execute("SELECT AVG(job_satisfaction) FROM hr_data").fetchone()[0] if hr_total > 0 else 0
    
    conn.close()
    return render_template("dashboard.html", 
                         employees=employees, total=total,
                         done_tasks=done_tasks, pending_tasks=pending_tasks, unread=unread,
                         hr_total=hr_total, hr_attrition=hr_attrition, 
                         hr_departments=hr_departments, hr_avg_satisfaction=hr_avg_satisfaction)

# ── New Employee ──────────────────────────────────────────────────────────────

@app.route("/new_employee", methods=["GET", "POST"])
@login_required
def new_employee():
    if request.method == "POST":
        name = request.form["name"]
        dept = request.form["department"]
        pos  = request.form["position"]
        sd   = request.form["start_date"]
        conn = get_db()
        c = conn.cursor()
        c.execute("INSERT INTO employees(name,department,position,start_date) VALUES(?,?,?,?)", (name, dept, pos, sd))
        eid = c.lastrowid
        # seed default policy & training
        for policy in ["Code of Conduct", "Data Privacy Policy", "IT Security Policy"]:
            c.execute("INSERT INTO policies(employee_id,policy) VALUES(?,?)", (eid, policy))
        for course in [("Orientation", "Pending"), ("Safety Training", "Pending"), ("Role-Specific Training", "Not Started")]:
            c.execute("INSERT INTO training(employee_id,course,status,due_date) VALUES(?,?,?,?)",
                      (eid, course[0], course[1], str(date.today())))
        c.execute("INSERT INTO notifications(employee_id,message,created_at) VALUES(?,?,?)",
                  (eid, f"Welcome {name}! Please complete your onboarding checklist.", str(date.today())))
        conn.commit()
        conn.close()
        flash(f"Employee {name} added successfully.")
        return redirect("/dashboard")
    return render_template("new_employee.html")

# ── Employee detail / checklist ───────────────────────────────────────────────

@app.route("/employee/<int:eid>")
@login_required
def employee(eid):
    conn = get_db()
    emp   = conn.execute("SELECT * FROM employees WHERE id=?", (eid,)).fetchone()
    tasks = conn.execute("SELECT * FROM tasks WHERE employee_id=?", (eid,)).fetchall()
    conn.close()
    return render_template("employee.html", emp=emp, tasks=tasks)

@app.route("/add_task/<int:eid>", methods=["POST"])
@login_required
def add_task(eid):
    task = request.form["task"]
    conn = get_db()
    conn.execute("INSERT INTO tasks(employee_id,task,status) VALUES(?,?,?)", (eid, task, "Pending"))
    conn.commit()
    conn.close()
    return redirect(f"/checklist/{eid}")

@app.route("/complete/<int:tid>/<int:eid>")
@login_required
def complete(tid, eid):
    conn = get_db()
    conn.execute("UPDATE tasks SET status='Done' WHERE id=?", (tid,))
    conn.commit()
    conn.close()
    return redirect(f"/checklist/{eid}")

# ── Checklist ─────────────────────────────────────────────────────────────────

@app.route("/checklist/<int:eid>")
@login_required
def checklist(eid):
    conn = get_db()
    emp   = conn.execute("SELECT * FROM employees WHERE id=?", (eid,)).fetchone()
    tasks = conn.execute("SELECT * FROM tasks WHERE employee_id=?", (eid,)).fetchall()
    conn.close()
    done  = sum(1 for t in tasks if t[3] == "Done")
    pct   = int(done / len(tasks) * 100) if tasks else 0
    return render_template("checklist.html", emp=emp, tasks=tasks, pct=pct)

# ── Policy Acknowledgement ────────────────────────────────────────────────────

@app.route("/policy/<int:eid>")
@login_required
def policy(eid):
    conn = get_db()
    emp      = conn.execute("SELECT * FROM employees WHERE id=?", (eid,)).fetchone()
    policies = conn.execute("SELECT * FROM policies WHERE employee_id=?", (eid,)).fetchall()
    conn.close()
    return render_template("policy.html", emp=emp, policies=policies)

@app.route("/acknowledge/<int:pid>/<int:eid>")
@login_required
def acknowledge(pid, eid):
    conn = get_db()
    conn.execute("UPDATE policies SET acknowledged=1 WHERE id=?", (pid,))
    conn.commit()
    conn.close()
    return redirect(f"/policy/{eid}")

# ── Training ──────────────────────────────────────────────────────────────────

@app.route("/training/<int:eid>")
@login_required
def training(eid):
    conn = get_db()
    emp      = conn.execute("SELECT * FROM employees WHERE id=?", (eid,)).fetchone()
    courses  = conn.execute("SELECT * FROM training WHERE employee_id=?", (eid,)).fetchall()
    conn.close()
    return render_template("training.html", emp=emp, courses=courses)

@app.route("/training_update/<int:tid>/<int:eid>", methods=["POST"])
@login_required
def training_update(tid, eid):
    status = request.form["status"]
    conn = get_db()
    conn.execute("UPDATE training SET status=? WHERE id=?", (status, tid))
    conn.commit()
    conn.close()
    return redirect(f"/training/{eid}")

# ── Notifications ─────────────────────────────────────────────────────────────

@app.route("/notifications")
@login_required
def notifications():
    conn = get_db()
    rows = conn.execute(
        "SELECT n.id, e.name, n.message, n.created_at, n.is_read, n.employee_id "
        "FROM notifications n JOIN employees e ON n.employee_id=e.id ORDER BY n.id DESC"
    ).fetchall()
    conn.close()
    return render_template("notifications.html", notifications=rows)

@app.route("/notify/read/<int:nid>")
@login_required
def mark_read(nid):
    conn = get_db()
    conn.execute("UPDATE notifications SET is_read=1 WHERE id=?", (nid,))
    conn.commit()
    conn.close()
    return redirect("/notifications")

@app.route("/notify/send", methods=["POST"])
@login_required
def send_notification():
    eid = request.form["employee_id"]
    msg = request.form["message"]
    conn = get_db()
    conn.execute("INSERT INTO notifications(employee_id,message,created_at) VALUES(?,?,?)", (eid, msg, str(date.today())))
    conn.commit()
    conn.close()
    flash("Notification sent.")
    return redirect("/notifications")

# ── KPI Dashboard ─────────────────────────────────────────────────────────────

@app.route("/kpi")
@login_required
def kpi():
    conn = get_db()
    employees = conn.execute("SELECT id, name FROM employees").fetchall()
    rows      = conn.execute(
        "SELECT k.id, e.name, k.metric, k.value, k.recorded_at, k.employee_id "
        "FROM kpi k JOIN employees e ON k.employee_id=e.id ORDER BY k.id DESC"
    ).fetchall()
    # summary per employee: tasks done %
    summary = []
    for emp in employees:
        total = conn.execute("SELECT COUNT(*) FROM tasks WHERE employee_id=?", (emp[0],)).fetchone()[0]
        done  = conn.execute("SELECT COUNT(*) FROM tasks WHERE employee_id=? AND status='Done'", (emp[0],)).fetchone()[0]
        ack   = conn.execute("SELECT COUNT(*) FROM policies WHERE employee_id=? AND acknowledged=1", (emp[0],)).fetchone()[0]
        pol   = conn.execute("SELECT COUNT(*) FROM policies WHERE employee_id=?", (emp[0],)).fetchone()[0]
        tr_done = conn.execute("SELECT COUNT(*) FROM training WHERE employee_id=? AND status='Completed'", (emp[0],)).fetchone()[0]
        tr_tot  = conn.execute("SELECT COUNT(*) FROM training WHERE employee_id=?", (emp[0],)).fetchone()[0]
        summary.append({
            "name": emp[1], "id": emp[0],
            "task_pct": int(done/total*100) if total else 0,
            "policy_pct": int(ack/pol*100) if pol else 0,
            "training_pct": int(tr_done/tr_tot*100) if tr_tot else 0,
        })
    conn.close()
    return render_template("kpi.html", employees=employees, kpi_rows=rows, summary=summary)

@app.route("/kpi/add", methods=["POST"])
@login_required
def kpi_add():
    eid    = request.form["employee_id"]
    metric = request.form["metric"]
    value  = request.form["value"]
    conn = get_db()
    conn.execute("INSERT INTO kpi(employee_id,metric,value,recorded_at) VALUES(?,?,?,?)",
                 (eid, metric, value, str(date.today())))
    conn.commit()
    conn.close()
    return redirect("/kpi")

# ── HR Data Import ────────────────────────────────────────────────────────────

@app.route("/import_hr_data")
@login_required
def import_hr_data_route():
    result = import_hr_data()
    flash(result)
    return redirect("/dashboard")

@app.route("/hr_data")
@login_required
def hr_data():
    conn = get_db()
    # Get pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = 50
    offset = (page - 1) * per_page
    
    # Get filtered data
    dept_filter = request.args.get('department', '')
    where_clause = ""
    params = []
    
    if dept_filter:
        where_clause = "WHERE department = ?"
        params.append(dept_filter)
    
    # Get data with pagination
    query = f"SELECT * FROM hr_data {where_clause} ORDER BY employee_id LIMIT ? OFFSET ?"
    params.extend([per_page, offset])
    data = conn.execute(query, params).fetchall()
    
    # Get total count
    count_query = f"SELECT COUNT(*) FROM hr_data {where_clause}"
    count = conn.execute(count_query, params[:-2] if dept_filter else []).fetchone()[0]
    
    # Get departments for filter
    departments = conn.execute("SELECT DISTINCT department FROM hr_data ORDER BY department").fetchall()
    
    # Get active employees from main employees table
    active_employees = conn.execute("SELECT * FROM employees ORDER BY department, name").fetchall()
    
    # Get all unique positions from HR dataset
    positions = conn.execute("SELECT DISTINCT job_role FROM hr_data ORDER BY job_role").fetchall()
    
    # Get position distribution
    position_stats = conn.execute("""
        SELECT job_role, COUNT(*) as count, 
               AVG(monthly_income) as avg_income,
               AVG(job_satisfaction) as avg_satisfaction,
               SUM(CASE WHEN attrition='Yes' THEN 1 ELSE 0 END) as attrition_count
        FROM hr_data 
        GROUP BY job_role 
        ORDER BY count DESC
    """).fetchall()
    
    # Get statistics
    stats = {
        'total': conn.execute("SELECT COUNT(*) FROM hr_data").fetchone()[0],
        'attrition_rate': conn.execute("SELECT COUNT(*) * 100.0 / (SELECT COUNT(*) FROM hr_data) FROM hr_data WHERE attrition='Yes'").fetchone()[0] or 0,
        'avg_age': conn.execute("SELECT AVG(age) FROM hr_data").fetchone()[0] or 0,
        'avg_income': conn.execute("SELECT AVG(monthly_income) FROM hr_data").fetchone()[0] or 0,
        'avg_satisfaction': conn.execute("SELECT AVG(job_satisfaction) FROM hr_data").fetchone()[0] or 0,
        'avg_performance': conn.execute("SELECT AVG(performance_rating) FROM hr_data").fetchone()[0] or 0,
        'active_employees': len(active_employees)
    }
    
    conn.close()
    
    # Calculate pagination info
    total_pages = (count + per_page - 1) // per_page
    has_prev = page > 1
    has_next = page < total_pages
    
    return render_template("hr_data.html", 
                         data=data, count=count, stats=stats, departments=departments,
                         page=page, total_pages=total_pages, has_prev=has_prev, has_next=has_next,
                         dept_filter=dept_filter, active_employees=active_employees,
                         positions=positions, position_stats=position_stats)

# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    init_db()
    conn = sqlite3.connect(DB)
    
    # Get admin credentials from environment
    admin_user = os.getenv('ADMIN_USERNAME', 'admin')
    admin_pass = os.getenv('ADMIN_PASSWORD', 'admin123')
    
    conn.execute("INSERT OR IGNORE INTO users(id,username,password,role) VALUES(1,?,?,?)", 
                 (admin_user, admin_pass, 'admin'))
    conn.commit()
    conn.close()
    
    # Import HR data on startup if not exists
    print("Checking HR dataset...")
    result = import_hr_data()
    print(result)
    
    # Get port from environment
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    
    app.run(host='0.0.0.0', port=port, debug=debug)
