import unittest
from ..fixture import get_path


from bricklane_platform.services.payment_processor import PaymentProcessor
from bricklane_platform.models.payment import Payment


def create_stub_payment(mock_is_successful):
    payment = Payment()
    payment.is_successful = lambda: mock_is_successful
    return payment


class TestPaymentProcessor(unittest.TestCase):

    def setUp(self):
        self.payment_processor = PaymentProcessor()
        self.card_fixture = get_path("card_payments_mixed.csv")
        self.bank_fixture = get_path("bank_payments.csv")
        self.empty_card_fixture = get_path("card_payments_empty.csv")
        self.empty_bank_fixture = get_path("bank_payments_empty.csv")

    def test_get_payments(self):

        card_payments = self.payment_processor.get_payments(
            self.card_fixture, "card")
        self.assertEqual(len(card_payments), 3)
        self.assertEqual(card_payments[0].card.card_id, 30)
        self.assertEqual(card_payments[1].card.card_id, 45)
        self.assertEqual(card_payments[2].card.card_id, 10)

        bank_payments = self.payment_processor.get_payments(
            self.bank_fixture, "bank")
        self.assertEqual(len(bank_payments), 2)
        self.assertEqual(bank_payments[0].bank.bank_account_id, '20')
        self.assertEqual(bank_payments[1].bank.bank_account_id, '60')

    def test_get_payments_empty(self):
        card_payments = self.payment_processor.get_payments(
            self.empty_card_fixture, "card")
        bank_payments = self.payment_processor.get_payments(
            self.empty_bank_fixture, "bank")
        self.assertEqual(len(bank_payments), 0)
        self.assertEqual(len(card_payments), 0)

    def test_verify_payments(self):
        payment1 = create_stub_payment(mock_is_successful=True)
        payment2 = create_stub_payment(mock_is_successful=False)
        payment3 = create_stub_payment(mock_is_successful=True)

        result = self.payment_processor.verify_payments(
            [payment1, payment2, payment3])
        self.assertEqual(result, [payment1, payment3])
