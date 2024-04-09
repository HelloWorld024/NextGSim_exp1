from edge.application_examples.RANAppPublic import RANApplicationPublic
from edge.application_examples.RANAppPublicRadioAware import RANApplicationPublicRadioAware
from edge.application_examples.RANAppPrivate import RANApplicationPrivate
from edge.application_examples.RANAppBlockchainPublic import RANAppBlockchainPublic
from edge.application_examples.RANAppBlockchainPublicRadioAware import RANAppBlockchainPublicRadioAware


def get_app(app_name):
    if app_name == "RANApplicationPublic":
        return RANApplicationPublic
    if app_name == "RANApplicationPublicRadioAware":
        return RANApplicationPublicRadioAware
    if app_name == "RANApplicationPrivate":
        return RANApplicationPrivate
    if app_name == "RANAppBlockchainPublicRadioAware":
        return RANAppBlockchainPublicRadioAware
    if app_name == "RANAppBlockchainPublic":
        return RANAppBlockchainPublic


# def get_service(service_name):
#     if service_name == "Data_Processing_Latency_Aware":
#         return DataProcessingPrivate
#     if service_name == "Data_Processing":
#         return RANAppPublic
