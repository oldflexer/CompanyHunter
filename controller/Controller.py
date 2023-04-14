from customtkinter import StringVar, BooleanVar


class Controller:
    def __init__(self, repo, view):
        self.repo = repo
        self.view = view
        self.companies = None

        self.full_name = StringVar()
        self.date_reg = StringVar()
        self.region = StringVar()
        self.town = StringVar()
        self.main_okved = StringVar()
        self.additional_okved = StringVar()
        self.status = BooleanVar(value=True)

    def search(self):
        self.companies = list(self.repo.get_companies(archive_index=0, controller=self))
        for company in self.companies:
            # print(company)
            self.view.add_company(company)
