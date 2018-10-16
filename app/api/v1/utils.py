import re 


class Validators:
    def valid_product_name(self, name):
        '''confirming name input has numbers and letters only'''
        regex = "^[a-zA-Z0-9_ ]+$"
        return re.match(regex, name)


    def valid_product_description(self, description):
        '''confirming description has numbers and letters only'''
        regex = "^[a-zA-Z0-9_ ]+$"
        return re.match(regex, description)
