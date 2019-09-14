from urllib.parse import urlencode as _urlencode

import requests as _requests
import types as _types
import json as _json
from typing import List as _list
import _thread

from .errors import InvalidCookiesError
from .endpoints import Endpoints as _endpoints
from .endpoints import headers as _headers
from .task import Task as _task
from .task import TaskFilter as _task_filter

class Client:
    def __init__(self,url):
        self.url = url
        self.cookies = {}
        self.filter = _task_filter()
        self.tasks = []

    @property
    def _formated_cookies(self):
        out = []
        for name in self.cookies:
            out.append(name+"="+self.cookies[name])
        return "; ".join(out)

    def _get_tasks(self,page=0):
        self.filter.page = page
        response = _requests.post(
            url=self.url+_endpoints.tasks,
            json=self.filter.json(),
            headers=_headers(self.url,_json.dumps(self.filter.json()),self._formated_cookies)
        )

        for idx,task in enumerate(response.json().get("items",tuple())):
            if len(self.tasks)-1 == (page)*self.filter.page_size+idx+1:
                self.tasks[(page)*self.filter.page_size+idx] = _task.from_json(task)
            else:
                while not len(self.tasks)-1 == (page)*self.filter.page_size+idx+1:
                    self.tasks.append(None)
                self.tasks[(page)*self.filter.page_size+idx] = _task.from_json(task)
        

    
    def set_cookies(self,cookies):
        try:
            for cookie in cookies.replace(" ","").split(";"):
                name, *value = cookie.split("=")
                value = "=".join(value)
                self.cookies[name] = value
        except:
            raise InvalidCookiesError
    
    def update(self,new_thread=False,on_complete=None):
        if new_thread:
            _thread.start_new_thread(self.update,(False,on_complete))
            return
        
        
    


        


