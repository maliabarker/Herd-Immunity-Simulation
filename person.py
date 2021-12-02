import random
random.seed(42)
from virus import Virus


class Person(object):
    ''' Person objects will populate the simulation. '''

    def __init__(self, _id, is_vaccinated, infection=None):
        ''' We start out with is_alive = True, because we don't make vampires or zombies.
        All other values will be set by the simulation when it makes each Person object.

        If person is chosen to be infected when the population is created, the simulation
        should instantiate a Virus object and set it as the value
        self.infection. Otherwise, self.infection should be set to None.
        '''
        self._id = _id  # int
        self.is_alive = True  # boolean
        self.is_vaccinated = is_vaccinated  # boolean
        self.infection = infection  # Virus object or None

    def did_survive_infection(self):
        ''' Generate a random number and compare to virus's mortality_rate.
        If random number is smaller, person dies from the disease.
        If Person survives, they become vaccinated and they have no infection.
        Return a boolean value indicating whether they survived the infection.
        '''
        # Only called if infection attribute is not None.
        # TODO:  Finish this method. Should return a Boolean
        assert self.is_vaccinated == False
        assert self.infection != None
        if self.infection != None:
            virus = self.infection
            rand_num = random.random()
            # print(rand_num)
            if rand_num <= virus.mortality_rate:
                self.is_alive = False
                self.infection = None
                return self.is_alive
            else:
                self.is_alive = True
                self.is_vaccinated = True
                self.infection = None
                return self.is_alive


''' These are simple tests to ensure that you are instantiating your Person class correctly. '''
def test_vacc_person_instantiation():
    # create some people to test if our init method works as expected
    vacc_person = Person(1, True)
    assert vacc_person._id == 1
    assert vacc_person.is_alive is True
    assert vacc_person.is_vaccinated is True
    assert vacc_person.infection is None

    person2 = Person(2, True)
    assert person2._id == 2
    assert person2.is_alive is True
    assert person2.is_vaccinated is True
    assert person2.infection is None

    person3 = Person(3, True)
    assert person3._id == 3
    assert person3.is_alive is True
    assert person3.is_vaccinated is True
    assert person3.infection is None


def test_not_vacc_person_instantiation():
    person = Person(2, False)
    # TODO: complete your own assert statements that test
    # the values at each attribute
    assert person._id == 2
    assert person.is_alive == True
    assert person.is_vaccinated == False
    assert person.infection == None


def test_sick_person_instantiation():
    # Create a Virus object to give a Person object an infection
    virus = Virus("Dysentery", 0.7, 0.2)
    # Create a Person object and give them the virus infection
    person = Person(3, False, virus)
    # TODO: complete your own assert statements that test
    # the values at each attribute
    assert person._id == 3
    assert person.is_alive is True
    assert person.is_vaccinated is False
    assert person.infection == virus
    # print(f'did survive: {person.did_survive_infection()}')
    test_did_survive_infection()
    
    covid = Virus("SARS-CoV-2", 0.9, 0.016)
    infected_person = Person(3, False, covid)
    assert infected_person._id == 3
    assert infected_person.is_alive is True
    assert infected_person.is_vaccinated is False
    assert infected_person.infection == covid
    # print(f'did survive: {person.did_survive_infection()}')
    test_did_survive_infection()


def test_did_survive_infection():
    # TODO: Create a Virus object to give a Person object an infection
    virus = Virus("Dysentery", 0.7, 0.2)
    # TODO: Create a Person object and give them the virus infection
    person = Person(4, False, virus)

    # Resolve whether the Person survives the infection or not
    survived = person.did_survive_infection()
    # Check if the Person survived or not
    if survived:
        assert person.is_alive is True
        assert person._id == 4
        assert person.is_vaccinated is True
        assert person.infection is None
        # TODO: Write your own assert statements that test
        # the values of each attribute for a Person who survived
        # assert ...
    else:
        assert person.is_alive is False
        assert person._id == 4
        assert person.is_vaccinated is False
        assert person.infection == virus
        # TODO: Write your own assert statements that test
        # the values of each attribute for a Person who did not survive
        # assert ...

virus = Virus("Dysentery", 0.7, 0.2)
person = Person(3, False, virus)

# print(person.did_survive_infection())
# print(person.did_survive_infection())
# print(person.did_survive_infection())



# print(test_vacc_person_instantiation())
# print(test_not_vacc_person_instantiation())
# print(test_sick_person_instantiation())

# print(f'test: {test_sick_person_instantiation()}')