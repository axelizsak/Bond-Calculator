from datetime import datetime, timedelta
import numpy as np

class BondCalculator:    
    def __init__(self, principal, coupon_rate, ytm, maturity_date):
        self.principal = float(principal)
        self.coupon_rate = float(coupon_rate) / 100
        self.ytm = float(ytm) / 100
        
        self.maturity_date = datetime.strptime(maturity_date, '%Y-%m-%d')
        self.today_date = datetime.today()
        
        self._find_next_coupon_date()
        self._calculate_time_periods()
    
    def _find_next_coupon_date(self):
        temp_date = self.maturity_date
        while temp_date > self.today_date:
            self.coupon_date = temp_date
            temp_date = temp_date - timedelta(days=365)
        
        if self.coupon_date <= self.today_date:
            self.coupon_date = self.coupon_date + timedelta(days=365)
    
    def _calculate_time_periods(self):
        self.years_to_maturity = (self.maturity_date - self.today_date).days / 365
        self.years_since_last_coupon = (365 - (self.coupon_date - self.today_date).days) / 365
        self.periods = int(np.ceil(self.years_to_maturity))
        
        base_period = (self.coupon_date - self.today_date).days / 365
        self.time_periods = [base_period + i for i in range(self.periods)]
    
    def _generate_cash_flows(self):
        cash_flows = [self.principal * self.coupon_rate] * (self.periods - 1)
        cash_flows.append(self.principal * (1 + self.coupon_rate))
        return cash_flows
    
    def calculate_price(self):
        cash_flows = self._generate_cash_flows()
        present_values = [
            cf / (1 + self.ytm) ** t 
            for cf, t in zip(cash_flows, self.time_periods)
        ]
        
        dirty_price = sum(present_values)
        accrued_interest = (self.years_since_last_coupon * 
                          self.principal * 
                          self.coupon_rate)
        clean_price = dirty_price - accrued_interest
        
        return clean_price, dirty_price
    
    def calculate_modified_duration(self):
        cash_flows = self._generate_cash_flows()
        present_values = [
            cf / (1 + self.ytm) ** t 
            for cf, t in zip(cash_flows, self.time_periods)
        ]
        
        weighted_pvs = [pv * t for pv, t in zip(present_values, self.time_periods)]
        macaulay = sum(weighted_pvs) / sum(present_values)
        modified_duration = macaulay / (1 + self.ytm)
        
        return modified_duration
    
    def calculate_convexity(self):
        cash_flows = self._generate_cash_flows()
        _, dirty_price = self.calculate_price()
        
        convexity_components = [
            (cf * t * (t + 1)) / ((1 + self.ytm) ** t)
            for cf, t in zip(cash_flows, self.time_periods)
        ]
        
        convexity = sum(convexity_components) / (dirty_price * (1 + self.ytm) ** 2)
        return convexity
    
    def calculate_elasticity(self):
        modified_duration = self.calculate_modified_duration()
        return abs(modified_duration * (1 + self.ytm))

    def get_all_metrics(self):
        clean_price, dirty_price = self.calculate_price()
        modified_duration = self.calculate_modified_duration()
        convexity = self.calculate_convexity()
        elasticity = self.calculate_elasticity()
        
        return {
            'clean_price': clean_price,
            'dirty_price': dirty_price,
            'modified_duration': modified_duration,
            'convexity': convexity,
            'elasticity': elasticity
        }

if __name__ == "__main__":
    calculator = BondCalculator(
        principal=float(input("Enter principal: ")),
        coupon_rate=float(input("Enter coupon rate (%): ")),
        ytm=float(input("Enter YTM (%): ")),
        maturity_date=input("Enter maturity date (YYYY-MM-DD): ")
    )
    
    metrics = calculator.get_all_metrics()
    
    print(f"Clean Price: {metrics['clean_price']:.2f}")
    print(f"Dirty Price: {metrics['dirty_price']:.2f}")
    print(f"Modified Duration: {metrics['modified_duration']:.2f}")
    print(f"Convexity: {metrics['convexity']:.4f}")
    print(f"Elasticity: {metrics['elasticity']:.2f}")