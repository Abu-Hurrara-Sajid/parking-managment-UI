
class Me:
    def __init__(self, name, cast):
        self.name = name
        self.cast = cast

# s = Me('hurrara', "Mayo Rajpoot")
# print(s.name, s.cast)


class course(Me):
    def __init__(self,course,Id):
        self.course=course
        self.Id=Id


c=course("Ideolody",5)
print(c.course,c.Id)
