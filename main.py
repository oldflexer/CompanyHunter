import controller.Controller
import controller.ParserRPN
import model.CompaniesRepository
import view.ApplicationGUI
import logging
import threading


def main():
    logging.basicConfig(level=logging.INFO,
                        filename=f"log/latest.log",
                        filemode="w")
    companies_repo = model.CompaniesRepository.CompaniesRepository()
    application_gui = view.ApplicationGUI.ApplicationGUI()
    control = controller.Controller.Controller(repo=companies_repo, view=application_gui)
    application_gui.set_ctrl(ctrl=control)
    application_gui.mainloop()


if __name__ == '__main__':
    main()
