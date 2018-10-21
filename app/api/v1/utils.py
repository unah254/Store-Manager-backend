import re 


class Validators:
    def valid_product_name(self, name):
        '''confirming name input has numbers and letters only'''
        regex = "^[a-zA-Z0-9_ ]+$"
        return re.match(regex, name)


    # def valid_product_description(self, description):
    #     '''confirming description has numbers and letters only'''
    #     regex = "^[a-zA-Z0-9_ ]+$"
    #     return re.match(regex, description)

    def valid_password(self, password):
        """validate for password """
        regex = "^[a-zA-Z0-9_ ]+$"
        return re.match(regex,password)

    def valid_email(self, email):
        """ validate for email """
        return re.match("^[^@]+@[^@]+[^@]+$", email)

    def valid_is_admin(self, is_admin):
        """ validate is_admin """
        return re.match("^[0-1]{,1}$", is_admin)

    def valid_price(self, price):
        """ validate price """
        return re.match("^[0-9]{3,6}$", price)
    
    def valid_inputs(self, string_inputs):
        """ validate for inputs """
        return re.match("^[a-zA-Z0-9-\._@ ]+$", string_inputs)