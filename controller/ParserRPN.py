import logging
import requests
import json


class ParserRPN:
    def __init__(self):
        try:
            self.logger = logging.getLogger(__name__)
            self.logger.info("init started")
            self.request_url = None
            self.payload = None
            self.logger.info("init successfully completed")
        except Exception as exception:
            self.logger.exception(exception)

    def parse_RPN(self, company):
        try:
            self.logger.info("parse_RPN started")
            self.request_url = "https://license.rpn.gov.ru/api/svc/license-activity-waste/registry/open?"
            self.payload = {"relations": "nsi_status,merging_license,territory_org",
                            "per_page": "20",
                            "page": "1",
                            "order_by[issuer_order_at]": "desc",
                            "scope[OrderByIssuerOrderAtIssuedAt]": "1",
                            "filter[status]": "active",
                            "filter[inn]": f"{company.inn}"}
            response = requests.get(url=self.request_url, params=self.payload)
            response_dict = json.loads(response.text)
            self.logger.info("parse_RPN successfully completed")
            return response_dict
        except Exception as exception:
            self.logger.exception(exception)
