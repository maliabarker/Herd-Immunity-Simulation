class Virus(object):
    '''Properties and attributes of the virus used in Simulation.'''

    def __init__(self, name, repro_rate, mortality_rate):
        self.name = name
        self.repro_rate = repro_rate
        self.mortality_rate = mortality_rate


def test_virus_instantiation():
    #TODO: Create your own test that models the virus you are working with
    '''Check to make sure that the virus instantiator is working.'''
    virus = Virus("HIV", 0.8, 0.3)
    assert virus.name == "HIV"
    assert virus.repro_rate == 0.8
    assert virus.mortality_rate == 0.3

    covid = Virus("SARS-CoV-2", 0.9, 0.016)
    assert covid.name == "SARS-CoV-2"
    assert covid.repro_rate == 0.9
    assert covid.mortality_rate == 0.016

    ebola = Virus("Ebola", 0.25, 0.7)
    assert ebola.name == "Ebola"
    assert ebola.repro_rate == 0.25
    assert ebola.mortality_rate == 0.7


    # print(virus2.name)
    # print(virus2.repro_rate)



test_virus_instantiation()