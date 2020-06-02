
class MagicList:

    class ValueMisMatchException(Exception):
        pass

    def __init__(self,cls_type=None):
        self._base_list = list()
        self.cls_type = cls_type

    def _check_key(self, key):
        if key > len(self._base_list):
            raise IndexError("list index out of range")

    def __setitem__(self, key, value):
        self._check_key(key)
        if self.cls_type:
            if not type(value) == self.cls_type:
                raise MagicList.ValueMisMatchException("Cant mix types like that!, stick to {}".format(self.cls_type))
        self._base_list.append(value)

    def __getitem__(self, key):
        self._check_key(key)
        if len(self._base_list) == key:
            if self.cls_type:
                self._base_list.append(self.cls_type())
        return self._base_list[key]

    def __str__(self):
        return str(self._base_list)

if __name__ == "__main__":
    from dataclasses import dataclass

    @dataclass
    class Person:
        age: int = 1

    b = MagicList(cls_type=Person)
    b[0] = Person(2)
    b[1].age = 15

    print(b)