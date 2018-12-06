from Forms import NewTruckForm, NewPaymentForm, NewBuyerForm, SaveForm
from View import TruckListView, TruckDetailView
from Models import TruckList
import pickle
import wx
import os


class PaymentTracker(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, title='PaymentTracker', size=(1050, 800))

        self.truck_list = self.load_truck_list()
        self.selected_truck = None

        self.truck_list_view = TruckListView(self)
        self.truck_list_view.set_trucks(self.truck_list.get_trucks())

        self.truck_detail_view = TruckDetailView(self)
        self.save_panel = SaveForm(self)
        self.truck_form = NewTruckForm(self)
        self.buyer_form = NewBuyerForm(self)
        self.payment_form = NewPaymentForm(self)

        top_sizer = wx.BoxSizer(wx.HORIZONTAL)
        view_sizer = wx.BoxSizer(wx.VERTICAL)
        form_sizer = wx.BoxSizer(wx.VERTICAL)

        view_sizer.Add(self.truck_list_view, 1,  wx.EXPAND, 2)
        view_sizer.Add(self.truck_detail_view, 1, wx.EXPAND, 2)

        form_sizer.Add(self.save_panel, 0, wx.ALL|wx.EXPAND, 2)
        form_sizer.Add(self.truck_form, 1,  wx.ALL |wx.EXPAND, 2)
        form_sizer.Add(self.buyer_form, 1, wx.ALL | wx.EXPAND, 2)
        form_sizer.Add(self.payment_form, 1,  wx.ALL | wx.EXPAND, 2)

        top_sizer.Add(view_sizer)
        top_sizer.Add(form_sizer)
        self.SetSizer(top_sizer)
        self.Bind(wx.EVT_BUTTON, self.handle_button_click)
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.handle_right_click)

    def handle_button_click(self, event):
        event_type = str(event.GetEventObject().GetLabel())

        if event_type == "Update":
            self.save_truck_list()
            self.truck_list.refresh_trucks()

        if event_type == "Add Truck":
            if self.truck_form.verify_values():
                values = self.truck_form.get_values()
                print(values)
                self.truck_list.add_truck(values[0], values[1], values[2], values[3], values[4])
                self.save_truck_list()
                self.truck_form.clear_values()
            else:
                dlg = wx.MessageDialog(self,
                                       "Check if Purchase Cost is a number!",
                                       "Check Values",
                                       wx.OK)
                dlg.ShowModal()

        if self.selected_truck is not None:

            if event_type == "Add Buyer":

                if self.buyer_form.verify_values():

                    values = self.buyer_form.get_values()
                    self.selected_truck.add_sale(values[0], values[1], values[2])
                    self.save_truck_list()
                    self.buyer_form.clear_values()

                else :
                    dlg = wx.MessageDialog(self,
                                           "Check if DownPayment & SalePrice are numbers!",
                                           "Check values",
                                           wx.OK)
                    dlg.ShowModal()

            elif event_type == "Add Payment":
                values = self.payment_form.get_values()

                if self.payment_form.verify_values():

                    self.selected_truck.add_payment_with_buyer(values[0], values[1], values[2])
                    self.truck_detail_view.set_buyers(self.selected_truck.sale_info)
                    self.save_truck_list()
                    self.payment_form.clear_values()
                else:
                    dlg = wx.MessageDialog(self,
                                           "Check if payment is a number!",
                                           "Check values",
                                           wx.OK)
                    dlg.ShowModal()

            # Dealing with the three delete events

            elif event_type == "Delete Truck":
                dlg = wx.MessageDialog(self,
                                       "Do you want to delete truck with VIN: {}".
                                       format(self.selected_truck.vin_number),
                                       'Delete Truck',
                                       wx.YES_NO)
                result = dlg.ShowModal()
                if result == wx.ID_YES:
                    self.truck_list.delete_truck(self.selected_truck)
                    self.save_truck_list()

            elif event_type == "Delete Buyer":
                dlg = wx.MessageDialog(self,
                                       "Do you want to delete buyer {} for truck with VIN: {}".
                                       format(self.truck_detail_view.get_selected_buyer().new_owner,
                                              self.selected_truck.vin_number),
                                       'Delete Buyer',
                                       wx.YES_NO)
                result = dlg.ShowModal()
                buyer = self.truck_detail_view.get_selected_buyer()
                if result == wx.ID_YES and (buyer is not None):
                    self.selected_truck.sale_info.remove(self.truck_detail_view.get_selected_buyer())
                    self.selected_truck.refresh_truck_status()
                    self.save_truck_list()

            elif event_type == "Delete Payment":
                dlg = wx.MessageDialog(self,
                                       "Are you sure you want to delete selected payment?",
                                       'Delete Payment',
                                       wx.YES_NO)
                result = dlg.ShowModal()

                payment = self.truck_detail_view.get_selected_payment()

                if result == wx.ID_YES and payment is not None:

                    self.selected_truck.delete_payment(payment)
                    self.save_truck_list()

            self.truck_detail_view.set_buyers(self.selected_truck.sale_info)
        self.truck_list_view.set_trucks(self.truck_list.get_trucks())

    def truck_to_buyer_list(self, truck):
        return [str(sale.new_owner) for sale in truck.sale_info]

    def handle_right_click(self, event):
        self.selected_truck = self.truck_list_view.get_selected()
        if self.selected_truck:
            self.selected_truck.refresh_truck_status()
            self.truck_detail_view.set_truck(self.selected_truck)
            self.payment_form.set_buyer_list(self.truck_to_buyer_list(self.selected_truck))
        event.StopPropagation()

    def load_truck_list(self):

        file_path = "data/trucklist.p"

        if os.stat(file_path).st_size == 0:
            return TruckList()

        truck_list_file = open(file_path, "rb")
        truck_list_object = pickle.load(truck_list_file)
        truck_list_file.close()
        return truck_list_object

    def save_truck_list(self):
        truck_list_file = open("data/trucklist.p", "wb")
        pickle.dump(self.truck_list, truck_list_file)
        truck_list_file.close()


# Run the program
if __name__ == '__main__':
    app = wx.App(False)
    frame = PaymentTracker().Show()
    app.MainLoop()
