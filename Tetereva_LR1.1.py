seconds=100000
days=seconds//86400
hours=(seconds-days*86400)//3600
minutes=(seconds-(days*86400+hours*3600))//60
sec=(seconds-(days*86400+hours*3600+minutes*60))
print('В',seconds,'секундах:',days, 'дней', hours,'часов',minutes,'минут',sec,'секунд')