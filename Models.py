from datetime import date, datetime

class TruckList:
    def __init__(self):
        self.truck_list = []

    def search_by_vin(self, input_vin):
        output_truck_list = []

        for truck in self.truck_list:
            if str(input_vin) in truck.vin_number:
                output_truck_list.append(truck)

        return output_truck_list

    def add_truck(self, vin=None, year=None, make=None, purchase_cost=None, prev_owner=None, description=None):
        self.truck_list.append(Truck(vin, year, make, purchase_cost, prev_owner, description))

    def add_sale_by_truck_vin(self, truck_vin, name, sale_price, amount_paid):
        truck = self.search_by_vin(truck_vin)

        if len(truck) == 1:
            truck[0].add_buyer(name, sale_price, amount_paid)
            return 1
        return -1

    def get_trucks(self):
        return self.truck_list

    def delete_truck(self, truck):
        self.truck_list.remove(truck)

    def refresh_trucks(self):
        for truck in self.truck_list:
            truck.refresh_truck_status()


class Truck:
    AVAILABLE = "available"
    RENTED = "rented"
    FINANCED = "finance"
    COMPLETED = "completed"
    LATE = "late"

    def __init__(self, vin, year, make, purchase_cost, prev_owner, description):
        """
        :param vin:
        :param year:
        :param purchase_cost:
        :param prev_owner:
        """
        self.vin_number = vin
        self.year = year
        self.make = make
        self.purchase_cost = purchase_cost
        self.prev_owner = prev_owner
        self.description = description
        self.current_buyer = None
        self.buyers = []
        self.status = self.AVAILABLE

    def add_buyer(self, name):
        self.buyers.append(Buyer(name))
        self.current_buyer = self.buyers[-1]

    def is_payment_due(self):
        if self.current_buyer:
            payment_date = self.current_buyer.next_payment_date
            last_payment = self.current_buyer.get_latest_payment_made()

            if last_payment:
                if last_payment < payment_date < date.today():
                    return True
        return False

    def refresh_truck_status(self):
        if self.current_buyer is None:
            self.status = self.AVAILABLE
        else:
            if self.current_buyer.sale_type == self.RENTED:
                self.status = self.RENTED
                if self.current_buyer.is_late():
                    self.status = self.LATE
            if self.current_buyer.sale_type == self.FINANCED:
                if self.current_buyer.amount_remaining <= 0:
                    self.status = self.COMPLETED
                else:
                    self.status = self.FINANCED

                if self.current_buyer.is_late():
                    self.status = self.LATE


    def buyback(self):
        self.current_buyer = None
        
    def choose_buyer(self, buyer_str):
        for buyer in self.buyers:
            if buyer_str == buyer.name:
                self.current_buyer = buyer
                return

    def delete_buyer(self, buyer):
        self.buyers.remove(buyer)


class Buyer:
    def __init__(self, name):
        self.name = str(name)
        self.sale_type = None

        self.monthly_payment = None

        # Total price calculated by adding sale_price, interest and tax then down_payment is deducted
        self.sale_price = None
        self.interest = None
        self.tax = None
        self.down_payment = None

        self.amount_paid = None
        self.amount_remaining = None

        self.payment_list = []
        self.first_payment_date = None
        self.next_payment_date = None

    def get_total_price(self):
        if self.sale_type == Truck.RENTED:
            return None
        return self.sale_price + self.interest + self.tax

    def __str__(self):
        return self.name

    def rent_truck(self, monthly_payment, first_payment_date):
        print(first_payment_date)
        self.sale_type = Truck.RENTED
        self.monthly_payment = monthly_payment
        self.first_payment_date = first_payment_date
        self.next_payment_date = self.move_date_one_month(self.first_payment_date)
        self.generate_payment_rent()

    def generate_payment_rent(self):
        if self.sale_type == Truck.RENTED:

            if len(self.payment_list) == 0:
                due_date = self.get_latest_payment_made()

            else:
                due_date = self.move_date_one_month(self.get_latest_payment_made())

            print(due_date, self.payment_list)
            self.payment_list.append(Payment(due_date=due_date,
                                             description="",
                                             balance=self.monthly_payment,
                                             payment_amount=self.monthly_payment,
                                             payment_date=due_date))

    def finance_truck(self, sale_price, interest, tax, down_payment, term_length, first_payment_date):
        self.sale_type = Truck.FINANCED
        
        self.sale_price = sale_price
        self.interest = interest
        self.tax = tax
        self.down_payment = down_payment
        
        self.amount_paid = self.down_payment
        self.amount_remaining = (self.sale_price + self.interest + self.tax) - self.down_payment
        self.first_payment_date = first_payment_date
        self.next_payment_date = self.move_date_one_month(self.first_payment_date)
        self.generate_payments_finance(term_length)

    def generate_payments_finance(self, term_length):
        if self.sale_type == Truck.FINANCED:
            daily_payment = self.amount_remaining / term_length
            curr_date = self.first_payment_date
            balance = self.amount_remaining
            for index in range(term_length):
                self.payment_list.append(Payment(due_date=curr_date,
                                                 description="",
                                                 balance=balance,
                                                 payment_amount=daily_payment,
                                                 payment_date=curr_date))

                curr_date = self.move_date_one_month(curr_date)
                balance -= daily_payment



    @staticmethod
    def move_date_one_month(input_date):
        if isinstance(input_date, date):
            month = input_date.month
            if month == 12:
                return date(input_date.year + 1, 1, input_date.day)
            else:
                return date(input_date.year, input_date.month + 1, input_date.day)
        return input_date

    def get_latest_payment_made(self):
        latest_payment = self.first_payment_date
        
        if self.payment_list:
            for payment in self.payment_list:
                if payment.is_confirmed:
                    latest_payment = payment.payment_date
                else:
                    break

        return latest_payment

    def is_late(self):


        if self.payment_list:
            for payment in self.payment_list:
                if not payment.is_confirmed:

                    if payment.is_due():
                        return True
                    else:
                        return False
        return False


    def refresh_values(self):
        self.calculate_amount_paid()
        self.next_payment_date = self.move_date_one_month(self.get_latest_payment_made())

    def calculate_amount_paid(self):
        self.amount_paid = 0
        for payment in self.payment_list:
            if payment.is_confirmed:
                self.amount_paid += payment.payment_amount
            else:
                break

    def get_payments_made(self):
        total = len(self.payment_list)
        done = 0
        for payment in self.payment_list:
            if payment.is_confirmed:
                done += 1
        return "{} of {}".format(done, total)


class Payment:
    def __init__(self, due_date, description, balance, payment_amount, payment_date):
        
        self.due_date = due_date
        self.payment_date = payment_date
        
        self.payment_amount = float(payment_amount)
        self.balance_before = float(balance)
        self.new_balance = self.balance_before - self.payment_amount
        
        self.description = description
        self.is_confirmed = False
        
    def __str__(self):
        return "Payment of ${} made on {}".format(str(self.payment_amount), self.due_date.strftime("%B %d, %Y"))

    def is_late(self):
        if self.payment_date > self.due_date:

            return True
        return False

    def is_due(self):
        if not self.is_confirmed:
            if date.today() > self.due_date:
                return True

        return False


