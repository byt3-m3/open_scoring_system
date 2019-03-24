import requests
import scrapy


class LoginSpider(scrapy.Spider):
    name = 'login-spider'
    login_url = 'http://192.168.1.103/action/admin/login'
    start_urls = [login_url]

    def parse(self, response):
        token = response.css('input[name="ossn_token"]::attr(value)').extract_first()

        data = {
            "ossn_token": token,
            "username": "cbaxter",
            "password": "pimpin12"
        }

        yield scrapy.FormRequest(url="http://192.168.1.103/action/admin/login", formdata=data, callback=self.parse())


data = requests.get("http://192.168.1.103/action/admin/login")

admin_creds = {"username": "cbaxter", "password": "pimpin12"}

token = requests.post("http://192.168.1.103/action/admin/login", data=admin_creds)
# action="http://192.168.1.103/action/admin/login"
raw_data = token.content.decode()
