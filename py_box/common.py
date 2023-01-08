class IUnicode:
    @property
    def unicode_name(self):
        pass

    @property
    def unicode_str(self):
        return u"\\N{{{}}}".format(self.unicode_name).encode().decode('unicode-escape')
