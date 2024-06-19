import datetime as dt


class Calculator:

    def __init__(self, limit):

        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):

        today_stats = 0
        format_date = '%d.%m.%Y'
        today = dt.datetime.today()
        for i in self.records:
            date = dt.datetime.strptime(i.date, format_date)
            if today.date() == date.date():
                today_stats += i.amount
        return today_stats

    def get_week_stats(self):
        format_date = '%d.%m.%Y'
        today = dt.datetime.today()
        delta = today - dt.timedelta(days=7)
        week_stats = 0
        for i in self.records:
            date = dt.datetime.strptime(i.date, format_date)

            if delta <= date <= today:
                week_stats += i.amount
        return week_stats


class CaloriesCalculator(Calculator):

    def __init__(self, limit):
        super().__init__(limit)

    def get_calories_remained(self):
        today_stats = self.get_today_stats()
        if today_stats >= self.limit:
            return 'Хватит есть!'
        remains = self.limit - today_stats
        return f'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {remains} кКал'


class CashCalculator(Calculator):

    def __init__(self, limit):
        super().__init__(limit)
        self.usd_rate = 87.04
        self.eur_rate = 93.3

    def get_today_cash_remained(self, currency='rub'):
        today_stats = self.get_today_stats()
        today_limit = self.limit
        if currency == 'usd':
            today_limit = round((today_limit / self.usd_rate), 2)
            today_stats = round((today_stats / self.usd_rate), 2)
        elif currency == 'eur':
            today_limit = round((today_limit / self.eur_rate), 2)
            today_stats = round((today_stats / self.eur_rate), 2)
        if today_limit > today_stats:
            remains = today_limit - today_stats
            return f'На сегодня осталось {remains} {currency}'
        elif today_limit == today_stats:
            return 'Денег нет, держись'
        debt = today_stats - today_limit
        return f'Денег нет, держись: твой долг - {debt} {currency}'


class Record:

    def __init__(self, amount, date=dt.date.today().strftime('%d.%m.%Y'), comment=None):
        self.amount = amount
        self.date = date
        self.comment = comment


# для CashCalculator
r1 = Record(amount=145, comment='Безудержный шопинг', date='13.06.2024')
r2 = Record(amount=1001,
            comment='Наполнение потребительской корзины')
r3 = Record(amount=1, comment='Катание на такси', date='19.06.2024')

# для CaloriesCalculator
r4 = Record(amount=1186,
            comment='Кусок тортика. И ещё один.',
            date='13.06.2024')
r5 = Record(amount=84, comment='Йогурт.')
r6 = Record(amount=1140, comment='Баночка чипсов.', date='19.06.2024')

cash_calculator = CashCalculator(1000)
cash_calculator.add_record(r1)
cash_calculator.add_record(r2)
cash_calculator.add_record(r3)

calories_calculator = CaloriesCalculator(1000)
calories_calculator.add_record(r4)
calories_calculator.add_record(r5)
calories_calculator.add_record(r6)

print(calories_calculator.get_calories_remained())
print(cash_calculator.get_today_cash_remained('rub'))
