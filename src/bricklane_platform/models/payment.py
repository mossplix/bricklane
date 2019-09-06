from decimal import Decimal
from dateutil.parser import parse


from bricklane_platform.models.card import Card
from bricklane_platform.models.bank import Bank
from bricklane_platform.config import PAYMENT_FEE_RATE


class Payment(object):

    customer_id = None
    date = None
    amount = None
    fee = None
    card_id = None
    card = None
    bank = None

    def __init__(self, data=None, source="card"):

        if not data:
            return

        self.customer_id = int(data["customer_id"])
        self.date = parse(data["date"])

        total_amount = Decimal(data["amount"])
        self.fee = total_amount * PAYMENT_FEE_RATE
        self.amount = total_amount - self.fee

        if(source == "card"):
            card = Card()
            card.card_id = int(data["card_id"])
            card.status = data["card_status"]
            self.card = card
        elif(source == "bank"):
            bank = Bank()
            bank.bank_account_id = data["bank_account_id"]
            bank.status = "processed"
            self.bank = bank

    def is_successful(self):
        payment_type = self.card or self.bank
        return payment_type.status == "processed"
