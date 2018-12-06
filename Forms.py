import wx
import wx.adv
from Models import Truck

class SaveForm(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)


        self.save_button = wx.Button(self, wx.ID_ANY, 'Update', style=wx.BU_EXACTFIT)
        self.save_button.SetBackgroundColour(wx.Colour(55, 186, 0))
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.save_button, 0, wx.EXPAND, 0)

        self.SetSizer(sizer)


class NewTruckForm(wx.Panel):

    def __init__(self, parent):
        # Add a panel so it looks correct on all platforms
        wx.Panel.__init__(self, parent=parent)

        title = wx.StaticText(self, wx.ID_ANY, 'New Truck')

        label_one = wx.StaticText(self, wx.ID_ANY, 'VIN')
        self.vin = wx.TextCtrl(self, wx.ID_ANY, '')

        label_two = wx.StaticText(self, wx.ID_ANY, 'Year')
        self.year = wx.TextCtrl(self, wx.ID_ANY, '')

        label_three = wx.StaticText(self, wx.ID_ANY, 'Previous Owner')
        self.prev_owner = wx.TextCtrl(self, wx.ID_ANY, '')

        label_four = wx.StaticText(self, wx.ID_ANY, 'Purchase Cost')
        self.purchase_cost = wx.TextCtrl(self, wx.ID_ANY, '')

        label_five = wx.StaticText(self, wx.ID_ANY, 'Description')
        self.description = wx.TextCtrl(self, wx.ID_ANY, '')

        ok_btn = wx.Button(self, wx.ID_ANY, 'Add Truck')

        top_sizer = wx.BoxSizer(wx.VERTICAL)
        title_sizer = wx.BoxSizer(wx.HORIZONTAL)
        input_label_sizer = wx.BoxSizer(wx.VERTICAL)
        input_text_sizer = wx.BoxSizer(wx.VERTICAL)
        input_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)

        title_sizer.Add(title, 0, wx.ALL, 4)
        input_label_sizer.Add(label_one, 0, wx.ALL, 4)
        input_label_sizer.Add(label_two, 0, wx.ALL, 4)
        input_label_sizer.Add(label_three, 0, wx.ALL, 4)
        input_label_sizer.Add(label_four, 0, wx.ALL, 4)
        input_label_sizer.Add(label_five, 0, wx.ALL, 4)

        input_text_sizer.Add(self.vin, 1, wx.ALL | wx.EXPAND, 4)
        input_text_sizer.Add(self.year, 1, wx.ALL | wx.EXPAND, 4)
        input_text_sizer.Add(self.prev_owner, 1, wx.ALL | wx.EXPAND, 4)
        input_text_sizer.Add(self.purchase_cost, 1, wx.ALL | wx.EXPAND, 4)
        input_text_sizer.Add(self.description, 1, wx.ALL | wx.EXPAND, 4)
        input_sizer.Add(input_label_sizer, 1, wx.CENTER, 4)
        input_sizer.Add(input_text_sizer, 1, wx.ALL | wx.EXPAND, 4)

        btn_sizer.Add(ok_btn, 0, wx.ALL, 4)

        top_sizer.Add(title_sizer, 0, wx.CENTER)
        top_sizer.Add(wx.StaticLine(self,), 0, wx.ALL | wx.EXPAND, 4)
        top_sizer.Add(input_sizer, 0, wx.ALL | wx.EXPAND, 4)
        top_sizer.Add(wx.StaticLine(self), 0, wx.ALL | wx.EXPAND, 4)
        top_sizer.Add(btn_sizer, 0, wx.ALL | wx.CENTER, 4)

        self.SetSizer(top_sizer)



    def get_values(self):
        return [self.vin.GetValue(),
                self.year.GetValue(),
                self.purchase_cost.GetValue(),
                self.prev_owner.GetValue(),
                self.description.GetValue()]

    def clear_values(self):
        self.vin.Clear()
        self.year.Clear()
        self.purchase_cost.Clear()
        self.prev_owner.Clear()
        self.description.Clear()

    def verify_values(self):
        if check_if_number(self.purchase_cost.GetValue()):
            return True
        return False


class NewPaymentForm(wx.Panel):

    def __init__(self, parent):

        # Add a panel so it looks correct on all platforms
        wx.Panel.__init__(self, parent=parent)

        title = wx.StaticText(self, wx.ID_ANY, 'New Payment')


        label_buyer = wx.StaticText(self, wx.ID_ANY, 'Buyer')
        self.buyer = wx.ComboBox(self, wx.ID_ANY)

        label_one = wx.StaticText(self, wx.ID_ANY, 'Payment Amount')
        self.payment = wx.TextCtrl(self, wx.ID_ANY, '')

        label_two = wx.StaticText(self, wx.ID_ANY, 'Date')
        self.date = wx.adv.DatePickerCtrl(self, wx.ID_ANY)

        ok_btn = wx.Button(self, wx.ID_ANY, 'Add Payment')

        top_sizer = wx.BoxSizer(wx.VERTICAL)
        title_sizer = wx.BoxSizer(wx.HORIZONTAL)
        input_label_sizer = wx.BoxSizer(wx.VERTICAL)
        input_text_sizer = wx.BoxSizer(wx.VERTICAL)
        input_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)

        title_sizer.Add(title, 0, wx.ALL, 4)
        input_label_sizer.Add(label_buyer, 0, wx.ALL, 4)
        input_label_sizer.Add(label_one, 0, wx.ALL, 4)
        input_label_sizer.Add(label_two, 0, wx.ALL, 4)

        input_text_sizer.Add(self.buyer, 1, wx.ALL |wx.EXPAND , 4)
        input_text_sizer.Add(self.payment, 1, wx.ALL | wx.EXPAND, 4)
        input_text_sizer.Add(self.date, 1, wx.ALL | wx.EXPAND, 4)

        input_sizer.Add(input_label_sizer, 1, wx.CENTER, 4)
        input_sizer.Add(input_text_sizer, 1, wx.ALL | wx.EXPAND, 4)

        btn_sizer.Add(ok_btn, 0, wx.ALL, 4)

        top_sizer.Add(title_sizer, 0, wx.CENTER)
        top_sizer.Add(wx.StaticLine(self), 0, wx.ALL | wx.EXPAND, 4)
        top_sizer.Add(input_sizer, 0, wx.ALL | wx.EXPAND, 4)
        top_sizer.Add(wx.StaticLine(self), 0, wx.ALL | wx.EXPAND, 4)
        top_sizer.Add(btn_sizer, 0, wx.ALL | wx.CENTER, 4)

        self.SetSizer(top_sizer)


    def get_values(self):
        return [self.buyer.GetValue(),
                self.payment.GetValue(),
                self.date.GetValue()]

    def clear_values(self):
        self.payment.Clear()

    def set_buyer_list(self, buyer_list):
        self.buyer.Clear()
        for buyer in buyer_list:
            self.buyer.Append(buyer)

    def verify_values(self):
        if check_if_number(self.payment.GetValue()):
            return True
        return False


class NewBuyerForm(wx.Panel):

    def __init__(self, parent):

        # Add a panel so it looks correct on all platforms
        wx.Panel.__init__(self, parent=parent)

        title = wx.StaticText(self, wx.ID_ANY, 'New Buyer')

        label_one = wx.StaticText(self, wx.ID_ANY, 'Buyer Name')
        self.buyer = wx.TextCtrl(self, wx.ID_ANY, '')

        label_two = wx.StaticText(self, wx.ID_ANY, 'Sale Price')
        self.sale_price = wx.TextCtrl(self, wx.ID_ANY, '')

        label_three = wx.StaticText(self, wx.ID_ANY, 'Down Payment')
        self.down_payment = wx.TextCtrl(self, wx.ID_ANY, '')

        ok_btn = wx.Button(self, wx.ID_ANY, 'Add Buyer')

        top_sizer = wx.BoxSizer(wx.VERTICAL)
        title_sizer = wx.BoxSizer(wx.HORIZONTAL)
        input_label_sizer = wx.BoxSizer(wx.VERTICAL)
        input_text_sizer = wx.BoxSizer(wx.VERTICAL)
        input_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)

        title_sizer.Add(title, 0, wx.ALL, 4)
        input_label_sizer.Add(label_one, 0, wx.ALL, 4)
        input_label_sizer.Add(label_two, 0, wx.ALL, 4)
        input_label_sizer.Add(label_three, 0, wx.ALL, 4)

        input_text_sizer.Add(self.buyer, 1, wx.ALL | wx.EXPAND, 4)
        input_text_sizer.Add(self.sale_price, 1, wx.ALL | wx.EXPAND, 4)
        input_text_sizer.Add(self.down_payment, 1, wx.ALL | wx.EXPAND, 4)

        input_sizer.Add(input_label_sizer, 1, wx.CENTER, 4)
        input_sizer.Add(input_text_sizer, 1, wx.ALL | wx.EXPAND, 4)

        btn_sizer.Add(ok_btn, 0, wx.ALL, 4)

        top_sizer.Add(title_sizer, 0, wx.CENTER)
        top_sizer.Add(wx.StaticLine(self), 0, wx.ALL | wx.EXPAND, 4)
        top_sizer.Add(input_sizer, 0, wx.ALL | wx.EXPAND, 4)
        top_sizer.Add(wx.StaticLine(self), 0, wx.ALL | wx.EXPAND, 4)
        top_sizer.Add(btn_sizer, 0, wx.ALL | wx.CENTER, 4)

        self.SetSizer(top_sizer)


    def verify_values(self):
        if check_if_number(self.down_payment.GetValue()):
            if check_if_number(self.sale_price.GetValue()):

                return True
        return False

    def get_values(self):
        return [self.buyer.GetValue(),
                self.sale_price.GetValue(),
                self.down_payment.GetValue()]

    def clear_values(self):
        self.buyer.Clear()
        self.sale_price.Clear()
        self.down_payment.Clear()


def check_if_number(value):
    try:
        float(value)
    except TypeError:
        print("Wrong Type for number comparison")
        return False

    except ValueError:
        return False

    return True
