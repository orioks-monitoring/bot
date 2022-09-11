class AssetsHelper:

    def __init__(self):
        self.__abs_assets_path = None

    def initialize(self, path: str):
        self.__abs_assets_path = path

    def get_assets_path(self):
        return self.__abs_assets_path

    def make_full_path(self, relative_path):
        return f'{self.get_assets_path()}/{relative_path}'


assetsHelper = AssetsHelper()
