from payments.models import Plan
import json
import os

def payment_seeder():
    with open(os.getcwd() + '/payments/files/plans.json', 'r') as f:
        data = json.load(f)
    
    monthly_plans = data["monthly"]
    for p in monthly_plans:
        plan = Plan(
            name = monthly_plans[p]["name"],
            price = monthly_plans[p]["price"]
        )
        plan.save()
