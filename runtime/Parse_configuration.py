# importing the Python modules
from termcolor import colored
from runtime.Scenarios import *
import json
import os


class SimulationParameters(object):
    def __init__(self, simulation, ConfigFile=True, ConfigFileName='config_test.json'):
        self.simulation = simulation
        self.SimParams = None
        self.config_file = ConfigFileName
        if ConfigFile:
            self.ConfigFileName = ConfigFileName
            self.parse_ConfigFile()
        else:
            return

    def parse_ConfigFile(self):
        # path = os.chdir(os.pardir + '/configuration')
        #  read file
        with open('configuration/'+self.ConfigFileName, 'r') as myfile:
            data = myfile.read()
        #  parse file
        config = json.loads(data)
        print(colored(f"***** New config {config} *****", 'green'))
        # self.SimulationParameters.disable_print = sim_params['disable_printing']
        self.num_TTI = config['simulation_time']
        if config['scenario'] == 'indoor':
            self.scenario = Indoor()
        elif config['scenario'] == 'outdoor':
            self.scenario = Outdoor()
        elif config['scenario'] == 'indoor office':
            self.scenario = IndoorOffice()
        elif config['scenario'] == 'indoor factory SL':
            self.scenario = IndoorFactorySL()
        elif config['scenario'] == 'indoor factory DL':
            self.scenario = IndoorFactoryDL()
        elif config['scenario'] == 'indoor factory SH':
            self.scenario = IndoorFactorySH()
        elif config['scenario'] == 'indoor factory DH':
            self.scenario = IndoorFactoryDH()
        self.num_cells = config['num_of_bs']
        self.scenario.max_num_devices_per_scenario = config['num_of_users']
        self.communication_type = config['communication_type']
        self.channel_measurement_granularity = config['scheduling_granularity']
        self.traffic_model = config['consider_traffic_models']
        self.with_mobility = config['consider_mobility']
        self.scheduler_type = config['scheduler_type']
        self.service_placement_algorithm = config['service_placement_algorithm']
        self.service_replacement_algorithm = config['service_replacement_algorithm']


