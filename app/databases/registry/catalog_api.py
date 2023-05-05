from typing import Optional
import pandas as pd
import requests

from app.databases.registry.registry_abc import Registry
from app.exceptions import APIResponseFormatException, IdNotExists, APIResponseError


class CatalogueAPI(Registry):

    def check_health(self) -> Optional[str]:
        try:
            self._get_request("https://api.eosc-portal.eu/vocabulary/byType")
        except APIResponseError as e:
            return "Cannot connect with catalogue API"
        return None

    @staticmethod
    def _get_request(request):
        response = requests.get(request)

        if response.status_code == 404:
            return None
        elif response.status_code != 200:
            raise APIResponseError("Error at request in catalogue API!")

        return response.json()

    @staticmethod
    def _reformat_service(service):
        # Get only the leaves for each field with hierarchy levels
        service["scientificDomains"] = [item["scientificSubdomain"] for item in service["scientificDomains"]]
        service["categories"] = [item["subcategory"] for item in service["categories"]]

        # Rename the fields used in metadata to the global naming
        service["scientific_domains"] = service.pop("scientificDomains")
        service["target_users"] = service.pop("targetUsers")

        return service

    # TODO change to one call
    def get_services_by_ids(self, ids, attributes=None, remove_generic_attributes=False):
        services = []
        for id in ids:
            service = self._get_request(f"https://api.eosc-portal.eu/resource/{id}?catalogue_id=eosc")
            if service is None:
                raise IdNotExists(f"Service id {id} does not exist!")
            services.append(self._reformat_service(service))

        if len(services):
            services_df = pd.DataFrame(services)
            services_df.rename(columns={'id': 'service_id'}, inplace=True)
            services_df = services_df[["service_id"] + attributes]
        else:
            services_df = pd.DataFrame(columns=["service_id"] + attributes)

        if remove_generic_attributes:
            self._remove_general_attributes_from_services(services_df)

        return services_df

    def get_services(self, attributes=None, reformat=True):
        """
        Args:
            attributes: list, the requested attributes for the services
            reformat: boolean, when true services attributes are reformated to be independent of the selected registry
        """
        if attributes is None:
            attributes = []

        # TODO currently we have hardcoded 800 as maximum quantity
        response = self._get_request("https://api.eosc-portal.eu/service/all?catalogue_id=eosc&quantity=800")

        try:
            if reformat:
                services = [self._reformat_service(service) for service in response["results"]]
            else:
                services = response["results"]
        except KeyError as e:
            raise APIResponseFormatException(f"{e} does not exist in the response's fields")

        if len(services):
            services_df = pd.DataFrame(services)
            services_df.rename(columns={'id': 'service_id'}, inplace=True)
            services_df = services_df[list(set(["service_id"] + attributes))]
        else:  # If there are no services
            services_df = pd.DataFrame(columns=list(set(["service_id"] + attributes)))

        self._remove_general_attributes_from_services(services_df)

        return services_df

    def get_service(self, service_id, reformat=True, remove_generic_attributes=True):
        service = self._get_request(f"https://api.eosc-portal.eu/resource/{service_id}?catalogue_id=eosc")

        if service is None:
            raise IdNotExists(f"Service id {service_id} does not exist!")

        if reformat:
            service = self._reformat_service(service)

        if remove_generic_attributes:
            self._remove_general_attributes_from_single_service(service)
        return service

    def get_scientific_domains(self):
        return [item["id"] for item in self._get_request("https://api.eosc-portal.eu/vocabulary/byType/SCIENTIFIC_SUBDOMAIN")]

    def get_categories(self):
        return [item["id"] for item in self._get_request("https://api.eosc-portal.eu/vocabulary/byType/SUBCATEGORY")]

    def get_target_users(self):
        return [item["id"] for item in self._get_request("https://api.eosc-portal.eu/vocabulary/byType/TARGET_USER")]

    def _remove_general_attributes_from_services(self, services):
        attributes = ['scientific_domains', 'categories', 'target_users']

        def remove_fields_containing_other(attribute_values):
            return [attr for attr in attribute_values if '-other' not in attr]

        for attribute in attributes:
            if attribute in services:
                services[attribute] = services[attribute].apply(remove_fields_containing_other)

    def _remove_general_attributes_from_single_service(self, service):
        attributes = ['scientific_domains', 'categories', 'target_users']

        for attribute in attributes:
            if attribute in service:
                service[attribute] = [attr for attr in service[attribute] if '-other' not in attr]

    def is_valid_service(self, service_id):
        return self.get_service(service_id) is not None