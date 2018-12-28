from json import JSONEncoder



class ComplexEncoder(JSONEncoder):


    def default(self, obj):

        from core.database.orm_framework import DBModel

        try:
            if isinstance(obj, DBModel):
                return obj.__dict__
            #elif callable(getattr(obj, "reprJSON")):
            #    return obj.reprJSON()
            #elif isinstance(obj, ActorModel):
            #    return None
            elif hasattr(obj, "callback"):
                return obj()
            else:
                return None
        except TypeError as e:
            pass
        return None
