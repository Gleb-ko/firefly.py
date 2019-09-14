from typing import Dict as _dict
from typing import List as _list
from typing import Any as _any

from datetime import datetime as _datetime

from .Person import Person as _person
from .Addresse import Addresse as _addresse
from .Mark import Mark as _mark

class Task:
    def __init__(self,
                Id,title,setter,student,addressees,due_date,
                set_date=_datetime.now(),
                mark=_mark.none(),
                last_marked_as_done_by=_person.none(),
                personal=False,
                excused=False,
                done=False,
                read=False,
                archived=False,
                resubmission_required=False,
                file_submission_required=False,
                file_submission_enabled=True,
                description_contains_questions=False):
        
        self.id = Id
        self.title = title
        self.setter = setter
        self.student = student
        self.addressees = addressees
        self.set_date = set_date
        self.due_date = due_date
        self.mark = mark

        self._set_flags(personal,excused,done,read,archived,resubmission_required,file_submission_required,file_submission_enabled,description_contains_questions)
        
    def _set_flags(self,personal,excused,done,read,archived,resubmission_required,file_submission_required,file_submission_enabled,description_contains_questions):
        self.personal = personal
        self.excused = excused
        self.done = done
        self.read = read
        self.archived = archived
        self.resubmission_required = resubmission_required
        self.file_submission_required = file_submission_required
        self.file_submission_enabled = file_submission_enabled
        self.description_contains_questions = description_contains_questions

    @classmethod
    def from_json(self,json:_dict[str,_any],**kwargs):
        task_json = json.copy()
        for key in kwargs:
            task_json[key] = kwargs[key] # Allows to override elements in the JSON
        
        return Task(
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
            personal=task_json.get("isPersonalTask",False),
            excused=task_json.get("isExcused",False),
            done=task_json.get("isDone",False),
            read=not task_json.get("isUnread",False),
            archived=task_json.get("archived",False),
            resubmission_required=task_json.get("isResubmissionRequired",False),
            file_submission_required=task_json.get("fileResubmissionRequired",False),
            file_submission_enabled=task_json.get("hasFileSubmission",False),
            description_contains_questions=task_json.get("descriptionContainsQuestions",False)
        )

        


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

