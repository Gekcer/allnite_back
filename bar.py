import json

class Bar:
    all_bars = None

    def __init__(self, name, url):
        self.name = name
        self.url = url

    @classmethod
    def get_all_bars(cls):
        if not cls.all_bars:
            with open('bars.json', 'r') as j:
                cls.all_bars = json.load(j)
        return cls.all_bars

    @classmethod
    def get_all_bar_names(cls):
        names = []
        for bar in cls.get_all_bars():
            names.append(bar['name'])

    def __str__(self):
        return f'Название: {self.name}\nСсылка: {self.url}'

if __name__ == '__main__':
    print(Bar.get_all_bars())
    print([Bar(x['name'], x['url']) for x in Bar.get_all_bars()])
    bar1 = Bar(1, 2)
    print(bar1)
