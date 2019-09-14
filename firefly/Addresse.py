from .Person import Person as _person

class Addresse:
    def __init__(self,guid,name,is_group=True):
        if is_group:
            self.guid = guid
            self.name = name
        else:
            self = _person(guid,name)

    @classmethod
    def from_json(self,json,**kwargs):
        addresse_json = json.copy()
        for key in kwargs:
            addresse_json[key] = kwargs[key] # Allow to override
        if addresse_json.get("is_group",False):
            return _person.from_json(addresse_json)
        else:
            return Addresse(
                guid=addresse_json["guid"],
                name=addresse_json["name"]
            )