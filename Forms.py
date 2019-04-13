import wx
import wx.adv
from wx.lib.pubsub import pub
from wx.core import DateTime as wxDateTime
from Models import Truck
from datetime import date


class NewTruckForm(wx.Frame):

    def __init__(self):
        # Add a panel so it looks correct on all platforms
        wx.Frame.__init__(self, None,wx.ID_ANY, "Add a Truck", size=(270, 330))

        top_panel = wx.Panel(self, wx.ID_ANY)
        title = wx.StaticText(top_panel, wx.ID_ANY, 'New Truck')

        label_one = wx.StaticText(top_panel, wx.ID_ANY, 'VIN')
        self.vin = wx.TextCtrl(top_panel, wx.ID_ANY, '')

        label_two = wx.StaticText(top_panel, wx.ID_ANY, 'Year')
        self.year = wx.TextCtrl(top_panel, wx.ID_ANY, '')

        label_make = wx.StaticText(top_panel, wx.ID_ANY, 'Make')
        self.make = wx.TextCtrl(top_panel, wx.ID_ANY, '')

        label_three = wx.StaticText(top_panel, wx.ID_ANY, 'Previous Owner')
        self.prev_owner = wx.TextCtrl(top_panel, wx.ID_ANY, '')

        label_four = wx.StaticText(top_panel, wx.ID_ANY, 'Purchase Cost')
        self.purchase_cost = wx.TextCtrl(top_panel, wx.ID_ANY, '')

        label_five = wx.StaticText(top_panel, wx.ID_ANY, 'Description')
        self.description = wx.TextCtrl(top_panel, wx.ID_ANY, '')

        ok_btn = wx.Button(top_panel, wx.ID_ANY, 'Add Truck')
        close_btn = wx.Button(top_panel, wx.ID_ANY, "Close")

        ok_btn.Bind(wx.EVT_BUTTON, self.send_values)
        close_btn.Bind(wx.EVT_BUTTON, self.close)

        top_sizer = wx.BoxSizer(wx.VERTICAL)
        title_sizer = wx.BoxSizer(wx.HORIZONTAL)
        vin_sizer = wx.BoxSizer(wx.HORIZONTAL)
        year_sizer = wx.BoxSizer(wx.HORIZONTAL)
        make_sizer = wx.BoxSizer(wx.HORIZONTAL)
        prev_owner_sizer = wx.BoxSizer(wx.HORIZONTAL)
        cost_sizer = wx.BoxSizer(wx.HORIZONTAL)
        description_sizer = wx.BoxSizer(wx.HORIZONTAL)

        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)

        title_sizer.Add(title, 0, wx.ALL, 4)

        vin_sizer.Add(label_one, 1, wx.ALL, 4)
        vin_sizer.Add(self.vin, 1, wx.ALL | wx.EXPAND, 4)

        year_sizer.Add(label_two, 1, wx.ALL, 4)
        year_sizer.Add(self.year, 1, wx.ALL | wx.EXPAND, 4)

        make_sizer.Add(label_make, 1, wx.ALL, 4)
        make_sizer.Add(self.make, 1, wx.ALL | wx.EXPAND, 4)

        prev_owner_sizer.Add(label_three, 1, wx.ALL, 4)
        prev_owner_sizer.Add(self.prev_owner, 1, wx.ALL | wx.EXPAND, 4)

        cost_sizer.Add(label_four, 1, wx.ALL, 4)
        cost_sizer.Add(self.purchase_cost, 1, wx.ALL | wx.EXPAND, 4)

        description_sizer.Add(label_five, 1, wx.ALL, 4)
        description_sizer.Add(self.description, 1, wx.ALL | wx.EXPAND, 4)

        btn_sizer.Add(ok_btn, 0, wx.ALL, 4)
        btn_sizer.Add(close_btn, 0, wx.ALL, 4)

        top_sizer.Add(title_sizer, 0, wx.CENTER)
        top_sizer.Add(wx.StaticLine(top_panel), 0, wx.ALL | wx.EXPAND, 4)
        top_sizer.Add(vin_sizer, 1, wx.CENTER, 4)
        top_sizer.Add(year_sizer, 1, wx.CENTER, 4)
        top_sizer.Add(make_sizer, 1, wx.CENTER, 4)
        top_sizer.Add(prev_owner_sizer, 1, wx.CENTER, 4)
        top_sizer.Add(cost_sizer, 1, wx.CENTER, 4)
        top_sizer.Add(description_sizer, 1, wx.CENTER, 4)
        top_sizer.Add(wx.StaticLine(top_panel), 0, wx.ALL | wx.EXPAND, 4)
        top_sizer.Add(btn_sizer, 0, wx.ALL | wx.CENTER, 4)

        top_panel.SetSizer(top_sizer)

        self.Show()

    def get_values(self):
        return {"vin": self.vin.GetValue(),
                "year": self.year.GetValue(),
                "make": self.make.GetValue(),
                "purchase_cost": self.purchase_cost.GetValue(),
                "prev_owner": self.prev_owner.GetValue(),
                "description": self.description.GetValue()}

    def verify_values(self):
        if check_if_number(self.purchase_cost.GetValue()):
            return True
        return False

    def send_values(self, event):
        event.StopPropagation()
        if self.verify_values():

            pub.sendMessage("root-listener", form_type="New Truck", form_data=self.get_values())
            self.Close()

    def close(self, event):
        event.StopPropagation()
        self.Close()


class RentTruckForm(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "Rent a truck", size=(270, 250))

        top_panel = wx.Panel(self, wx.ID_ANY)

        title = wx.StaticText(top_panel, wx.ID_ANY, 'Rent Truck')

        buyer_label = wx.StaticText(top_panel, wx.ID_ANY, "Buyer Name")
        self.buyer = wx.TextCtrl(top_panel, wx.ID_ANY, "")

        monthly_payment_label = wx.StaticText(top_panel, wx.ID_ANY, "Monthly Payment")
        self.monthly_payment = wx.TextCtrl(top_panel, wx.ID_ANY, "")

        first_payment_label = wx.StaticText(top_panel, wx.ID_ANY, "First Payment")
        self.first_payment = wx.adv.DatePickerCtrl(top_panel, wx.ID_ANY)

        ok_btn = wx.Button(top_panel, wx.ID_ANY, 'OK')
        cancel_btn = wx.Button(top_panel, wx.ID_ANY, 'Cancel')

        ok_btn.Bind(wx.EVT_BUTTON, self.send_values)
        cancel_btn.Bind(wx.EVT_BUTTON, self.close)

        top_sizer = wx.BoxSizer(wx.VERTICAL)
        title_sizer = wx.BoxSizer(wx.HORIZONTAL)
        input_label_sizer = wx.BoxSizer(wx.VERTICAL)
        input_text_sizer = wx.BoxSizer(wx.VERTICAL)
        input_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)

        title_sizer.Add(title, 0, wx.ALL, 4)
        input_label_sizer.Add(buyer_label, 0, wx.ALL, 4)
        input_label_sizer.Add(monthly_payment_label, 0, wx.ALL, 4)
        input_label_sizer.Add(first_payment_label, 0, wx.ALL, 4)

        input_text_sizer.Add(self.buyer, 1, wx.ALL | wx.EXPAND, 4)
        input_text_sizer.Add(self.monthly_payment, 1, wx.ALL | wx.EXPAND, 4)
        input_text_sizer.Add(self.first_payment, 1, wx.ALL | wx.EXPAND, 4)

        input_sizer.Add(input_label_sizer, 1, wx.CENTER, 4)
        input_sizer.Add(input_text_sizer, 1, wx.ALL | wx.EXPAND, 4)

        btn_sizer.Add(ok_btn, 0, wx.ALL, 4)
        btn_sizer.Add(cancel_btn, 0, wx.ALL, 4)

        top_sizer.Add(title_sizer, 0, wx.CENTER)
        top_sizer.Add(wx.StaticLine(top_panel), 0, wx.ALL | wx.EXPAND, 4)
        top_sizer.Add(input_sizer, 0, wx.ALL | wx.EXPAND, 4)
        top_sizer.Add(wx.StaticLine(top_panel), 0, wx.ALL | wx.EXPAND, 4)
        top_sizer.Add(btn_sizer, 0, wx.ALL | wx.CENTER, 4)

        top_panel.SetSizer(top_sizer)

        self.Show()

    def send_values(self, event):
        event.StopPropagation()
        if self.validate_values():

            pub.sendMessage("root-listener", form_type="Rent Truck", form_data=self.get_values())
            self.Close()

    def validate_values(self):
        if check_if_number(self.monthly_payment.GetValue()) and self.buyer.GetValue() != "":
            return True
        return False

    def get_values(self):
        print(wxdatetime_to_date(self.first_payment.GetValue()),"THis line from get values" ,self.first_payment.GetValue())
        return {"buyer_name": self.buyer.GetValue(),
                "monthly_payment": float(self.monthly_payment.GetValue()),
                "first_payment_date": wxdatetime_to_date(self.first_payment.GetValue())}

    def close(self, event):
        event.StopPropagation()
        self.Close()


class FinanceTruckForm(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "Finance a truck", size=(300, 400))

        top_panel = wx.Panel(self, wx.ID_ANY)

        title = wx.StaticText(top_panel, wx.ID_ANY, 'Finance Truck')

        buyer_label = wx.StaticText(top_panel, wx.ID_ANY, "Buyer Name")
        self.buyer = wx.TextCtrl(top_panel, wx.ID_ANY, "")

        sale_price_label = wx.StaticText(top_panel, wx.ID_ANY, "Sale Price")
        self.sale_price = wx.TextCtrl(top_panel, wx.ID_ANY, "")

        interest_label = wx.StaticText(top_panel, wx.ID_ANY, "Interest")
        self.interest = wx.TextCtrl(top_panel, wx.ID_ANY, "")

        tax_label = wx.StaticText(top_panel, wx.ID_ANY, "Tax")
        self.tax = wx.TextCtrl(top_panel, wx.ID_ANY, "")

        down_payment_label = wx.StaticText(top_panel, wx.ID_ANY, "Down Payment")
        self.down_payment = wx.TextCtrl(top_panel, wx.ID_ANY, "")

        term_length_label = wx.StaticText(top_panel, wx.ID_ANY, "Term Length")
        self.term_length = wx.TextCtrl(top_panel, wx.ID_ANY, "")

        first_payment_label = wx.StaticText(top_panel, wx.ID_ANY, "First Payment")
        self.first_payment = wx.adv.DatePickerCtrl(top_panel, wx.ID_ANY)

        ok_btn = wx.Button(top_panel, wx.ID_ANY, 'OK')
        cancel_btn = wx.Button(top_panel, wx.ID_ANY, 'Cancel')

        ok_btn.Bind(wx.EVT_BUTTON, self.send_values)
        cancel_btn.Bind(wx.EVT_BUTTON, self.close)

        top_sizer = wx.BoxSizer(wx.VERTICAL)
        title_sizer = wx.BoxSizer(wx.HORIZONTAL)

        buyer_sizer = wx.BoxSizer(wx.HORIZONTAL)
        sale_price_sizer = wx.BoxSizer(wx.HORIZONTAL)
        interest_sizer = wx.BoxSizer(wx.HORIZONTAL)
        tax_sizer = wx.BoxSizer(wx.HORIZONTAL)
        down_payment_sizer = wx.BoxSizer(wx.HORIZONTAL)
        term_length_sizer = wx.BoxSizer(wx.HORIZONTAL)
        first_payment_sizer = wx.BoxSizer(wx.HORIZONTAL)

        input_sizer = wx.BoxSizer(wx.VERTICAL)
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)

        title_sizer.Add(title, 0, wx.ALL, 4)

        buyer_sizer.Add(buyer_label, 1, wx.ALL, 4)
        buyer_sizer.Add(self.buyer, 1, wx.ALL | wx.EXPAND, 4)

        sale_price_sizer.Add(sale_price_label, 1, wx.ALL, 4)
        sale_price_sizer.Add(self.sale_price, 1, wx.ALL | wx.EXPAND, 4)

        interest_sizer.Add(interest_label, 1, wx.ALL, 4)
        interest_sizer.Add(self.interest, 1, wx.ALL | wx.EXPAND, 4)

        tax_sizer.Add(tax_label, 1, wx.ALL, 4)
        tax_sizer.Add(self.tax, 1, wx.ALL | wx.EXPAND, 4)

        down_payment_sizer.Add(down_payment_label, 1, wx.ALL, 4)
        down_payment_sizer.Add(self.down_payment, 1, wx.ALL | wx.EXPAND, 4)

        term_length_sizer.Add(term_length_label, 1, wx.ALL, 4)
        term_length_sizer.Add(self.term_length, 1, wx.ALL | wx.EXPAND, 4)

        first_payment_sizer.Add(first_payment_label, 1, wx.CENTER, 4)
        first_payment_sizer.Add(self.first_payment, 1, wx.ALL | wx.EXPAND, 6)

        input_sizer.Add(buyer_sizer, 1, wx.CENTER, 4)
        input_sizer.Add(sale_price_sizer, 1, wx.CENTER, 4)
        input_sizer.Add(interest_sizer, 1, wx.CENTER, 4)
        input_sizer.Add(tax_sizer, 1, wx.CENTER, 4)
        input_sizer.Add(down_payment_sizer, 1, wx.CENTER, 4)
        input_sizer.Add(term_length_sizer, 1, wx.CENTER, 4)
        input_sizer.Add(first_payment_sizer, 1, wx.CENTER, 4)

        btn_sizer.Add(ok_btn, 0, wx.ALL, 4)
        btn_sizer.Add(cancel_btn, 0, wx.ALL, 4)

        top_sizer.Add(title_sizer, 0, wx.CENTER)
        top_sizer.Add(wx.StaticLine(top_panel), 0, wx.ALL | wx.EXPAND, 4)
        top_sizer.Add(input_sizer, 0, wx.ALL | wx.EXPAND, 4)
        top_sizer.Add(wx.StaticLine(top_panel), 0, wx.ALL | wx.EXPAND, 4)
        top_sizer.Add(btn_sizer, 0, wx.ALL | wx.CENTER, 4)

        top_panel.SetSizer(top_sizer)

        self.Show()

    def send_values(self, event):
        event.StopPropagation()
        if self.validate_values():

            pub.sendMessage("root-listener", form_type="Finance Truck", form_data=self.get_values())
            self.Close()
        else:
            dlg = wx.MessageDialog(None,
                                   "Check values and make sure buyer name is not empty.",
                                   'Error', wx.OK_DEFAULT | wx.ICON_EXCLAMATION)
            dlg.ShowModal()

    def validate_values(self):
        should_be_num_list = [self.sale_price.GetValue(), self.interest.GetValue(), self.tax.GetValue(),
                              self.down_payment.GetValue(), self.term_length.GetValue()]

        check_list = [1 for value in should_be_num_list if check_if_number(value)]

        if self.buyer.GetValue() != "" and len(check_list) == 5:
            return True
        return False

    def get_values(self):
        return {"buyer_name": self.buyer.GetValue(),
                "sale_price": float(self.sale_price.GetValue()),
                "interest": float(self.interest.GetValue()),
                "tax": float(self.tax.GetValue()),
                "down_payment": float(self.down_payment.GetValue()),
                "term_length": int(self.term_length.GetValue()),
                "first_payment_date": wxdatetime_to_date(self.first_payment.GetValue())}

    def close(self, event):
        event.StopPropagation()
        self.Close()

def check_if_number(value):
    try:
        float(value)
    except TypeError:
        print("Wrong Type for number comparison")
        return False

    except ValueError:
        return False

    return True


def wxdatetime_to_date(input_datetime):
    if isinstance(input_datetime, wxDateTime):
        return date(input_datetime.year, input_datetime.month + 1, input_datetime.day)
    else:
        print("Not wxtime",type(input_datetime))
        return input_datetime
