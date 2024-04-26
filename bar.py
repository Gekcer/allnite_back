import json

class Bar:
    all_bars = None

    def __init__(self, name, url):
        self.name = name
        self.url = url

    @classmethod
    def get_all_bars(cls):
        if not cls.all_bars:
            with open('bars.json', 'r', encoding='utf-8') as j:
                all_bars = json.load(j)
        return all_bars

    @classmethod
    def get_all_bar_names(cls):
        names = []
        for bar in cls.get_all_bars():
            names.append(bar['name'])
        return names

    @classmethod
    def get_bars_by_media(cls, media):
        all_bars = Bar.get_all_bars()
        names = []
        for bar in all_bars:
            if bar.get(media):
                names.append(bar)
        return names

    def __str__(self):
        return f'Название: {self.name}\nСсылка: {self.url}'

if __name__ == '__main__':
    bars = Bar.get_bars_by_media('Telegram')
    for bar in bars:
        print(bar)