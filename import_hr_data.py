#!/usr/bin/env python3
"""
Standalone script to import HR_Dataset.csv into the database
"""
import sqlite3
import csv
import os

DB = "database.db"

def create_hr_table():
    """Create the HR data table"""
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    
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
    
    conn.commit()
    conn.close()
    print("HR data table created successfully")

def import_csv_data():
    """Import data from HR_Dataset.csv"""
    if not os.path.exists('HR_Dataset.csv'):
        print("Error: HR_Dataset.csv not found in current directory")
        return
    
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    
    # Clear existing data
    c.execute("DELETE FROM hr_data")
    
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
                    int(row['Employee_ID']), row['Department'], row['Gender'], int(row['Age']),
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
        print(f"Successfully imported {imported} HR records")
        
        # Show some stats
        total = c.execute("SELECT COUNT(*) FROM hr_data").fetchone()[0]
        departments = c.execute("SELECT DISTINCT department FROM hr_data").fetchall()
        attrition_yes = c.execute("SELECT COUNT(*) FROM hr_data WHERE attrition='Yes'").fetchone()[0]
        
        print(f"Total records: {total}")
        print(f"Departments: {', '.join([d[0] for d in departments])}")
        print(f"Attrition rate: {attrition_yes}/{total} ({attrition_yes/total*100:.1f}%)")
        
    except Exception as e:
        print(f"Error importing data: {str(e)}")
    finally:
        conn.close()

if __name__ == "__main__":
    print("HR Dataset Import Tool")
    print("=" * 30)
    
    create_hr_table()
    import_csv_data()
    
    print("\nImport completed!")