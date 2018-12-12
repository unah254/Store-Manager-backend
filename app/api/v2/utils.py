import re


class Validators:
    def valid_product_name(self, name):
        '''confirming name input has numbers and letters only'''
        print("validating")
        regex = "^[a-zA-Z0-9_]+$"
        return re.match(regex, name)

    def valid_password(self, password):
        """validate for password """
        print(password)
        return re.search(r'^(?=.{8,}$)[A-Z]+.*(\w+\d+|\d+\w+)$', password)

    def valid_email(self, email):
        """ validate for email """
        return re.search(r"(^[a-zA-Z0-9_.-]+@[a-zA-Z-]+\.[.a-zA-Z-]+$)", email)

    def valid_inputs(self, string_inputs):
        """ validate for inputs """
        return re.match("^[a-zA-Z0-9-\._@ `]+$", string_inputs)
