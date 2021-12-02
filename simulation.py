import random, sys
random.seed(42)
from person import Person
from logger import Logger
from virus import Virus


class Simulation(object):
    ''' Main class that will run the herd immunity simulation program.
    Expects initialization parameters passed as command line arguments when file is run.

    Simulates the spread of a virus through a given population.  The percentage of the
    population that are vaccinated, the size of the population, and the amount of initially
    infected people in a population are all variables that can be set when the program is run.
    '''

    def __init__(self, pop_size, vacc_percentage, initial_infected, virus):
        ''' Logger object logger records all events during the simulation.
        Population represents all Persons in the population.
        The next_person_id is the next available id for all created Persons,
        and should have a unique _id value.
        The vaccination percentage represents the total percentage of population
        vaccinated at the start of the simulation.
        You will need to keep track of the number of people currently infected with the disease.
        The total infected people is the running total that have been infected since the
        simulation began, including the currently infected people who died.
        You will also need to keep track of the number of people that have died as a result
        of the infection.

        All arguments will be passed as command-line arguments when the file is run.
        HINT: Look in the if __name__ == "__main__" function at the bottom.
        '''
        # TODO: Create a Logger object and bind it to self.logger.
        # Remember to call the appropriate logger method in the corresponding parts of the simulation.
        # TODO: Call self._create_population() and pass in the correct parameters.
        # Store the array that this method will return in the self.population attribute.
        # TODO: Store each newly infected person's ID in newly_infected attribute.
        # At the end of each time step, call self._infect_newly_infected()
        # and then reset .newly_infected back to an empty list.

        self.next_person_id = 0 # Int to iterate and store unique person id
        self.vacc_percentage = vacc_percentage # float between 0 and 1
        self.virus = virus # Virus object
        
        self.initial_infected = initial_infected # Int
        self.total_infected = 0 # Int
        self.current_infected = 0 # Int
        self.newly_infected = []

        self.current_dead = 0
        self.total_dead = 0 # Int

        self.population = [] # List of Person objects, holds population after create_population is called
        self.pop_size = pop_size # Int amnt of population for create_population function
        self._create_population(self.initial_infected)

        self.file_name = "{}_simulation_pop_{}_vp_{}_infected_{}.txt".format(
            virus_name, pop_size, vacc_percentage, initial_infected)
        self.logger = Logger(self.file_name)
        
        

    def _create_population(self, initial_infected):
        '''This method will create the initial population.
            Args:
                initial_infected (int): The number of infected people that the simulation
                will begin with.

            Returns:
                list: A list of Person objects.

        '''
        # TODO: Finish this method!  This method should be called when the simulation
        # begins, to create the population that will be used. This method should return
        # an array filled with Person objects that matches the specifications of the
        # simulation (correct number of people in the population, correct percentage of
        # people vaccinated, correct number of initially infected people).

        # Use the attributes created in the init method to create a population that has
        # the correct intial vaccination percentage and initial infected.
        while self.next_person_id in range (0, int(self.pop_size)):
            """Vaccinated People"""
            # print(int(self.pop_size * self.vacc_percentage))
            for self.next_person_id in range(0, int(self.pop_size * self.vacc_percentage)):
                self.population.append(Person(self.next_person_id, True, None))
                self.next_person_id += 1
            # for testing purposes
            vaccinated = len(self.population)
            print(f'vaccinated people:{vaccinated}')
            """Infected People"""
            for self.next_person_id in range (0, int(initial_infected)):
                self.population.append(Person(self.next_person_id, False, self.virus))
                self.current_infected += 1
                self.next_person_id += 1
            # for testing purposes
            infected = len(self.population) - vaccinated
            print(f'infected people:{infected}')
            """Unvaccinated, Uninfected People"""
            for self.next_person_id in range(len(self.population), int(self.pop_size)):
                self.population.append(Person(self.next_person_id, False, None))
                self.next_person_id += 1
            # for testing purposes
            others = vaccinated + infected
            unvacc = len(self.population) - others
            print(f'unvaccinated uninfected people:{unvacc}')
        # print(len(self.population))
        return self.population

    def _simulation_should_continue(self):
        ''' The simulation should only end if the entire population is dead
        or everyone is vaccinated.

            Returns:
                bool: True for simulation should continue, False if it should end.
        '''
        # TODO: Complete this helper method.  Returns a Boolean.
        print(self.total_dead)
        if self.total_dead >= self.pop_size:
            print('everyone died')
            return False

        for person in self.population:
            # print(person)
            if person.is_alive == True and person.is_vaccinated != True:
                assert person.is_alive == True
                assert person.is_vaccinated == False
                return True
                # # print(f'{person} is alive')
                # if person.is_vaccinated == True:
                #     assert person.is_vaccinated == True
                #     # print('vaccinated')
                #     continue
                # else:
                #     assert person.is_vaccinated == False
                #     # print('unvacc :(')
                #     return True
        print('everyone vaccinated')
        return False

    def run(self):
        ''' This method should run the simulation until all requirements for ending
        the simulation are met.
        '''
        # TODO: Finish this method.  To simplify the logic here, use the helper method
        # _simulation_should_continue() to tell us whether or not we should continue
        # the simulation and run at least 1 more time_step.

        # TODO: Keep track of the number of time steps that have passed.
        # HINT: You may want to call the logger's log_time_step() method at the end of each time step.
        # TODO: Set this variable using a helper
        time_step_counter = 0
        should_continue = True
        self.logger.write_metadata(self.pop_size, self.vacc_percentage, self.virus.name, self.virus.mortality_rate, self.virus.repro_rate, self.initial_infected)
        # print('running')
        while should_continue:
            print('continuing')
            print(len(self.population))
            # TODO: for every iteration of this loop, call self.time_step() to compute another
            # round of this simulation.
            self.time_step()
            self._infect_newly_infected()

            time_step_counter += 1
            self.logger.log_time_step(time_step_counter, len(self.newly_infected), 0, self.total_infected, self.total_dead)
            self._simulation_should_continue()
            
            if self._simulation_should_continue() == False:
                print(f"The simulation has ended after {time_step_counter} turns.")
                return False

    def time_step(self):
        ''' This method should contain all the logic for computing one time step
        in the simulation.
        
        This includes:
            1. 100 total interactions with a random person for each infected person
                in the population
            2. If the person is dead, grab another random person from the population.
                Since we don't interact with dead people, this does not count as an interaction.
            3. Otherwise call simulation.interaction(person, random_person) and
                increment interaction counter by 1.
            '''
        # TODO: Finish this method.
        print('started')
        i = 0
        # print(self.current_infected)
        for person in self.population:
            if person.infection == self.virus and person.is_alive == True:
                while i < 100:
                    random_person = random.choice(self.population)
                    # print(random_person)
                    if random_person.is_alive == True:
                        # print('interaction okay')
                        self.interaction(person, random_person)
                        i += 1
                    else:
                        print('person dead')
                        continue       
                i = 0     

        for person in self.population:
            if person.infection == self.virus and person.is_alive == True:
                if person.did_survive_infection == True:
                    print('survived infection')
                    # print(person.did_survive_infection)
                    self.logger.log_infection_survival(person, False)
                else:
                    # print('did not survive infection')
                    # print(person.did_survive_infection)
                    self.logger.log_infection_survival(person, True)
                    self.total_dead += 1
                    print(f'total dead: {self.total_dead}')

    def interaction(self, person, random_person):
        '''This method should be called any time two living people are selected for an
        interaction. It assumes that only living people are passed in as parameters.

        Args:
            person1 (person): The initial infected person
            random_person (person): The person that person1 interacts with.
        '''
        # Assert statements are included to make sure that only living people are passed
        # in as params
        assert person.is_alive == True
        assert random_person.is_alive == True

        # TODO: Finish this method.
        #  The possible cases you'll need to cover are listed below:
            # random_person is vaccinated:
            #     nothing happens to random person.
            # random_person is already infected:
            #     nothing happens to random person.
            # random_person is healthy, but unvaccinated:
            #     generate a random number between 0 and 1.  If that number is smaller
            #     than repro_rate, random_person's ID should be appended to
            #     Simulation object's newly_infected array, so that their .infected
            #     attribute can be changed to True at the end of the time step.
        # TODO: Call logger method during this method.
        if random_person.is_vaccinated == True:
            self.logger.log_interaction(person, random_person, False, True, False)
            
        elif random_person.infection != None:
            self.logger.log_interaction(person, random_person, True, False, False)
            
        else:
            num = random.random()
            # print(num)
            # print(self.virus.repro_rate)
            if num <= self.virus.repro_rate:
                # print('infected')
                self.newly_infected.append(random_person._id)
                self.total_infected += 1
                self.current_infected += 1
                self.logger.log_interaction(person, random_person, True, False, True)
                
            else:
                self.logger.log_interaction(person, random_person, False, False, False)
                # print('no infection!')
                
                
    def _infect_newly_infected(self):
        ''' This method should iterate through the list of ._id stored in self.newly_infected
        and update each Person object with the disease. '''
        # TODO: Call this method at the end of every time step and infect each 
        # TODO: Once you have iterated through the entire list of self.newly_infected, remember
        # to reset self.newly_infected back to an empty list.
        print(f'newly infected: {len(self.newly_infected)}')
        
        for person in self.population:
            for id in self.newly_infected:
                print(id)
                if id == person._id:
                    print('new infection')
                    person.infection = self.virus
                    self.current_infected += 1
        self.newly_infected = []

        


if __name__ == "__main__":
    params = sys.argv[1:]
    virus_name = str(params[0])
    repro_num = float(params[1])
    mortality_rate = float(params[2])

    pop_size = int(params[3])
    vacc_percentage = float(params[4])

    if len(params) == 6:
        print('beep')
        initial_infected = int(params[5])
    else:
        print('boop')
        initial_infected = 1

    virus = Virus(virus_name, repro_num, mortality_rate)
    """Testing Attribues"""
    # print(virus_name)
    # print(repro_num)
    # print(mortality_rate)
    # print(pop_size)
    # print(vacc_percentage)
    # print(initial_infected)
    # print(virus)
    sim = Simulation(pop_size, vacc_percentage, initial_infected, virus)


    # sim.time_step()

    # print(sim.vacc_percentage)
    
    """Testing simulation should continue: WORKS!"""
    # sim._create_population(sim.initial_infected)
    # print(sim._simulation_should_continue())


    sim.run()
