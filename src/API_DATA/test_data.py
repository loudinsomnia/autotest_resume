from faker import Faker
import pytest
import pyotp
import uuid


class APITestData:
    pass


class USERTestData:
    pass


class SecretKey:
    pass


class APIKey:
    pass


class Transactions:
    pass


class Merchant:
    pass


class Assets:
    pass


class AdminMethods:
    pass


class InternalWallet:
    pass


class NoneLoginData:
    fake = Faker()
    email = fake.email()
    register_data = {"email": fake.email(),
                     "password": None}
