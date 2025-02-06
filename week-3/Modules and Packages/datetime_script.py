import datetime

class datecount():
    def __init__(self, step: str="daily"):
        __step_bank = ('alternative', 'daily',  'weekly', 'monthly', 'quarterly', 'yearly')
        self.step = step.lower()
        if self.step not in __step_bank:
            raise ValueError(f"Valid steps are: {__step_bank}")
        self.curr_date = datetime.date.today()
        
    def __next__(self):
        current_date = self.curr_date
        match self.step:
            case "daily":
                self.curr_date += datetime.timedelta(1)
                return current_date

            case "alternative":
                self.curr_date += datetime.timedelta(2)
                return current_date
            
            case "weekly":
                self.curr_date += datetime.timedelta(weeks=1)
                return current_date

            case "monthly":
                year = self.curr_date.year
                if self.curr_date.month + 1 > 12: year = self.curr_date.year+1

                month = 1 + (self.curr_date.month % 12)

                try: self.curr_date = self.curr_date.replace(year, month)
                except ValueError: self.curr_date = datetime.date(year, month+1, 1) - datetime.timedelta(1) #for next month being feb/aug
                return current_date
            
            case "quarterly":
                year = self.curr_date.year
                if self.curr_date.month + 3 > 12: year = self.curr_date.year+1
                
                month = 1 + (self.curr_date.month-1+3) % 12
                try: self.curr_date = self.curr_date.replace(year, month)
                except ValueError: self.curr_date = datetime.date(year, month+1, 1) - datetime.timedelta(1) #for next month being feb/aug
                return current_date
            
            case "yearly":
                self.curr_date = self.curr_date.replace(year=self.curr_date.year+1)
                return current_date
            
    def __iter__(self):
        return self
    

def datecount1(step):
    curr_date = datetime.date.today()
    while True:
        yield curr_date
        match step:
            case "daily":
                curr_date += datetime.timedelta(1)

            case "alternative":
                curr_date += datetime.timedelta(2)
            
            case "weekly":
                curr_date += datetime.timedelta(weeks=1)

            case "monthly":
                year = curr_date.year
                if curr_date.month + 1 > 12: year = curr_date.year+1

                month = 1 + (curr_date.month % 12)

                try: curr_date = curr_date.replace(year, month)
                except ValueError: curr_date = datetime.date(year, month+1, 1) - datetime.timedelta(1) #for next month being feb/aug
            
            case "quarterly":
                year = curr_date.year
                if curr_date.month + 3 > 12: year = curr_date.year+1
                
                month = 1 + (curr_date.month-1+3) % 12
                try: curr_date = curr_date.replace(year, month)
                except ValueError: curr_date = datetime.date(year, month+1, 1) - datetime.timedelta(1) #for next month being feb/aug
            
            case "yearly":
                curr_date = curr_date.replace(year=curr_date.year+1)

            case _:
                raise ValueError(f"Valid steps are: 'alternative', 'daily',  'weekly', 'monthly', 'quarterly', 'yearly'")
            
if __name__ == "__main__":
    dc1 = datecount1(step="daily")
    for i in range(10):
        print(next(dc1))