from Forms import NewTruckForm, RentTruckForm, FinanceTruckForm
from View import TruckListView, TruckDetailView
from Models import TruckList, Truck
import ObjectListView
from wx.lib.pubsub import pub
import pickle
import wx
import os
import matplotlib.pyplot as pt

TRUCK_UNAVAILABLE = 'Truck is not available'
TRUCK_NO_BUYER = 'Truck has no buyer'
TRUCK_NOT_SELECTED = 'No Truck Selected'
TRUCK_HAS_NO_BUYER = "Truck has no current buyer"

class PaymentTracker(wx.Frame):


    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, title='PaymentTracker', size=(950, 620))

        pub.subscribe(self.form_handler, 'root-listener')

        self.truck_list = self.load_truck_list()
        self.selected_truck = None

        self.truck_list_view = TruckListView(self)
        self.truck_list_view.set_trucks(self.truck_list.get_trucks())

        self.truck_detail_view = TruckDetailView(self)

        top_sizer = wx.BoxSizer(wx.VERTICAL)
        truck_list_sizer = wx.BoxSizer(wx.HORIZONTAL)
        truck_detail_sizer = wx.BoxSizer(wx.HORIZONTAL)

        truck_list_sizer.Add(self.truck_list_view, 1,  wx.EXPAND, 2)
        truck_detail_sizer.Add(self.truck_detail_view, 1, wx.EXPAND, 2)

        top_sizer.Add(truck_list_sizer)
        top_sizer.Add(truck_detail_sizer)
        self.SetSizer(top_sizer)

        self.Bind(wx.EVT_BUTTON, self.handle_button_click)
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.handle_right_click)
        self.Bind(ObjectListView.EVT_CELL_EDIT_FINISHED, self.after_edit_refresher)

    def after_edit_refresher(self, event=None):
        if event is not None:
            event.StopPropagation()
        self.save_truck_list()

    def form_handler(self, form_type, form_data):

        if form_type == "New Truck":
            self.truck_list.add_truck(vin=form_data["vin"],
                                      year=form_data["year"],
                                      make=form_data["make"],
                                      purchase_cost=form_data["purchase_cost"],
                                      prev_owner=form_data["prev_owner"],
                                      description=form_data["description"])

        elif form_type == "Rent Truck":
            self.selected_truck.add_buyer(name=form_data["buyer_name"])
            self.selected_truck.current_buyer.rent_truck(monthly_payment=form_data["monthly_payment"],
                                                         first_payment_date=form_data["first_payment_date"])

        elif form_type == "Finance Truck":
            self.selected_truck.add_buyer(name=form_data["buyer_name"])
            self.selected_truck.current_buyer.finance_truck(sale_price=form_data["sale_price"],
                                                            interest=form_data["interest"],
                                                            tax=form_data["tax"],
                                                            down_payment=form_data["down_payment"],
                                                            term_length=form_data["term_length"],
                                                            first_payment_date=form_data["first_payment_date"])

        self.refresh_truck_list()


    def handle_button_click(self, event):
        event_type = str(event.GetEventObject().GetLabel())

        if event_type == "New Truck":
            NewTruckForm().Show()

        elif event_type == "Delete Truck":
            if not self.is_truck_selected():
                wx.MessageBox(TRUCK_NOT_SELECTED, 'Error', wx.OK | wx.ICON_ERROR)
                return

            dlg = wx.MessageDialog(None, "Do you want to delete truck with vin: {}".
                                   format(self.selected_truck.vin_number),
                                   'Updater', wx.YES_NO | wx.ICON_QUESTION)
            result = dlg.ShowModal()

            if result == wx.ID_YES:
                self.truck_list.delete_truck(self.selected_truck)

        elif event_type == "Delete Buyer":
            if not self.is_truck_selected():
                wx.MessageBox(TRUCK_NOT_SELECTED, 'Error', wx.OK | wx.ICON_ERROR)
                return
            elif self.selected_truck.current_buyer is None:
                wx.MessageBox(TRUCK_NO_BUYER, 'Error', wx.OK | wx.ICON_ERROR)
                return
            else:
                dlg = wx.MessageDialog(None, "Do you want to delete buyer {}".
                                       format(self.selected_truck.current_buyer.name),
                                       'Updater', wx.YES_NO | wx.ICON_QUESTION)
                result = dlg.ShowModal()

                if result == wx.ID_YES:

                    self.selected_truck.buyers.pop(self.selected_truck.current_buyer)
                    self.selected_truck.current_buyer = None

        elif event_type == "Choose Buyer":
            pass

        elif event_type == "Rent Truck":
            if not self.is_truck_selected():
                wx.MessageBox(TRUCK_NOT_SELECTED, 'Error', wx.OK | wx.ICON_ERROR)
                return
            if self.truck_has_buyer():
                wx.MessageBox(TRUCK_UNAVAILABLE, 'Error', wx.OK | wx.ICON_ERROR)
                return
            rent_truck_form = RentTruckForm()
            rent_truck_form.Show()

        elif event_type == "Finance Truck":
            if not self.is_truck_selected():
                wx.MessageBox(TRUCK_NOT_SELECTED, 'Error', wx.OK | wx.ICON_ERROR)
                return
            if self.truck_has_buyer():
                wx.MessageBox(TRUCK_UNAVAILABLE, 'Error', wx.OK | wx.ICON_ERROR)
                return

            finance_truck_form = FinanceTruckForm()
            finance_truck_form.Show()

        elif event_type == "Print Payments":
            if not self.is_truck_selected():
                wx.MessageBox(TRUCK_NOT_SELECTED, 'Error', wx.OK | wx.ICON_ERROR)
                return
            if not self.truck_has_buyer():
                wx.MessageBox(TRUCK_NO_BUYER, 'Error', wx.OK | wx.ICON_ERROR)
                return

            self.print_payment()

        elif event_type == "Edit Buyer":
            pass

        elif event_type == "Buyback":
            if not self.is_truck_selected():
                wx.MessageBox(TRUCK_NOT_SELECTED, 'Error', wx.OK | wx.ICON_ERROR)
                return
            elif self.selected_truck.current_buyer is None:
                wx.MessageBox(TRUCK_NO_BUYER, 'Error', wx.OK | wx.ICON_ERROR)
                return
            else:
                dlg = wx.MessageDialog(None, "Do you want to buyback truck ?",
                                       'Updater', wx.YES_NO | wx.ICON_QUESTION)
                result = dlg.ShowModal()

                if result == wx.ID_YES:

                    self.selected_truck.current_buyer = None
                    print(self.selected_truck.current_buyer)
        self.refresh_truck_list()

    def print_payment(self):

        def payment_list_maker(payment_list):
            """
            This function will take the list of Payment Objects and return a dict with lists as values.The lists
            can be  directly feed into the plotly Table as data

            Example- {'payment_date':[the payments dates of all the Payment Objects], '':[], ...}"

            :param payment_list: PaymentObject from Models
            :return:
            """

            return {'Date': [payment.due_date for payment in payment_list],
                    'Description': [payment.description for payment in payment_list],
                    'Balance': [payment.balance_before for payment in payment_list],
                    'Payment': [payment.payment_amount for payment in payment_list],
                    'New Balance': [payment.new_balance for payment in payment_list],
                    'Confirmation': [payment.is_confirmed for payment in payment_list]}

        def rent_table(input_data):
            values = ['Date', 'Description', 'Payment', 'Confirmation']
            return #Table
        def finance_table(input_data):
            values = ['Date', 'Description', 'Balance', 'Payment', 'New Balance', 'Confirmation']
            return#Table

        buyer = self.selected_truck.current_buyer
        data = payment_list_maker(buyer.payment_list)

        if buyer.sale_type == Truck.RENTED:
            table = rent_table(data)
        elif buyer.sale_type == Truck.FINANCED:
            table = finance_table(data)
        else:
            pass
        py.iplot([table])





    def truck_to_buyer_list(self, truck):
        return [str(sale.new_owner) for sale in truck.sale_info]

    def handle_right_click(self, event):

        self.selected_truck = self.truck_list_view.get_selected()
        self.truck_detail_view.clear_truck()
        self.truck_list.refresh_trucks()

        if self.selected_truck:

            self.truck_detail_view.set_truck(self.selected_truck)

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

    def refresh_truck_list(self):
        self.save_truck_list()
        # self.truck_list.refresh_trucks()
        self.truck_list_view.set_trucks(self.truck_list.get_trucks())
        if self.selected_truck:
            self.truck_detail_view.set_truck(self.selected_truck)
        else:
            self.truck_detail_view.clear_truck()

    def is_truck_selected(self):
        if self.selected_truck:
            return True
        return False

    def truck_has_buyer(self):
        if self.selected_truck:
            if self.selected_truck.current_buyer:
                return True

        return False


# Run the program
if __name__ == '__main__':
    app = wx.App(False)
    frame = PaymentTracker().Show()
    app.MainLoop()
