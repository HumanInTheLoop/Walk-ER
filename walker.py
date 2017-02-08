import json
import sys
import os
from collections import OrderedDict
from pygame.locals import *

'''
TODO:
- SQL Table Conversion (may or may not be possible)
'''

class InputException(Exception):
    def handle(self):
        print self.message

class InvalidArgumentException(Exception):
    def handle(self):
        print self.message

class setup:
    
    def __init__(self):
        self.debugmode = False
        # I'm defaulting cmdmode to True since the GUI isn't implemented yet
        self.cmdmode = False
        self.helpmode = False
        self.walkmode = False
        self.validargs = ['-h', '--help', '-v', '--verbose', '-c', '--cmd', '-w', '--walk']

    def print_help_menu(self):
        print '''
NAME
    Walk-ER vBeta0.3

SYNOPSIS
    $ python walker.py [OPTIONS] [FILE]
    
    >>> import walker

DESCRIPTION
    "Walker" for Entity-Relational Diagrams from ERDPlus
    https://erdplus.com/#/

    Used for parsing the JSON file exports from ERDPlus.
    Parses the document, rebuilds the relationships and assists the user in creating a BoostSRL Background File.

OPTIONS
    -h, --help: Print a message that briefly summarizes command-line options and help information, then exits.
            
    -v, --verbose:
            "Debug Mode," where intermediate steps are printed to terminal.
            Most applicable when Commandline mode is also activated.

    -c, --cmd: "Commandline Mode", override the gui and interact through the shell.

    -w, --walk: [EXPERIMENTAL] walk graph from target to features, instantiating variables along the path.

FILE
    Specify a relative or absolute path to the JSON (.erdplus) file.
        diagrams/SmokesFriends.erdplus
        diagrams/FatherOf.erdplus
        /home/user/Desktop/Walk-ER/diagrams/SmokesFriends.erdplus

AUTHOR
    Written by Alexander L. Hayes, Indiana University STARAI Lab
    Bugs/Questions: hayesall@indiana.edu
    Last Updated: February 8, 2017

COPYRIGHT
    Copyright 2017 Free Software Foundation, Inc.  License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>.
    This is free software: you are free to change and redistribute it.  There is NO WARRANTY, to the extent permitted by law.

PLANNED FEATURES

    -t, --test: Run unit tests.

    -d, --depth: max search depth (default=None)

    -r, --repeat: number of times a node can be revisited (default=0) 
            '''
        exit()

    def read_user_input(self):
        '''Read the user-specified input for the file to parse
        Succeeds if the file is valid.'''
        args = sys.argv
        flags = args[1:-1]
        
        #check if there are no arguments
        if (len(args) == 1):
            self.print_help_menu()

        for flag in flags:
            if flag not in self.validargs:
                raise InvalidArgumentException(
                    '\nUnknown argument: %s' % flag
                )

        # Help: print help to out and terminate program.
        if ('-h' in args) or ('--help' in args):
            self.helpmode = True
            self.print_help_menu()

        # Debug mode
        if ('-v' in args) or ('--verbose' in args):
            self.debugmode = True

        # gui override: commandline mode
        if ('-c' in args) or ('--cmd' in args):
            self.cmdmode = True
        
        # instantiate variables by walking the graph
        if ('-w' in args) or ('--walk' in args):
            self.walkmode = True

        # not file not found
        if not os.path.isfile(args[-1]):
            raise InputException(
                '\nFile error, file not found.'
                '\nUsage: $ python walker.py [OPTIONS] [FILE]'
            )
        return args[-1]

    def import_data(self, file_to_read):
        '''Reads the contents of 'file_to_read', raises an exception if it cannot be read.'''
        try:
            doc = open(file_to_read).read()
        except:
            raise InputException(
                '\nFile error, could not read file.'
                '\nUsage: $ python walker.py [OPTIONS] [FILE]'
            )
        return doc

class buildDictionaries:

    def __init__(self, debugmode=False):
        self.debugmode = debugmode

    def debug(self):
        if self.debugmode:
            print "\n'Debug Mode' is activated, intermediate steps will be printed to terminal.\n"

    def extractVariables(self, json_dict):
        '''
        Input: a json dictionary
        Returns of dictionary of variables bound to their entity-id from ERDPlus
        i.e. {'1': 'professorid', '10': 'courseid', '6': 'studentid'}
        '''
        ER_dictionary = {}
        variable_dictionary = {}
        coordinate_dictionary = {}
        
        if 'shapes' in json_dict:
            for i in range(len(json_dict['shapes'])):
                current = json_dict['shapes'][i]
                if ('type' in current) and ('details' in current):
                    number = str(current['details'].get('id'))
                    name = str(current['details'].get('name'))
                    xcoord = int(current['details'].get('x'))
                    ycoord = int(current['details'].get('y'))

                    coordinate_dictionary[number] = [xcoord, ycoord]
                    ER_dictionary[number] = [name, str(current['type'])]
                    if current['type'] == 'Entity':
                        variable_dictionary[number] = name.lower() + 'id'
        if self.debugmode:
            print 'Variables:\n', str(variable_dictionary)
            print 'All Shapes:\n', str(ER_dictionary)
            print 'Coordinates:\n', str(coordinate_dictionary)
        return ER_dictionary, variable_dictionary, coordinate_dictionary
        
    def extractAttributes(self, json_dict, ER_dictionary, variable_dictionary):
        '''
        Input: a json dictionary, ER_dictionary, variable_dictionary
        Returns a dictionary of [entity-id, isMultivalued] bound to their name:
        i.e. {'Salary': ['True', '1'], 'Tenure': ['False', '1'], 'Rating': ['True', '10'], ...}
        '''
        attribute_dictionary = {}

        if 'shapes' in json_dict:
            for i in range(len(json_dict['shapes'])):
                current = json_dict['shapes'][i]
                if ('type' in current) and ('details' in current):
                    if current['type'] == 'Attribute':
                        name = str(current['details'].get('name'))
                        multi = str(current['details'].get('isMultivalued'))
                        attribute_dictionary[name] = [multi]

        if 'connectors' in json_dict:
            for i in range(len(json_dict['connectors'])):
                current = json_dict['connectors'][i]
                if 'type' in current:
                    # rebuild the graph as an undirected dictionary
                    src = str(current['source'])
                    dest = str(current['destination'])
                    if (current['type'] == 'Connector'):
                        # attributes can be inferred if it's a regular connector
                        name = str(ER_dictionary.get(str(current['source']))[0])
                        if name in attribute_dictionary:
                            attribute_dictionary[name].append(dest)
                        
        if self.debugmode:
            print 'Attributes:\n', str(attribute_dictionary)
        return attribute_dictionary

    def rebuildGraph(self, json_dict, ER_dictionary):
        '''
        Input: a json dictionary
        Creates an intermediary dictionary of nodes and associated edges {'1': ['2', '3', '7', '11', '34'], }
        Returns an updated dictionary where references are replaced with names
        {}
        '''
        Graph = {}
        ER_Graph = {}
        
        if 'connectors' in json_dict:
            for i in range(len(json_dict['connectors'])):
                current = json_dict['connectors'][i]
                if 'type' in current:
                    # rebuild an undirected graph from the connectors
                    src = str(current['source'])
                    dest = str(current['destination'])
                    if src in Graph:
                        Graph[src].append(dest)
                    else:
                        Graph[src] = [dest]
                    if dest in Graph:
                        Graph[dest].append(src)
                    else:
                        Graph[dest] = [src]
        if self.debugmode:
            print 'Graph:\n', str(Graph)

        # update the keys and values
        ER_Graph = {}
        for key in ER_dictionary:
            ER_Graph[ER_dictionary.get(key)[0]] = [ER_dictionary[value][0] for value in Graph[key]]
        return ER_Graph

    def extractRelationships(self, json_dict, variable_dictionary):
        '''
        "Determine if if a relationship is one-many, many-one, many-many, or unspecified."
        Input: a json dictionary and a variable dictionary
        Returns a dictionary of [to, from, toCardinality, fromCardinality]
        i.e. {'Advises': ['6', '1', 'many', 'one']}
          --> Many students are advised by a professor.
        i.e. {'Takes': ['10', '6', 'many', 'many']}
          --> Many courses are taken by many students.
          --(or)-> students take multiple courses, and courses are taken by multiple students.
        '''
        relationship_dictionary = {}
        
        if 'shapes' in json_dict:
            for i in range(len(json_dict['shapes'])):
                current = json_dict['shapes'][i]
                if ('type' in current) and ('details' in current):
                    name = str(current['details'].get('name'))
                    if current['type'] == 'Relationship':
                        temp = current['details'].get('slots')
                        var1 = variable_dictionary.get(str(temp[0]['entityId']))
                        var2 = variable_dictionary.get(str(temp[1]['entityId']))
                        relationship_dictionary[name] = [str(temp[1]['entityId']), str(temp[0]['entityId'])]

        for x in json_dict['shapes']:
            shapes_dict = x['details'].get('slots')
            if shapes_dict:
                name = str(x['details'].get('name'))
                dir1 = str(shapes_dict[0].get('cardinality'))
                dir2 = str(shapes_dict[1].get('cardinality'))
                relationship_dictionary[name].append(dir2)
                relationship_dictionary[name].append(dir1)

        if self.debugmode:
            print 'Relationships:\n', str(relationship_dictionary)
        return relationship_dictionary

class cmdlineMode:

    def __init__(self, debugmode=False):
        self.debugmode = debugmode

    def targetFeatureSelection(self, attribute_dictionary, relationship_dictionary):
        '''Ask the user for ['target', ['feature1', 'feature2', ...]]'''
        possible_targets = attribute_dictionary.keys() + relationship_dictionary.keys()
        
        while 1:
            print "\nPlease select your target from this list:\n\t" + '    '.join(possible_targets)
            sys.stdout.flush()
            target = raw_input()
            if target in possible_targets:
                possible_targets.remove(target)
                break
            else:
                print '\tError, target not in list.'

        while 1:
            print "\nPlease select features you want to learn over (separated by spaces):\n\t" + '    '.join(possible_targets)
            sys.stdout.flush()
            features = raw_input()
            features = features.split()
            final_features = []
            for feature in features:
                if feature in possible_targets:
                    final_features.append(feature)
                else:
                    print '\tError, "' + feature + '" not in list.'
            if (len(final_features) == len(features)):
                break
        
        targetAndFeatures = [target, list(OrderedDict.fromkeys(final_features))]
        if self.debugmode:
            print targetAndFeatures
        return targetAndFeatures

class guiMode:

    def __init__(self, ER_dictionary, variable_dictionary, 
                 attribute_dictionary, relationship_dictionary, coordinate_dictionary):
        self.ER_dictionary = ER_dictionary
        self.variable_dictionary = variable_dictionary
        self.attribute_dictionary = attribute_dictionary
        self.relationship_dictionary = relationship_dictionary
        self.coordinate_dictionary = coordinate_dictionary
        
        # Shapes that need to be drawn
        self.rectangles = {}
        self.ovals = {}
        self.diamonds = {}

    def build_shapes(self):
        for key in ER_dictionary:
            current_type = ER_dictionary[key][1]
            coords = self.coordinate_dictionary.get(key)
            if (current_type == 'Attribute'):
                self.ovals[key] = [coords[0], coords[1], ER_dictionary[key][0]]
            elif (current_type == 'Entity'):
                self.rectangles[key] = [coords[0], coords[1], ER_dictionary[key][0]]
            elif (current_type == 'Relationship'):
                self.diamonds[key] = [coords[0], coords[1], ER_dictionary[key][0]]

    def run_gui(self):
        #needs to return a targetsAndFeatures: ['Salary', ['Teaches', 'Rating', 'Tenure']]
        import pygame
        pygame.init()
        pygame.font.init()

        myfont = pygame.font.SysFont('monospace', 12)
        
        # colors
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
        DARKGRAY = (64, 64, 64)
        GRAY = (128, 128, 128)
        LIGHTGRAY = (212, 208, 200)
        BLUE = (0, 0, 255)
        RED = (255, 0, 0)

        size = [900, 600]
        screen = pygame.display.set_mode(size)

        # loop until the user clicks the close button
        done = False
        clock = pygame.time.Clock()

        # shapes to draw
        #Entities are rectangles
        rectangles = self.rectangles.values()
        #Attributes are ovals
        ovals = self.ovals.values()
        #Relationships are diamonds, there aren't built-in diamonds so we can do rectangles in the meantime
        diamonds = self.diamonds.values()

        while not done:
            clock.tick(10)

            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        done = True
                elif event.type == pygame.QUIT:
                    done = True

            # Clear the screen and set background color to white
            screen.fill(WHITE)

            # Draw all of the rectangles
            for tupl in rectangles:
                #rectangles should be 110,55
                pygame.draw.rect(screen, BLACK, (tupl[0], tupl[1], 110, 55), 1)
                label = myfont.render(tupl[2], 1, BLACK)
                screen.blit(label, (tupl[0]+5, tupl[1]+5))
                
            # Draw all of the ovals
            for tupl in ovals:
                # ovals should be about the same size 110,55
                pygame.draw.ellipse(screen, BLACK, (tupl[0], tupl[1], 110, 55), 1)
                label = myfont.render(tupl[2], 1, BLACK)
                screen.blit(label, (tupl[0]+40, tupl[1]+20))
                
            for tupl in diamonds:
                #!!! switch this to pygame.draw.polygon (specify an array of points to draw between)
                pygame.draw.rect(screen, BLACK, (tupl[0], tupl[1], 50, 25), 1)
                label = myfont.render(tupl[2], 1, BLACK)
                screen.blit(label, (tupl[0]+5, tupl[1]+5))
              
            #button = button.get_rect()
            #b = screen.blit(button, (300, 200))

            pygame.display.flip()

        pygame.font.quit()
        pygame.quit()

class constructModes:

    def __init__(self, targetAndFeatures, ER_dictionary, 
                 variable_dictionary, attribute_dictionary, 
                 relationship_dictionary, cmdlinemode=True, debugmode=False):
        self.cmdmode = cmdlinemode
        self.debugmode = debugmode
        self.target = targetAndFeatures[0]
        self.features = targetAndFeatures[1]
        self.ER_dictionary = ER_dictionary
        self.variable_dictionary = variable_dictionary
        self.attribute_dictionary = attribute_dictionary
        self.relationship_dictionary = relationship_dictionary
        self.target_variables = []
        self.all_modes = ['//Modes:', '//target:']
        if self.cmdmode:
            print "\n\n//Modes:"

    def handleTargetVariables(self):
        if self.cmdmode:
            print "//target:"

        # The target can be either a relation or an attribute
        if self.target in self.relationship_dictionary:
            # ['1', '1', 'many', 'one']
            #target_type = 'relationship'
            if self.debugmode:
                print self.relationship_dictionary.get(self.target)
            
            target_variable = self.relationship_dictionary[self.target][0:2]
            self.target_variables = [self.variable_dictionary.get(target_variable[0]),
                                     self.variable_dictionary.get(target_variable[1])]

            current_mode = "mode: %s(+%s,+%s)." % (self.target.lower(),
                                                   self.target_variables[0],
                                                   self.target_variables[1])
            if self.cmdmode:
                print current_mode
            self.all_modes.append(current_mode)
            
            #handle reflexive relationships by cutting extra variables
            self.target_variables = list(set(self.target_variables))

        elif self.target in self.attribute_dictionary:
            # ['False', '1']
            #target_type = 'attribute'
            target_variable = self.attribute_dictionary.get(self.target)

            if self.debugmode:
                print "//Target Variable: ", target_variable
            
            isMultivalued = (target_variable[0] == 'True')

            self.target_variables = [self.variable_dictionary.get(target_variable[1])]

            if isMultivalued:
                current_mode = "mode: %s(+%s,#%s)." % (self.target.lower(), 
                                                       self.target_variables[0],
                                                       self.target.lower())
                if self.cmdmode:
                    print current_mode
                self.all_modes.append(current_mode)
                #else we're in gui mode and we should print directly to a file
            else:
                current_mode = "mode: %s(+%s)." % (self.target.lower(), 
                                                   self.target_variables[0])
                if self.cmdmode:
                    print current_mode
                self.all_modes.append(current_mode)
                #else we're in gui mode and we should print directly to a file
                
        else:
            raise InvalidArgumentException(
                '\nTarget variable is neither an attribute nor a relationship.'
                '\nIf you experience this error, send the file and a brief description to Alexander.'
                '\nUsage: $ python walker.py [OPTIONS] [FILE]'
            )
        print "//other features"
        self.all_modes.append('//other features')

    def handleRelationVariables(self):
        # iterate through all relationships
        for rel in self.relationship_dictionary.keys():
            # we've already handled the target, skip it.
            current_relation = self.relationship_dictionary[rel]
            if rel in self.target:
                continue
            elif rel in self.features:
                #relationship is important
                if (current_relation[0] == current_relation[1]):
                    # check for reflexivity
                    a_mode = self.variable_dictionary.get(current_relation[0])
                    b_mode = self.variable_dictionary.get(current_relation[1])
                    current_mode1 = "mode: %s(+%s,-%s)." % (rel.lower(), a_mode, b_mode)
                    current_mode2 = "mode: %s(-%s,+%s)." % (rel.lower(), b_mode, a_mode)
                    if self.cmdmode:
                        print current_mode1, '\n', current_mode2
                    self.all_modes.append(current_mode1)
                    self.all_modes.append(current_mode2)
                else:
                    #relationship is not reflexive
                    inst_a = '+'
                    inst_b = '+'
                    if (self.variable_dictionary.get(current_relation[0]) not in self.target_variables):
                        inst_a = '-'
                    if (self.variable_dictionary.get(current_relation[1]) not in self.target_variables):
                        inst_b = '-'
                    current_mode = "mode: %s(%s%s,%s%s)." % (rel.lower(), inst_a,
                                                             self.variable_dictionary.get(current_relation[0]),
                                                             inst_b,
                                                             self.variable_dictionary.get(current_relation[1]))
                    if self.cmdmode:
                        print current_mode
                    self.all_modes.append(current_mode)

            else:
                # if the relation is "less important," fill with +
                current_mode = "mode: %s(+%s,+%s)." % (rel.lower(),
                                                       self.variable_dictionary.get(current_relation[0]),
                                                       self.variable_dictionary.get(current_relation[1]))
                if self.cmdmode:
                    print current_mode
                self.all_modes.append(current_mode)
            
    
    def handleAttributeVariables(self):
        for attr in self.attribute_dictionary.keys():
            current_attribute = self.attribute_dictionary[attr]
            isMultivalued = (current_attribute[0] == 'True')
            
            if ((self.variable_dictionary.get(current_attribute[1]) not in self.target_variables) 
                and 
                (attr in self.features)):
                # If the attribute variable is not a target variable, but is an important feature.
                instantiation_symbol = '-'
            else:
                # Otherwise, the variable has either been instantiated or was deemed unimportant.
                instantiation_symbol = '+'

            if attr in self.target:
                # The variable has already been handled, do nothing.
                continue
            else:
                if isMultivalued:
                    current_mode = "mode: %s(%s%s,#%s)." % (attr.lower(), instantiation_symbol,
                                                            self.variable_dictionary.get(current_attribute[1]),
                                                            attr.lower())
                else:
                    current_mode = "mode: %s(%s%s)." % (attr.lower(), instantiation_symbol,
                                                        self.variable_dictionary.get(current_attribute[1]))
                if self.cmdmode:
                    print current_mode
                self.all_modes.append(current_mode)

    def write_modes_to_file(self):

        if self.cmdmode:
            while 1:
                print '\nWould you like to write these modes to a background.txt file? [y/n]'
                sys.stdout.flush()
                write_choice = raw_input()
                if ((write_choice == 'y') or (write_choice == 'Y') or (write_choice == 'yes')):
                    print '\nWriting modes to background.txt'
                    write_to = open('background.txt', 'w')
                    for mode in self.all_modes:
                        write_to.write("%s\n" % mode)
                    break
                elif ((write_choice == 'n') or (write_choice == 'N') or (write_choice == 'no')):
                    print '\nNow exiting.'
                    break
                else:
                    print '\nInvalid choice.'

class networks:
    

    def __init__(self, targetAndFeatures, ER_dictionary, 
                 variable_dictionary, attribute_dictionary, 
                 relationship_dictionary, cmdlinemode=True, debugmode=False):
        self.cmdmode = cmdlinemode
        self.debugmode = debugmode
        self.targetAndFeatures = targetAndFeatures
        self.target = targetAndFeatures[0]
        self.features = targetAndFeatures[1]
        self.ER_dictionary = ER_dictionary
        self.variable_dictionary = variable_dictionary
        self.attribute_dictionary = attribute_dictionary
        self.relationship_dictionary = relationship_dictionary
        self.target_variables = []
        self.all_modes = ['//Modes:', '//target:']
        if self.cmdmode:
            print "\n\n//Modes:"

    def find_all_paths(self, graph, start, end, path=[]):
        # https://www.python.org/doc/essays/graphs/
        path = path + [start]
        if start == end:
            return [path]
        if start not in graph:
            #if not graph.has_key(start):
            return []
        paths = []
        for node in graph[start]:
            if node not in path:
                newpaths = self.find_all_paths(graph, node, end, path)
                for newpath in newpaths:
                    paths.append(newpath)
        return paths

    def paths_from_target_to_features(self, graph):
        all_paths = []
        if self.debugmode:
            print '\nAll paths from target to features.'
        for feature in self.targetAndFeatures[1]:
            p = self.find_all_paths(graph, self.targetAndFeatures[0], feature)
            all_paths.append(p)
            #print p
        return all_paths

    def find_pagerank(self, graph):
        import networkx as nx
        '''Takes a graph in the form of a python dictionary, returns dictionary of pageranks for each node'''
        G = nx.from_dict_of_lists(graph)
        P = nx.pagerank(G, alpha=0.85)
        if self.debugmode:
            print P
        return P

    def walkFeatures(self, graph, targetAndFeatures, all_paths):
        '''
        "Use user-selected features to construct background/modes."
        Input: [target feature], [a list of features selected by the user].
        Output: (for now, print modes to terminal, in the future write them to a file)
        '''
        
        '''
        I thought this might be possible, but they're doing different things so probably not.
        ConstructModes = constructModes(self.targetAndFeatures, self.ER_dictionary, 
                                        self.variable_dictionary, self.attribute_dictionary, 
                                        self.relationship_dictionary, cmdlinemode=self.cmdmode, 
                                        debugmode=self.debugmode)
        ConstructModes.handleTargetVariables()
        print '\n', str(ConstructModes.all_modes), '\n'
        '''

        # First, instantiate variables 
        if self.target in self.attribute_dictionary:
            target_variables = [(self.attribute_dictionary[self.target])[1]]
        elif self.target in self.relationship_dictionary:
            target_variables = (self.relationship_dictionary[self.target])[0:2]

        print '\n', str(target_variables), '\n'

        for lsa in all_paths:
            print "a"
            for lsb in lsa:
                print lsb
                instantiated_variables = set(target_variables)
                for predicate in lsb:
                    # Skip the first predicate since it's the target.
                    if predicate in self.attribute_dictionary:
                        if attribute_dictionary[predicate][1] in instantiated_variables:
                            print "+%s" % (variable_dictionary[attribute_dictionary[predicate][1]])
                        else:
                            print "-%s" % (variable_dictionary[attribute_dictionary[predicate][1]])
                        instantiated_variables = instantiated_variables.union(set((attribute_dictionary[predicate])[1]))
                        #print attribute_dictionary[predicate]
                    elif predicate in self.relationship_dictionary:
                        for var in relationship_dictionary[predicate][0:2]:
                            if var in instantiated_variables:
                                print "+%s" % (variable_dictionary[var])
                            else:
                                print "-%s" % (variable_dictionary[var])
                        instantiated_variables = instantiated_variables.union(set((relationship_dictionary[predicate])[0:2]))
                        #print relationship_dictionary[predicate]
                    else:
                        # Predicate is an entity and we can skip it.
                        continue
                    print predicate, instantiated_variables

class unitTests:
    
    def __init__(self):
        pass

    def run_unit_tests(self):
        pass

if __name__ == '__main__':
    '''Setup'''
    Setup = setup()
    # specify file to read
    json_file = Setup.read_user_input()
    # import the file
    json_data = Setup.import_data(json_file)
    # convert from json format to something more python-friendly
    json_dict = json.loads(json_data)
    
    '''Create dictionaries from the provided file'''
    #Check if the user set the "debug mode" flag (-v, --verbose)
    BuildDictionaries = buildDictionaries(Setup.debugmode)
    BuildDictionaries.debug()
    
    # find the variables (based on entities in the graph), also create a dictionary of all shapes
    ER_dictionary, variable_dictionary, coordinate_dictionary = BuildDictionaries.extractVariables(json_dict)

    # find the attributes
    attribute_dictionary = BuildDictionaries.extractAttributes(json_dict, ER_dictionary, variable_dictionary)
    
    # find the relationships and their cardinality # {'Friends', ['1','1','many','many']}
    relationship_dictionary = BuildDictionaries.extractRelationships(json_dict, variable_dictionary)

    # rebuild an undirected graph
    Graph = BuildDictionaries.rebuildGraph(json_dict, ER_dictionary)

    '''Different options depending on whether the user is in gui/cmdline mode'''
    if Setup.cmdmode:
        cmdlinemode = cmdlineMode(Setup.debugmode)

        # Ask the user for the target and useful features.
        targetAndFeatures = cmdlinemode.targetFeatureSelection(attribute_dictionary, relationship_dictionary)

    else:
        # debugmode is basically irrelevant within the gui
        guimode = guiMode(ER_dictionary, variable_dictionary, attribute_dictionary, relationship_dictionary, coordinate_dictionary)
        #guimode = guiMode(coordinate_dictionary) #debugmode is irrelevant with the gui.
        guimode.build_shapes()
        guimode.run_gui()
        #targetAndFeatures = guimode.targetFeatureSelection(attribute_dictionary, relationship_dictionary)

        # doing some testing just in case
        #cmdlinemode = cmdlineMode(Setup.debugmode)
        #targetAndFeatures = cmdlinemode.targetFeatureSelection(attribute_dictionary, relationship_dictionary)
        

    if Setup.walkmode:
        '''Optional / testing: with the rebuild graph, walk the graph'''
        # Open an instance of the networks class.

        Networks = networks(targetAndFeatures, ER_dictionary,
                            variable_dictionary, attribute_dictionary,
                            relationship_dictionary, cmdlinemode=Setup.cmdmode, debugmode=Setup.debugmode)
        
        all_paths = Networks.paths_from_target_to_features(Graph)
        #P = Networks.find_pagerank(Graph)
        Networks.walkFeatures(Graph, targetAndFeatures, all_paths)
        
    else:
        ConstructModes = constructModes(targetAndFeatures, ER_dictionary, 
                                        variable_dictionary, attribute_dictionary, 
                                        relationship_dictionary, cmdlinemode=Setup.cmdmode, 
                                        debugmode=Setup.debugmode)
        
        ConstructModes.handleTargetVariables()
        ConstructModes.handleRelationVariables()
        ConstructModes.handleAttributeVariables()
        ConstructModes.write_modes_to_file()

    exit()
