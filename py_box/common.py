class IUnicode:
    @property
    def unicode_name(self):
        pass

    @property
    def unicode_str(self) -> str:
        return u"\\N{{{}}}".format(self.unicode_name).encode().decode('unicode-escape')
