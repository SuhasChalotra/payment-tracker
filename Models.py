from datetime import date


class TruckList:
    def __init__(self):
        self.truck_list = []

    def search_by_vin(self, input_vin):
        output_truck_list = []

        for truck in self.truck_list:
            if str(input_vin) in truck.vin_number:
                output_truck_list.append(truck)

        return output_truck_list

    def add_truck(self, vin=None, year=None, purchase_cost=None, prev_owner=None, description=None):
        self.truck_list.append(Truck(vin, year, purchase_cost, prev_owner, description))

    def add_sale_by_truck_vin(self, truck_vin, new_owner, sale_price, amount_paid):
        truck = self.search_by_vin(truck_vin)

        if len(truck) == 1:
            truck[0].add_sale(new_owner, sale_price, amount_paid)
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
    NEW_TRUCK = "New"
    IN_PROGRESS = "In progress"
    COMPLETED = "Completed"

    def __init__(self, vin, year, purchase_cost, prev_owner=None, description=None):
        """
        :param vin:
        :param year:
        :param purchase_cost:
        :param prev_owner:
        """
        self.vin_number = vin
        self.year = year
        self.purchase_cost = purchase_cost
        self.prev_owner = prev_owner
        self.description = description
        self.current_owner = ""
        self.sale_info = []
        self.status = self.NEW_TRUCK

    def add_sale(self, new_owner, sale_price):
        self.sale_info.append(BuyerInfo(new_owner, sale_price))
        self.refresh_truck_status()

    def add_payment_with_buyer(self, buyer, payment, input_date, description):
        for sale in self.sale_info:
            if sale.new_owner == buyer:
                sale.add_payment(input_date,
                                 payment,
                                 description)
                sale.refresh_values()

        self.refresh_truck_status()

    def delete_payment(self, payment):
        for buyer in self.sale_info:
            if payment in buyer.payments:
                buyer.payments.remove(payment)

    def refresh_truck_status(self):
        if not self.sale_info:
            self.status = self.NEW_TRUCK
        else:
            buyer = self.sale_info[-1]
            self.current_owner = str(buyer.new_owner)
            buyer.refresh_values()

            if buyer.amount_remaining <= 0:
                self.status = self.COMPLETED
            else:
                self.status = self.IN_PROGRESS


class BuyerInfo:
    def __init__(self, new_owner, sale_price):
        self.new_owner = new_owner
        self.sale_price = float(sale_price)
        self.amount_paid = 0
        self.amount_remaining = self.sale_price - self.amount_paid
        self.payments = []

    def add_payment(self, input_date, payment_amount, description):
        self.payments.append(Payment(input_date, payment_amount, self.new_owner, description))
        self.amount_paid += float(payment_amount)

    def get_amount_paid(self):
        return self.amount_paid

    def calculate_amount_paid(self):
        self.amount_paid = 0
        for payment in self.payments:
            self.amount_paid += payment.payment_amount

    def refresh_values(self):
        self.calculate_amount_paid()
        self.amount_remaining = self.sale_price - self.amount_paid


class Payment:
    def __init__(self, input_date, payment_amount, buyer, description=""):
        print(input_date)
        self.date = date(input_date.GetYear(), input_date.GetMonth() + 1, input_date.GetDay())
        self.payment_amount = float(payment_amount)
        self.buyer = buyer
        self.description = description

    def __str__(self):
        return "Payment of ${} made on {}".format(str(self.payment_amount), self.date.strftime("%B %d, %Y"))
