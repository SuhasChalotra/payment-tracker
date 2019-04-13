import wx
from ObjectListView import ObjectListView as Olv, ColumnDefn
from Models import Truck
from Forms import NewTruckForm


class TruckListView(wx.Panel):
    """
    This will the first component in our app, displaying the truck inventory and a form to add new ones
    """
    def __init__(self, parent):

        wx.Panel.__init__(self, parent=parent)
        self.dataOlv = Olv(self, wx.ID_ANY, style=wx.LC_REPORT)

        done = wx.Bitmap("data/Checkmark.png", wx.BITMAP_TYPE_ANY)
        progress = wx.Bitmap("data/Progress.png", wx.BITMAP_TYPE_ANY)
        self.done = self.dataOlv.AddImages(wx.Icon(done))
        self.progress = self.dataOlv.AddImages(wx.Icon(progress))

        self.dataOlv.SetColumns([
            ColumnDefn("Buyer", "left", 180, "current_buyer",
                       imageGetter=self.image_getter),
            ColumnDefn("VIN", "right", 180, "vin_number"),
            ColumnDefn("Year", "right", 70, "year"),
            ColumnDefn("Make", "right", 70, "make"),
            ColumnDefn("Description", "right", 140, "description"),
            ColumnDefn("Previous Owner", "right", 140, "prev_owner"),
            ColumnDefn("Purchase Cost", "right", 140, "purchase_cost", stringConverter=numbers_with_commas)
        ])

        self.dataOlv.rowFormatter = truck_row_formatter

        self.dataOlv.cellEditMode = Olv.CELLEDIT_SINGLECLICK

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.dataOlv, 1, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(sizer)

    def set_trucks(self, truck_list):
        self.dataOlv.SetObjects(truck_list)

    def add_truck(self, truck):
        self.dataOlv.AddObject(truck)

    def get_selected(self):
        return self.dataOlv.GetSelectedObject()

    def image_getter(self, truck):
        if truck.status == Truck.COMPLETED:
            return self.done
        elif truck.status == Truck.RENTED or truck.status == Truck.FINANCED:
            return self.progress


def truck_row_formatter(list_item, truck):
    if truck.status == truck.COMPLETED:
        list_item.SetBackgroundColour(wx.Colour(197, 247, 213))
    elif truck.status == truck.RENTED or truck.status == truck.FINANCED:
        if truck.is_payment_due():
            list_item.SetBackgroundColour(wx.RED)
        else:
            list_item.SetBackgroundColour(wx.Colour(165, 224, 240))
    else:
        list_item.SetBackgroundColour(wx.WHITE)


class TruckDetailView(wx.Panel):
    """
    This will be second component where a selected truck's details are displayed along with buttons
    to sell/rent the truck and to make any other edits.
    """

    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)

        self.selected_truck = None

        selected_truck_buyer_label = wx.StaticText(self, wx.ID_ANY, "Buyer")
        self.selected_truck_buyer = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_READONLY)
        selected_truck_vin_label = wx.StaticText(self, wx.ID_ANY, "VIN")
        self.selected_truck_vin = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_READONLY)
        selected_truck_description_label = wx.StaticText(self, wx.ID_ANY, "Description")
        self.selected_truck_description = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_READONLY)

        selected_truck_sale_price_label = wx.StaticText(self, wx.ID_ANY, "Sale Price")
        self.selected_truck_sale_price = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_READONLY)
        selected_truck_tax_label = wx.StaticText(self, wx.ID_ANY, "Total Taxes")
        self.selected_truck_tax = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_READONLY)
        selected_truck_interest_label = wx.StaticText(self, wx.ID_ANY, "Interest")
        self.selected_truck_interest = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_READONLY)
        selected_truck_total_price_label = wx.StaticText(self, wx.ID_ANY, "Total Price")
        self.selected_truck_total_price = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_READONLY)

        selected_truck_down_payment_label = wx.StaticText(self, wx.ID_ANY, "Down Payment")
        self.selected_truck_down_payment = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_READONLY)
        selected_truck_amount_remaining_label = wx.StaticText(self, wx.ID_ANY, "Amount Remaining")
        self.selected_truck_amount_remaining = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_READONLY)
        selected_truck_payments_label = wx.StaticText(self, wx.ID_ANY, "Payments made")
        self.selected_truck_payments = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_READONLY)
        selected_truck_next_payment_label = wx.StaticText(self, wx.ID_ANY, "Next Payment")
        self.selected_truck_next_payment = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_READONLY)

        new_truck_btn = wx.Button(self, wx.ID_ANY, 'New Truck')
        rent_truck_btn = wx.Button(self, wx.ID_ANY, 'Rent Truck')
        finance_truck_btn = wx.Button(self, wx.ID_ANY, 'Finance Truck')
        new_truck_btn.SetBackgroundColour(wx.Colour(153, 255, 220))
        rent_truck_btn.SetBackgroundColour(wx.Colour(153, 255, 220))
        finance_truck_btn.SetBackgroundColour(wx.Colour(153, 255, 220))

        print_payments_btn = wx.Button(self, wx.ID_ANY, 'Print Payments')
        edit_buyer_btn = wx.Button(self, wx.ID_ANY, 'Edit Buyer')
        choose_buyer_btn = wx.Button(self, wx.ID_ANY, 'Choose Buyer')
        buyback_btn = wx.Button(self, wx.ID_ANY, 'Buyback')
        print_payments_btn.SetBackgroundColour(wx.Colour(180, 255, 153))
        edit_buyer_btn.SetBackgroundColour(wx.Colour(180, 255, 153))
        choose_buyer_btn.SetBackgroundColour(wx.Colour(180, 255, 153))
        buyback_btn.SetBackgroundColour(wx.Colour(180, 255, 153))

        delete_buyer_btn = wx.Button(self, wx.ID_ANY, 'Delete Buyer')
        delete_truck_btn = wx.Button(self, wx.ID_ANY, 'Delete Truck')
        delete_buyer_btn.SetBackgroundColour(wx.Colour(255, 153, 153))
        delete_truck_btn.SetBackgroundColour(wx.Colour(255, 153, 153))

        selected_truck_sizer = wx.BoxSizer(wx.VERTICAL)
        selected_truck_text_sizer_one = wx.BoxSizer(wx.HORIZONTAL)
        selected_truck_text_sizer_two = wx.BoxSizer(wx.HORIZONTAL)
        selected_truck_text_sizer_three = wx.BoxSizer(wx.HORIZONTAL)
        selected_truck_btn_sizer = wx.BoxSizer(wx.HORIZONTAL)

        selected_truck_text_sizer_one.Add(selected_truck_buyer_label, 0, wx.ALL | wx.EXPAND, 4)
        selected_truck_text_sizer_one.Add(self.selected_truck_buyer, 2, wx.ALL | wx.EXPAND, 4)
        selected_truck_text_sizer_one.Add(selected_truck_vin_label, 0, wx.ALL | wx.EXPAND, 4)
        selected_truck_text_sizer_one.Add(self.selected_truck_vin, 1, wx.ALL | wx.EXPAND, 4)
        selected_truck_text_sizer_one.Add(selected_truck_description_label, 0, wx.ALL | wx.EXPAND, 4)
        selected_truck_text_sizer_one.Add(self.selected_truck_description, 4, wx.ALL | wx.EXPAND, 4)

        selected_truck_text_sizer_two.Add(selected_truck_sale_price_label, 0, wx.ALL | wx.EXPAND, 4)
        selected_truck_text_sizer_two.Add(self.selected_truck_sale_price, 2, wx.ALL | wx.EXPAND, 4)
        selected_truck_text_sizer_two.Add(selected_truck_tax_label, 0, wx.ALL | wx.EXPAND, 4)
        selected_truck_text_sizer_two.Add(self.selected_truck_tax, 2, wx.ALL | wx.EXPAND, 4)
        selected_truck_text_sizer_two.Add(selected_truck_interest_label, 0, wx.ALL | wx.EXPAND, 4)
        selected_truck_text_sizer_two.Add(self.selected_truck_interest, 2, wx.ALL | wx.EXPAND, 4)
        selected_truck_text_sizer_two.Add(selected_truck_total_price_label, 0, wx.ALL | wx.EXPAND, 4)
        selected_truck_text_sizer_two.Add(self.selected_truck_total_price, 1, wx.ALL | wx.EXPAND, 4)
        
        selected_truck_text_sizer_three.Add(selected_truck_down_payment_label, 0, wx.ALL | wx.EXPAND, 4)
        selected_truck_text_sizer_three.Add(self.selected_truck_down_payment, 1, wx.ALL | wx.EXPAND, 4)
        selected_truck_text_sizer_three.Add(selected_truck_amount_remaining_label, 0, wx.ALL | wx.EXPAND, 4)
        selected_truck_text_sizer_three.Add(self.selected_truck_amount_remaining, 1, wx.ALL | wx.EXPAND, 4)
        selected_truck_text_sizer_three.Add(selected_truck_payments_label, 0, wx.ALL | wx.EXPAND, 4)
        selected_truck_text_sizer_three.Add(self.selected_truck_payments, 1, wx.ALL | wx.EXPAND, 4)
        selected_truck_text_sizer_three.Add(selected_truck_next_payment_label, 0, wx.ALL | wx.EXPAND, 4)
        selected_truck_text_sizer_three.Add(self.selected_truck_next_payment, 2, wx.ALL | wx.EXPAND, 4)

        selected_truck_btn_sizer.Add(new_truck_btn, 1, wx.ALL | wx.EXPAND)
        selected_truck_btn_sizer.Add(rent_truck_btn, 1,  wx.ALL | wx.EXPAND)
        selected_truck_btn_sizer.Add(finance_truck_btn, 1,  wx.ALL | wx.EXPAND)

        selected_truck_btn_sizer.Add(print_payments_btn, 1, wx.ALL | wx.EXPAND)
        selected_truck_btn_sizer.Add(edit_buyer_btn, 1,  wx.ALL | wx.EXPAND)
        selected_truck_btn_sizer.Add(choose_buyer_btn, 1,  wx.ALL | wx.EXPAND)
        selected_truck_btn_sizer.Add(buyback_btn, 1, wx.ALL | wx.EXPAND)

        selected_truck_btn_sizer.Add(delete_buyer_btn, 1,  wx.ALL | wx.EXPAND)
        selected_truck_btn_sizer.Add(delete_truck_btn, 1,  wx.ALL | wx.EXPAND)

        selected_truck_sizer.Add(selected_truck_text_sizer_one)
        selected_truck_sizer.Add(selected_truck_text_sizer_two)
        selected_truck_sizer.Add(selected_truck_text_sizer_three)
        selected_truck_sizer.Add(selected_truck_btn_sizer)

        self.paymentsOlv = Olv(self, wx.ID_ANY, style=wx.LC_REPORT)

        self.paymentsOlv.SetColumns([
            ColumnDefn("Date", "left", 120, "due_date", stringConverter=date_str),
            ColumnDefn("Description", "left", 200, "description"),
            ColumnDefn("Balance", "left", 120, "balance_before", stringConverter=numbers_with_commas),
            ColumnDefn("Payment", "left", 120, "payment_amount", stringConverter=numbers_with_commas),
            ColumnDefn("New Balance", "left", 120, "new_balance", stringConverter=numbers_with_commas),
            ColumnDefn("Received", "left", 90, "is_confirmed", stringConverter=confirm_status,
                       valueSetter=self.confirm_payment),
            ColumnDefn("Payment Date", "left", 150, "payment_date", stringConverter=date_str)
        ])

        self.paymentsOlv.cellEditMode = Olv.CELLEDIT_SINGLECLICK
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(selected_truck_sizer, 1, wx.ALL | wx.EXPAND, 5)
        sizer.Add(self.paymentsOlv, 5, wx.ALL | wx.EXPAND, 5)
        self.SetSizer(sizer)

    def set_truck(self, truck):
        self.selected_truck = truck
        self.selected_truck_vin.SetValue(truck.vin_number)
        self.selected_truck_description.SetValue(truck.description)

        if truck.current_buyer is not None:
            self.selected_truck_buyer.SetValue(truck.current_buyer.name)

            self.selected_truck_sale_price.SetValue(str(truck.current_buyer.sale_price))
            self.selected_truck_tax.SetValue(str(truck.current_buyer.tax))
            self.selected_truck_interest.SetValue(str(truck.current_buyer.interest))
            self.selected_truck_total_price.SetValue(str(truck.current_buyer.get_total_price()))

            self.selected_truck_down_payment.SetValue(str(truck.current_buyer.down_payment))
            self.selected_truck_amount_remaining.SetValue(str(truck.current_buyer.amount_remaining))
            self.selected_truck_payments.SetValue(str(truck.current_buyer.get_payments_made()))
            self.selected_truck_next_payment.SetValue(str(truck.current_buyer.next_payment_date))
            self.paymentsOlv.SetObjects(truck.current_buyer.payment_list)

    def clear_truck(self):
        self.selected_truck = None
        self.selected_truck_vin.Clear()
        self.selected_truck_description.Clear()

        self.selected_truck_buyer.Clear()

        self.selected_truck_sale_price.Clear()
        self.selected_truck_tax.Clear()
        self.selected_truck_interest.Clear()
        self.selected_truck_total_price.Clear()

        self.selected_truck_down_payment.Clear()
        self.selected_truck_amount_remaining.Clear()
        self.selected_truck_payments.Clear()
        self.selected_truck_next_payment.Clear()

    def confirm_payment(self, payment, value):
        payment.is_confirmed = value
        buyer = self.selected_truck.current_buyer
        if buyer.sale_type == Truck.RENTED:
            if value is True and payment.due_date == buyer.next_payment_date:
                buyer.generate_payment_rent()
        elif buyer.sale_type == Truck.FINANCED:
            pass
        buyer.refresh_values()


def confirm_status(input_str):
    if input_str:
        return "Y"
    else:
        return ""


def date_str(input_date):
    if input_date:
        return input_date.strftime("%B %d, %Y")
    else:
        return ''


def numbers_with_commas(input_num):
    return "$ " + "{:,.2f}".format(float(input_num))
