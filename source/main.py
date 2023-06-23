import controller.Controller
import controller.RosprirodnadzorAPI
import model.CompaniesRepository
import view.ApplicationGUI
import logging


def main():
    logging.basicConfig(level=logging.INFO,
                        filename="log/latest.log",
                        filemode="w")
    companies_repo = model.CompaniesRepository.CompaniesRepository()
    application_gui = view.ApplicationGUI.ApplicationGUI()
    control = controller.Controller.Controller(repo=companies_repo, view=application_gui)
    application_gui.set_controller(controller=control)
    application_gui.mainloop()


if __name__ == '__main__':
    main()
