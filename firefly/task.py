from typing import Dict as _dict
from typing import List as _list
from typing import Any as _any

from datetime import datetime as _datetime
from urllib.parse import quote_plus as _quote_plus
import requests as _requests
import re as _re
import json as _json

from .endpoints import headers as _headers
from .endpoints import Endpoints as _endpoints
from .Person import Person as _person
from .Addresse import Addresse as _addresse
from .Mark import Mark as _mark

class Task:
    def _set_flags(self,excused,done,read,archived,resubmission_required,file_submission_required,file_submission_enabled,description_contains_questions):
        """Set flags of task
        
        Arguments:
            excused {bool} -- Is the task excused by the setter
            done {bool} -- Is the task done
            read {bool} -- Is the task read
            archived {bool} -- Is the task archived
            resubmission_required {bool} -- Is resubmission required
            file_submission_required {bool} -- Is file submission required
            file_submission_enabled {bool} -- Is file submission enabled
            description_contains_questions {bool} -- Does description contain questions
        """
        self.excused = excused
        self.done = done
        self.read = read
        self.archived = archived
        self.resubmission_required = resubmission_required
        self.file_submission_required = file_submission_required
        self.file_submission_enabled = file_submission_enabled
        self.description_contains_questions = description_contains_questions

    @classmethod
    def _from_json(self,client,json,**kwargs):
        """Make Task from JSON
        
        Arguments:
            client {Client} -- The client being used
            json {dict[str,any]} -- The JSON to use
        
        Returns:
            Task -- The task
        """
        task_json = {**json.copy(), **kwargs}  # Allows to override elements in the JSON
        
        return Task(
            client=client,
            Id=task_json["id"],
            title=task_json["title"],
            setter=_person.from_json(task_json["setter"]),
            student=_person.from_json(task_json["student"]),
            addressees=[_addresse.from_json(addresse) for addresse in task_json["addressees"]],
            set_date=_datetime(
                year=int(task_json["setDate"][:4]),
                month=int(task_json["setDate"][5:7]),
                day=int(task_json["setDate"][8:])
            ),
            due_date=_datetime(
                year=int(task_json["dueDate"][:4]),
                month=int(task_json["dueDate"][5:7]),
                day=int(task_json["dueDate"][8:])
            ),
            mark=_mark.from_json(task_json["mark"]),
            last_marked_as_done_by=_person.from_json(task_json["lastMarkedAsDoneBy"]),
            excused=task_json.get("isExcused",False),
            done=task_json.get("isDone",False),
            read=not task_json.get("isUnread",False),
            archived=task_json.get("archived",False),
            resubmission_required=task_json.get("isResubmissionRequired",False),
            file_submission_required=task_json.get("fileResubmissionRequired",False),
            file_submission_enabled=task_json.get("hasFileSubmission",False),
            description_contains_questions=task_json.get("descriptionContainsQuestions",False)
        )

    def _set_done(self,value):
        """Set task as done or undone
        
        Arguments:
            value {bool} -- Done [True] or undone [False]
        """
        url = self.client.url+_endpoints.responses.format(task_id=self.id)
        data = "data="+_quote_plus(_json.dumps({
            "recipient": {
                "type": "user",
                "guid": self.student.guid
            },
            "event": {
                "type": {True:"mark-as-done",False:"mark-as-undone"}[value],
                "feedback": "",
                "sent": _datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                "author": self.student.guid
            }
        }).replace(" ",""))
        headers = {
            **_headers(url,content=data,cookies=self.client._formated_cookies,content_type="x-www-form-urlencoded; charset=UTF-8",accept="*/*"),
            "X-Requested-With": "XMLHttpRequest"
        }
        status_code = _requests.post(url,data=data,headers=headers).status_code
        if status_code < 300 and status_code >= 200:
            self.done = value
        

    
    def __init__(self,
                client,Id,title,setter,student,addressees,due_date,
                set_date=_datetime.now(),
                mark=_mark.none(),
                last_marked_as_done_by=_person.none(),
                excused=False,
                done=False,
                read=False,
                archived=False,
                resubmission_required=False,
                file_submission_required=False,
                file_submission_enabled=True,
                description_contains_questions=False):
        
        self.client = client
        self.id = Id
        self.title = title
        self.setter = setter
        self.student = student
        self.addressees = addressees
        self.set_date = set_date
        self.due_date = due_date
        self.mark = mark

        self._description = None

        self._set_flags(excused,done,read,archived,resubmission_required,file_submission_required,file_submission_enabled,description_contains_questions)


    @property
    def description(self):
        # HACK -- Currently it retreives description from HTML. Try to find an endpoint for getting the description, if possible
        if self._description == None:
            url = self.client.url+_endpoints.task.format(task_id=self.id)
            headers = _headers(url,content="",cookies=self.client._formated_cookies)
            page = _requests.get(url,headers=headers).content.decode("utf-8").replace("\n","<br/>").replace("\\r\\n","<br/>")
            description_html = _re.findall("ffComponent[^>]*>(((?!</div>).)*)(?=</div>)",page)[0][0]
            description = _re.sub("<((?!br)[^>])*>","",description_html)
            description = description.replace("&amp;nbsp;","").replace("<br/>","\n").replace("<br>","\n").replace("\\&quot;","\"")
            self._description = description
        return self._description

    @property
    def personal(self):
        return self.setter == self.student

    
    
    def update_description(self):
        """Update the description from firefly
        
        Returns:
            string -- The updated description
        """
        self._description = None
        return self.description
    
    def toggle_done(self):
        self._set_done(not self.done)

    def mark_done(self):
        self._set_done(True)

    def mark_undone(self):
        self._set_done(False)

    def send_comment(self,message):
        """Set task as done or undone
        
        Arguments:
            message {str} -- Message to send
        """
        url = self.client.url+_endpoints.responses.format(task_id=self.id)
        data = "data="+_quote_plus(_json.dumps({
            "recipient": {
                "type": "user",
                "guid": self.student.guid
            },
            "event": {
                "type": "comment",
                "message": message,
                "feedback": "",
                "sent": _datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                "author": self.student.guid
            }
        }).replace(" ",""))
        headers = {
            **_headers(url,content=data,cookies=self.client._formated_cookies,content_type="x-www-form-urlencoded; charset=UTF-8",accept="*/*"),
            "X-Requested-With": "XMLHttpRequest"
        }
        _requests.post(url,data=data,headers=headers)
        


class TaskFilter:
    class OwnerType:
        ONLY_SETTERS = "OnlySetters"

    class ArchiveStatus:
        ALL = "All"

    class CompletionStatus:
        ALL = "All"
        ALL_INCLUDING_ARCHIVED = "AllIncludingArchived"
        TO_DO = "Todo"
        DONE = "Done"
        DONE_OR_ARCHIVED = "DoneOrArchived"

    class ReadStatus:
        ALL = "All"
        READ = "OnlyRead"
        UNREAD = "OnlyUnread"

    class MarkingStatus:
        ALL = "All"
        MARKED = "OnlyMarked"
        UNMARKED = "OnlyUnmarked"

    class Sorting:
        class Column:
            DUE_DATE = "DueDate"
            SET_DATE = "SetDate"

        class Order:
            ASCENDING = "Ascending"
            DESCENDING = "Descending"
        
        def __init__(self,column=Column.DUE_DATE,order=Order.ASCENDING):
            self.column = column
            self.order = order

    def __init__(self,
            page=0,
            page_size=10,
            owner_type=OwnerType.ONLY_SETTERS,
            archive_status=ArchiveStatus.ALL,
            completion_status=CompletionStatus.ALL_INCLUDING_ARCHIVED,
            read_status=ReadStatus.ALL,
            marking_status=MarkingStatus.ALL,
            sorting=Sorting()):
        
        self.page = page
        self.page_size = page_size
        self.owner_type = owner_type
        self.archive_status = archive_status
        self.completion_status = completion_status
        self.read_status = read_status
        self.marking_status = marking_status
        self.sorting = sorting
    
    def json(self):
        return {
            "ownerType": self.owner_type,
            "page": self.page,
            "pageSize": self.page_size,
            "archiveStatus": self.archive_status,
            "completionStatus": self.completion_status,
            "readStatus": self.read_status,
            "markingStatus": self.marking_status,
            "sortingCriteria":[{
                "column": self.sorting.column,
                "order": self.sorting.order
            }]
        }

