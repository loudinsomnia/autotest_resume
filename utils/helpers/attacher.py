import allure


class Attach:
    def allure_attach(self, **kwargs):
        """Attach\n
        :body -- тело переданное в запрос\n
        :status_code -- status code запроса\n
        :response -- response от сервер\n
        :любый дополнительные данные -- ``name=key,body=value``\n"""
        for key, value in kwargs.items():
            if value != '':
                allure.attach(name=f"{key}", body=f"{value}")
            else:
                allure.attach(name=f"{key}", body="No data")