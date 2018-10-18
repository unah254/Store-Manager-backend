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

    def valid_password(self, password):
        """validate for password """
        return re.match("^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])[a-zA-Z0-9]{8,15}$",
                        password)

    def valid_email(self, email):
        """ validate for email """
        return re.match("^[^@]+@[^@]+\.[^@]+$", email)

    