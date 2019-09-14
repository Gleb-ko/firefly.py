class Mark:
    def __init__(self,marked,grade,mark,mark_max,has_feedback):
        self.marked = marked
        self.grade = grade
        self.mark = mark
        self.mark_max = mark_max
        self.has_feedback = has_feedback

    @classmethod
    def from_json(self,json,**kwargs):
        """Make Mark class from JSON
        
        Arguments:
            json {dict} -- JSON of the mark
            kwargs {dict} -- To override the JSON
        
        Returns:
            Mark -- A Mark type from the JSON
        """
        mark_json = json.copy()
        for key in kwargs:
            mark_json[key] = kwargs[key] # Allow to override
        return Mark(
            marked=mark_json["isMarked"],
            grade=mark_json["grade"],
            mark=mark_json["mark"],
            mark_max=mark_json["markMax"],
            has_feedback=mark_json["hasFeedback"]
        )

    @classmethod
    def none(self):
        """Returns a blank mark. (Not set)
        
        Returns:
            Mark -- An empty Mark type
        """
        return Mark(
            marked=False,
            grade=None,
            mark=None,
            mark_max=None,
            has_feedback=False
        )