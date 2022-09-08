'''
Payroll Module for Project 5
'''
import os, os.path, shutil

PAY_LOGFILE = "paylog.txt"

class Employee:
    def __init__(self, emp_id, first_name, last_name, address, city, state, zipcode):
        self.emp_id = emp_id
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.classification = None
        
    def make_hourly(self, wage):
        self.classification = Hourly(wage)
    
    def make_salaried(self, salary):
        self.classification = Salaried(salary)
    
    def make_commissioned(self, salary, commission_rate):
        self.classification = Commissioned(salary, commission_rate)
        
    def issue_payment(self):
        pay = self.classification.issue_payment()
        if pay == None:
            pass
        else:
            pay = "{:.2f}".format(pay)
            paylog = open(PAY_LOGFILE, "a")
            paylog.write(f"Mailing {pay} to {self.first_name} {self.last_name} at {self.address} {self.city} {self.state} {self.zipcode}\n")
            paylog.close()
        
class Classification:
    def __init__(self):
        pass
    
    def issue_payment(self):
        pass
    
class Hourly(Classification):
    def __init__(self, wage):
        self.wage = float(wage)
        self.timecards = []
        
    def add_timecard(self, t_card):
        self.timecards.append(t_card)
        
    def issue_payment(self):
        pay = 0
        if len(self.timecards) > 0:
            for t_card in self.timecards:
                d_pay = float(t_card) * self.wage
                pay += d_pay
            self.timecards = []
            pay = round(pay, 2)
            return pay
        else:
            pass
    
class Salaried(Classification):
    def __init__(self, salary):
        self.salary = float(salary)
        
    def issue_payment(self):
        b_weekly = 1 / 24
        pay = self.salary * b_weekly
        pay = round(pay, 2)
        return pay
    
class Commissioned(Salaried):
    def __init__(self, salary, commission_rate):
        super().__init__(salary)
        self.commission_rate = float(commission_rate) / 100
        self.receipts = []
        
    def add_receipt(self, receipt):
        self.receipts.append(receipt)
        
    def issue_payment(self):
        b_weekly = 1 / 24
        ttl_commission = 0
        if len(self.receipts) > 0:
            for receipt in self.receipts:
                commission = float(receipt) * self.commission_rate
                ttl_commission += commission
        self.receipts = []
        salary = (self.salary * b_weekly)
        pay = salary + ttl_commission
        pay = round(pay, 2)
        return pay

global employees
employees = []

def load_employees():
    emp_list = open("employees.csv", "r")
    x = 0
    for line in emp_list:
        line = line.split(",")
        if x == 0:
            pass
        else:
            emp = Employee(line[0], line[1], line[2], line[3], line[4], line[5], line[6])
            
            if line[7] == "1":
                emp.make_salaried(line[8])
            
            elif line[7] == "2":
                emp.make_commissioned(line[8], line[9])
                
            elif line[7] == "3":
                emp.make_hourly(line[10])
                
            employees.append(emp)
        x += 1

def find_employee_by_id(id):
    for object in employees:
        if object.emp_id == id:
            return object
        else:
            pass

def process_timecards():
    tc_list = open("timecards.csv", "r")
    for line in tc_list:
        line = line.strip().split(",")
        emp = find_employee_by_id(line[0])
        clss = emp.classification
        for card in line[1:]:
            clss.add_timecard(float(card))

def process_receipts():
    r_list = open("receipts.csv", "r")
    for line in r_list:
        line = line.strip().split(",")
        emp = find_employee_by_id(line[0])
        clss = emp.classification
        for receipt in line[1:]:
            clss.add_receipt(float(receipt))

def run_payroll():
    if os.path.exists(PAY_LOGFILE): # pay_log_file is a global variable holding ‘payroll.txt’ 
        os.remove(PAY_LOGFILE) 
    for emp in employees:         # employees is the global list of Employee objects 
        emp.issue_payment()       # issue_payment calls a method in the classification 
                                  # object to compute the pay
                                  
load_employees()
process_timecards()
process_receipts()
run_payroll()




                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  