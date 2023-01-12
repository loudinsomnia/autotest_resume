import pytest
import requests
import json
from conftest import config


class BaseParams:
    def __init__(self):
        self.url = config.url_v1.url
        self.admin_url = config.admin_url.url
        self.header_api = {"x-access-apikey": config.headers.x_api_key,
                           "Content-Type": config.headers.contentType}
        self.public = config.public
        self.api = config.api
        self.user = config.user
        self.admin = config.admin
        self.nonloginendpoint = config.nonloginendpoint
        self.header_jwt = {"Content-Type": config.headers.contentType,
                           "x-access-token": None}

    def jwt_parser(self, parse):
        self.header_jwt["x-access-token"] = parse
        return self.header_jwt


class Public(BaseParams):
    def get_Info(self):
        return requests.request("GET", url=self.url + self.public.getInfo)

    def getAssetsList(self):
        return requests.request("GET", url=self.url + self.public.getAssetsList)


class API(BaseParams):

    def createApiKey(self, api_cr):
        return requests.request("POST", url=self.url + self.user.createApiKey, headers=self.header_api,
                                data=json.dumps(api_cr))

    def getMerchants(self):
        return requests.request("GET", url=self.url + self.api.getMerchants, headers=self.header_api)

    def getMerchantWallets(self, merchid):
        return requests.request("GET", url=self.url + self.api.getMerchantWallets, headers=self.header_api,
                                params=json.dumps(merchid))

    def getMerchantPendings(self, merchid):
        return requests.request("GET", url=self.url + self.api.getMerchantPendings, headers=self.header_api,
                                params=json.dumps(merchid))

    def getMerchantBalances(self, merchid):
        return requests.request("GET", url=self.url + self.api.getMerchantBalances, headers=self.header_api,
                                params=json.dumps(merchid))

    def createWithdraw(self, data_cr_withdraw):
        return requests.request("POST", url=self.url + self.api.createWithdraw, headers=self.header_api,
                                data=json.dumps(data_cr_withdraw))

    def createRecive(self, data_cr_recive):
        return requests.request("POST", url=self.url + self.api.createPayment, headers=self.header_api,
                                data=json.dumps(data_cr_recive))


class User(BaseParams):

    def login(self, data):
        return requests.request("POST", url=self.url + self.user.login, headers=self.header_jwt,
                                data=json.dumps(data))

    def create_merchant(self, jwt, merch_name):
        return requests.request("POST", url=self.url + self.user.createMerchant, headers=self.jwt_parser(jwt),
                                data=json.dumps(merch_name))

    def putSecret(self, jwt, merchuid):
        return requests.request("POST", url=self.url + self.user.putSecretKey, headers=self.jwt_parser(jwt),
                                data=json.dumps(merchuid))

    def deleteSecretKey(self, jwt, merchuid):
        return requests.request("POST", url=self.url + self.user.deleteSecretKey, headers=self.jwt_parser(jwt),
                                data=json.dumps(merchuid))

    def createOtp(self, jwt):
        return requests.request("POST", url=self.url + self.user.createOtp, headers=self.jwt_parser(jwt))

    def putOtpState(self, jwt, otp_state):
        return requests.request("POST", url=self.url + self.user.putOtpState, headers=self.jwt_parser(jwt),
                                data=json.dumps(otp_state))

    def createApiKey(self, jwt, api_cr):
        return requests.request("POST", url=self.url + self.user.createApiKey, headers=self.jwt_parser(jwt),
                                data=json.dumps(api_cr))

    def get_api_key(self, jwt, api_get):
        return requests.request("GET", url=self.url + self.user.getApiKeys, headers=self.jwt_parser(jwt),
                                params=api_get)

    def deleteApiKey(self, jwt, apikey_id):
        return requests.request("POST", url=self.url + self.user.deleteApiKey, headers=self.jwt_parser(jwt),
                                data=json.dumps(apikey_id))

    def putAssetSettings(self, jwt, asset_settings):
        return requests.request("POST", url=self.url + self.user.putAssetSettings, headers=self.jwt_parser(jwt),
                                data=json.dumps(asset_settings))

    def createPayment(self, jwt, data_payment):
        return requests.request("POST", url=self.url + self.user.createPayment, headers=self.jwt_parser(jwt),
                                data=json.dumps(data_payment))

    def createWithdraw(self, jwt, withdraw_cr):
        return requests.request("POST", url=self.url + self.user.createWithdraw, headers=self.jwt_parser(jwt),
                                data=json.dumps(withdraw_cr))

    def putAssetsList(self, jwt, asset_list):
        return requests.request("POST", url=self.url + self.user.putAssetsList, headers=self.jwt_parser(jwt),
                                data=json.dumps(asset_list))

    def patchApiKey(self, jwt, id):
        return requests.request("POST", url=self.url + self.user.patchApiKey, headers=self.jwt_parser(jwt),
                                data=json.dumps(id))

    def patchMerchantSettings(self, jwt, settings):
        return requests.request("POST", url=self.url + self.user.patchMerchantSettings, headers=self.jwt_parser(jwt),
                                data=json.dumps(settings))

    def createInternalWallet(self, jwt, createinternal):
        return requests.request("POST", url=self.url + self.user.createInternalWallet, headers=self.jwt_parser(jwt),
                                data=json.dumps(createinternal))

    def patchMainInternalWallet(self, jwt, changeinternal):
        return requests.request("POST", url=self.url + self.user.patchMainInternalWallet, headers=self.jwt_parser(jwt),
                                data=json.dumps(changeinternal))

    def repeatFailedWithdraw(self, jwt, faildWdata):
        return requests.request("POST", url=self.url + self.user.repeatFailedWithdraw, headers=self.jwt_parser(jwt),
                                data=json.dumps(faildWdata))

    def cancelWithdraw(self, jwt, cancel):
        return requests.request("POST", url=self.url + self.user.cancelWithdraw, headers=self.jwt_parser(jwt),
                                data=json.dumps(cancel))

    def getTransactions(self, jwt, merchUid):
        return requests.request("GET", url=self.url + self.user.getTransactions, headers=self.jwt_parser(jwt),
                                params=json.dumps(merchUid))

    def getPendings(self, jwt, merchUid):
        return requests.request("GET", url=self.url + self.user.getMerchantPendings, headers=self.jwt_parser(jwt),
                                params=json.dumps(merchUid))

    def getMerchantBalances(self, jwt, merchUid):
        return requests.request("GET", url=self.url + self.user.getMerchantBalances, headers=self.jwt_parser(jwt),
                                params=json.dumps(merchUid))

    def removeWallet(self, jwt, merchuid):
        return requests.request("POST", url=self.url + self.user.removeWallet, headers=self.jwt_parser(jwt),
                                data=json.dumps(merchuid))

    def bulkCreateWithdaws(self,jwt,withdraw_batch):
        return requests.request("POST",url=self.url+self.user.bulkCreateWithdaws,headers=self.jwt_parser(jwt),
                                data=json.dumps(withdraw_batch).encode('utf-8'))

    def putSymbolToAssetsList(self,jwt,asset):
        return requests.request("POST",url=self.url + self.user.putSymbolToAssetsList,headers=self.jwt_parser(jwt),
                                data=json.dumps(asset))

    def deleteSymbolFromAssetsList(self,jwt,asset):
        return requests.request("POST",url=self.url+self.user.deleteSymbolFromAssetsList,headers=self.jwt_parser(jwt),
                                data=json.dumps(asset))

    def deleteMerchant(self,jwt,merchant):
        return requests.request("POST",url=self.url+self.user.deleteMerchant,headers=self.jwt_parser(jwt),
                                data=json.dumps(merchant))

    def change0xWallets(self,jwt,chain):
        return requests.request("POST",url=self.url+self.user.change0xWallets,headers=self.jwt_parser(jwt),
                                data=json.dumps(chain))

    def checkValidation(self,jwt,withdraw_cr):
        return requests.request("POST",url=self.url+self.user.checkWithdrawValidity,headers=self.jwt_parser(jwt),
                                data=json.dumps(withdraw_cr))


class Admin(BaseParams):
    def getUsers(self, jwt):
        return requests.request("GET", url=self.admin_url + self.admin.getUsers, headers=self.jwt_parser(jwt))

    def getUsersEvents(self, jwt):
        return requests.request("GET", url=self.admin_url + self.admin.getUsersEvents, headers=self.jwt_parser(jwt))

    def getAdminGasWallets(self,jwt):
        return requests.request("GET",url=self.admin_url+self.admin.getAdminGasWallets,headers=self.jwt_parser(jwt))

    def getAdminServiceWallets(self,jwt):
        return requests.request("GET",url=self.admin_url+self.admin.getAdminServiceWallets,headers=self.jwt_parser(jwt))

    def getTotalSumPaysAndWds(self,jwt,merchant):
        return requests.request("POST",url=self.admin_url+self.admin.getTotalSumPaysAndWds,headers=self.jwt_parser(jwt),
                                data=json.dumps(merchant))

    def getServiceStat(self,jwt):
        return requests.request("GET",url=self.admin_url+self.admin.getServiceStat,headers=self.jwt_parser(jwt))


class NoneLoginMethods(BaseParams):
    def register(self, register_data):
        return requests.request("POST", url=self.url + self.nonloginendpoint.register,
                                data=json.dumps(register_data))

    def createConfirmEmail(self):
        return requests.request("POST",url=self.url+self.nonloginendpoint.createConfirmEmail)



