class RequestExceptions(Exception):
    '''This class is a custom exceptions class that is uspposed to return pretty messages on anomilies'''
    def __init__(self, message, code):
        self.message = message
        self.code = code
    
    def __str__(self):
        return f"Status code: {self.code}, {self.message}"

class CompanyClientsServer:
    '''This class simulates a server that handles communication with a databse that stores client data for companies'''
    __req_limit = 100
    __curr_req = 89
    _self = None


    def __new__(cls, *args, **kwargs):
        '''Ensure only one instance is initialized at all times'''
        if cls._self is None:
            cls._self = super(CompanyClientsServer,cls).__new__(cls)
        return cls._self

        
    def __init__(self, ip):
        self.ip = ip

        #Some random data structure
        self.data_structure = {
            "_id",
            "client_name",
            "client_Cname",
            "client_domain",
            "client_contract_valid_till"
        }


    def request(self, *args, **kwargs):
        '''This method takes in keyword arguments as url headers for fetching requested data'''
        try: 

            assert self.__curr_req != self.__req_limit #check for too many requests
            self.__curr_req+=1

            if kwargs["method"]=="GET":
                return self.handle_get(kwargs)

        except AssertionError:
            return f"Too many requests, try again later..."
        

    def handle_get(self, kwargs):
        '''Handles get requests to the server and is supposed to return some data'''
        try:
            if not self.url_exists(kwargs["url"], kwargs["method"]):
                raise RequestExceptions("URL does not exist", 404)
            
            if kwargs["url"]=="/get_client_validation_date":
                self.__curr_req-=1
                return self.get_client_validation(kwargs["client_id"])

            if kwargs["url"]=="/get_domains":
                self.__curr_req-=1
                return self.get_domains(kwargs["access_token"])
            

        except RequestExceptions as e:
            self.__curr_req-=1
            return str(e) 
        
        except KeyError as e:
            self.__curr_req-=1
            return str(RequestExceptions(f"BAD_REQUEST: {str(e)} not provided", 400))



    def url_exists(self, url, method):
        '''Checks if the passed in URL exists or not'''
        urls = {
            "GET":[
            "/get_client_validation_date",
            "/get_client",
            "/get_domains"]

            #more methods and urls
            #.....
            #.....
            }
        return url in urls[method]
    

    def get_client_validation(self, client_id):
        '''An example method, returns contract end date for company clients'''
        client_ids = {
            "1op":"2025 Jan 14", 
            "1oq":"2027 Feb 27", 
            "10k":"not decided"
            }
        if client_id not in client_ids:
            raise RequestExceptions("Client not found", 404)
        
        return client_ids[client_id]
    

    def get_domains(self, access_token):
        '''An example method that lists all the domains of the registered companies'''

        #server database storing all the tokens for logged in users
        permissions = {
            "jbvarverbntrn":True,
            "vjcib2opf298fhsb":False,
            "kjvwbf0p91wu":True
        }

        #dummy output for successful fetch
        dummy_domains = ["IT", "Commerce", "Education"]

        if access_token not in permissions:
            raise RequestExceptions("Unauthorized Access", 403)
        
        if not permissions[access_token]:
            raise RequestExceptions("FORBIDDEN_ACCESS: you cannot access this data", 401)
        
        return dummy_domains

        
        
new_server = CompanyClientsServer("mjgcq.qjf.hf")


#Example requests to the server
print(new_server.request(url="/get_domains", method="GET", access_token="jbvarverbntrn"))
print(new_server.request(url="/get_domains", method="GET"))
print(new_server.request(url="/get_domains", method="GET", access_token="vjcib2opf298fhsb"))
print(new_server.request(url="/get_client_validation_date", method="GET", client_id="1op"))
print(new_server.request(url="/get_client_validation_date", method="GET", client_id="10k"))
print(new_server.request(url="/get_client_validation_date", method="GET", client_id="jbiu"))
print(new_server.request(url="/broken_link", method="GET"))