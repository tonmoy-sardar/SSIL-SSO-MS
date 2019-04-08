from django.shortcuts import render

from smssend.models import *
from urllib.request import Request, urlopen
import urllib
import json
from django.conf import settings

from django.template import Context,Template

class GlobleSmsSend(object):
    """docstring for ClassName"""
    def __init__(self, code, recipient_list:list):
        super(GlobleSmsSend, self).__init__()
        self.code = code
        self.recipient_list = recipient_list

    def sms_send(self, sms_data:dict):
        print("self.code: ", self.code)
        sms_content = SmsContain.objects.get(code = self.code)
        contain_variable = sms_content.contain_variable.split(",")
        print("contain_variable: ", contain_variable)

        txt_content = Template(sms_content.txt_content)
        match_data_dict = {}
        for data in contain_variable:
            if data.strip() in sms_data:
                match_data_dict[data.strip()] = sms_data[data.strip()]

        if match_data_dict:
            context_data = Context(match_data_dict)
            
            txt_content = txt_content.render(context_data)

        for contact_no in self.recipient_list:
            api_url = settings.SMS_URL+"?username="+ urllib.parse.quote_plus(settings.SMS_USER)+"&password="+ urllib.parse.quote_plus(settings.SMS_PASS)+"&sender="+settings.SMS_SENDER+"&message="+ urllib.parse.quote_plus(txt_content)+"&numbers="+str(contact_no)+"&unicode=false&flash=false"

            req = Request(api_url,headers={'User-Agent': 'Mozilla/5.0'})
            webpage = urlopen(req).read()
            print('webpage: ',webpage.decode('utf-8'))
            json_raw_response = webpage.decode('utf-8')
            json_decode_response = json.loads(json_raw_response)
        
        print("SMS send Done..... ")
        return True

