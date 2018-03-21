#!/usr/bin/env python

__author__ = "Mitch Dawson"
__email__ = "info@ucdevops.com"

import requests

# Define our request headers
header = {
    "Content-Type": "application/x-www-form-urlencoded"
}

# Define our individual cucm extension mobility hosts
host = "https://cucm1"
# Define our extension mobility api url
em_url = ":8443/emservice/EMServiceServlet"
# Define our extension mobility proxy user credentials
# The accouunt needs the "Standard EM Authentication Proxy Rights" role applied
proxy_user = "username"
proxy_pass = "password"


class Login:

    def __init__(self, url, proxy_user, proxy_password):
        self.url = url
        self.proxy_user = proxy_user
        self.proxy_pass = proxy_password
        
    def login_msg(self, mac, profile, uid):
        # The function creates our message, required to perform a login request
        # Takes the Phone MAC, Device Profile Name and userid as input
        return """
        <request>
            <appInfo>
                <appID>{0}</appID>
                <appCertificate>{1}</appCertificate>
            </appInfo>
            <login>
                <deviceName>{2}</deviceName>
                <userID>{3}</userID>
                <deviceProfile>{4}</deviceProfile>
                <exclusiveDuration>
                    <indefinite></indefinite>
                </exclusiveDuration>
            </login>
        </request>
        """.format(self.proxy_user, self.proxy_pass, mac, uid, profile)
        
    def make_request(self, message):
        # The function posts our message to Extension Mobility API
        return requests.post(
            data={"xml": message},
            url=self.url
        )
        
    def do_login(self, mac, profile, uid):
        # Function which carries out our required steps to perform our login
        print("*" * 50, "\n")
        print(
            "Logging in User '{}' into Handset {} "
            "with Profile {} .....\n"
            .format(uid, mac, profile)
        )
        print(
            self.make_request(
                self.login_msg(mac, profile, uid)
            ).text
        )
        print("*" * 50, "\n")
        
def main():
    # Open and read our csv input file
    data = open("login.csv", "r").read().split("\n")
    # Instantiate our "Login" class
    login = Login(
        host + em_url, proxy_user, proxy_pass
    )
    # Loop through our login data, skipping our header line
    for line in data[1:]:
        mac, profile, uid = line.split(",")
        login.do_login(mac, profile, uid)
        
if __name__ == "__main__":
    main()
