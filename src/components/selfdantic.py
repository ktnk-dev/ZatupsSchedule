class BaseModel:
    def __init__(self, **kwargs) -> None:
        for key in self.__annotations__.keys():
            if key in kwargs: 
                self.__setattr__(key, kwargs[key])
    
    def model_dump(self):
        return {
            key: self.__getattribute__(key)
            for key in self.__annotations__.keys()
        }
