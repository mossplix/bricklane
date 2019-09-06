import unittest
from datetime import datetime

from bricklane_platform.models.payment import Payment
from bricklane_platform.models.card import Card
from bricklane_platform.models.bank import Bank


class TestPayment(unittest.TestCase):

    def test_init(self):
        payment = Payment()

        self.assertIsNone(payment.customer_id)
        self.assertIsNone(payment.date)
        self.assertIsNone(payment.amount)
        self.assertIsNone(payment.fee)
        self.assertIsNone(payment.card_id)

    def test_init_with_data(self):

        payment_data = [{
            "amount": "2000",
            "card_id": "45",
            "card_status": "processed",
            "customer_id": "123",
            "date": "2019-02-01",
        }, {
            "amount": "2000",
            "bank_account_id": "45",
            "customer_id": "123",
            "date": "2019-02-01"
        }]
        for data in payment_data:

            payment = Payment(data)

            self.assertEqual(payment.customer_id, 123)
            self.assertEqual(payment.date, datetime(2019, 2, 1))
            self.assertEqual(payment.amount, 1960)
            self.assertEqual(payment.fee, 40)

            if payment.card:
                card = payment.card
                self.assertIsInstance(card, Card)
                self.assertEqual(card.card_id, 45)
                self.assertEqual(card.status, "processed")
            if payment.bank:
                bank = payment.bank
                self.assertIsInstance(bank, Bank)
                self.assertEqual(bank.bank_account_id, 45)
                self.assertEqual(card.status, "processed")

    def test_is_successful(self):
        card = Card()
        card.status = "processed"
        payment1 = Payment()
        payment1.card = card

        bank = Bank()
        bank.status = "processed"
        payment2 = Payment()
        payment2.bank = bank

        self.assertTrue(payment1.is_successful())
        self.assertTrue(payment2.is_successful())

    def test_is_successful_declined(self):
        card = Card()
        card.status = "declined"
        payment = Payment()
        payment.card = card

        self.assertFalse(payment.is_successful())

    def test_is_successful_errored(self):
        card = Card()
        card.status = "errored"
        payment = Payment()
        payment.card = card

        self.assertFalse(payment.is_successful())
