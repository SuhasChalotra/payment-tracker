import wx
from ObjectListView import ObjectListView, ColumnDefn
from Models import Truck

class TruckListView(wx.Panel):

    def __init__(self, parent):

        wx.Panel.__init__(self, parent=parent)
        self.dataOlv = ObjectListView(self, wx.ID_ANY,
                                      style=wx.LC_REPORT)

        done = wx.Bitmap("data/Checkmark.png", wx.BITMAP_TYPE_ANY)
        progress = wx.Bitmap("data/Progress.png", wx.BITMAP_TYPE_ANY)
        self.done = self.dataOlv.AddImages(wx.Icon(done))
        self.progress = self.dataOlv.AddImages(wx.Icon(progress))

        self.dataOlv.SetColumns([
            ColumnDefn("Buyer", "left", 150, "current_owner", imageGetter=self.image_getter),
            ColumnDefn("VIN", "left", 150, "vin_number"),
            ColumnDefn("Year", "left", 65, "year"),
            ColumnDefn("Description", "left", 130, "description"),
            ColumnDefn("Previous Owner", "left", 100, "prev_owner"),
            ColumnDefn("Purchase Cost", "left", 100, "purchase_cost", stringConverter=numbers_with_commas)
        ])

        self.dataOlv.rowFormatter = row_formatter

        self.dataOlv.cellEditMode = ObjectListView.CELLEDIT_SINGLECLICK

        sizer = wx.BoxSizer(wx.VERTICAL)
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
        elif truck.status == Truck.IN_PROGRESS:
            return self.progress


def row_formatter(listItem, truck):
    if truck.status == truck.COMPLETED:
        listItem.SetBackgroundColour(wx.Colour(197, 247, 213))
    elif truck.status == truck.IN_PROGRESS:
        listItem.SetBackgroundColour(wx.Colour(165, 224, 240))
    else:
        listItem.SetBackgroundColour(wx.WHITE)


class TruckDetailView(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)

        self.selected_truck = None

        selected_truck_label = wx.StaticText(self, wx.ID_ANY, "Selected Truck VIN")
        self.selected_truck_text = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_READONLY)
        delete_truck_btn = wx.Button(self, wx.ID_ANY, "Delete Truck")
        delete_buyer_btn = wx.Button(self, wx.ID_ANY, 'Delete Buyer')
        delete_payment_btn = wx.Button(self, wx.ID_ANY, 'Delete Payment')

        selected_truck_sizer = wx.BoxSizer(wx.HORIZONTAL)
        selected_truck_sizer.Add(selected_truck_label, 1, wx.ALL | wx.EXPAND, 5)
        selected_truck_sizer.Add(self.selected_truck_text, 2, wx.ALL | wx.EXPAND, 5)
        selected_truck_sizer.Add(delete_truck_btn, 1, wx.EXPAND)
        selected_truck_sizer.Add(delete_buyer_btn, 1, wx.EXPAND)
        selected_truck_sizer.Add(delete_payment_btn, 1, wx.EXPAND)
        self.buyerOlv = ObjectListView(self, wx.ID_ANY, style=wx.LC_REPORT)

        self.buyerOlv.SetColumns([
            ColumnDefn("Buyer", "left", 150, "new_owner"),
            ColumnDefn("Sale Price", "left", 140, "sale_price", stringConverter=numbers_with_commas),
            ColumnDefn("Amount Remaining", "left", 160, "amount_remaining", stringConverter=numbers_with_commas),
            ColumnDefn("Amount Received", "left", 160, "amount_paid", stringConverter=numbers_with_commas),
        ])

        self.buyerOlv.cellEditMode = ObjectListView.CELLEDIT_SINGLECLICK

        self.paymentsOlv = ObjectListView(self, wx.ID_ANY, style=wx.LC_REPORT)

        self.paymentsOlv.SetColumns([
            ColumnDefn("Buyer", "left", 200, "buyer"),
            ColumnDefn("Date", "left", 150, "date", stringConverter=date_str),
            ColumnDefn("Payment Amount", "left", 150, "payment_amount", stringConverter=numbers_with_commas),
            ColumnDefn("Description", "left", 200, "description")
        ])

        self.paymentsOlv.cellEditMode = ObjectListView.CELLEDIT_SINGLECLICK

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(selected_truck_sizer, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(self.buyerOlv, 1, wx.ALL | wx.EXPAND, 5)
        sizer.Add(self.paymentsOlv, 2, wx.ALL | wx.EXPAND, 5)
        self.SetSizer(sizer)

    def set_buyers(self, buyers):
        self.buyerOlv.SetObjects(buyers)
        payment_list = []

        for buyer in buyers:
            payment_list += buyer.payments
        self.paymentsOlv.SetObjects(payment_list)

    def set_truck(self, truck):
        self.selected_truck = truck
        self.selected_truck_text.SetValue(truck.vin_number)

        self.set_buyers(self.selected_truck.sale_info)

    def clear_truck(self):
        self.selected_truck = None
        self.selected_truck_text.Clear()

    def get_selected_buyer(self):
        return self.buyerOlv.GetSelectedObject()

    def get_selected_payment(self):
        return self.paymentsOlv.GetSelectedObject()


def date_str(input_date):
    return input_date.strftime("%B %d, %Y")


def numbers_with_commas(input_num):
    return "$ " + "{:,.2f}".format(float(input_num))
