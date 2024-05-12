import pandas as pd
import math
import random

tab = '   '

class Relationship():
    def __init__(self, statement_type, statements):
        '''
        :param statement_type: AND, OR, NOT
        :param statements: list of factors or single factor (for not)
        '''
        self.statement_type = statement_type
        self.statements = statements
        
        if type(statements) is list and statement_type == 'NOT':
            print('You cannot have a list of statements in NOT statement, only a single factor')
            
        if not type(statements) is list and statement_type != 'NOT':
            print('You need to have a list of statements in your OR/AND statement, not a single factor' )

    def evaluate(self):
        if self.statement_type == 'OR':
            # The 'any' function can deal with None
            return any(s.evaluate() for s in self.statements)
        
        if self.statement_type == 'AND':
            # Deal with unknown values
            if None in [s.evaluate() for s in self.statements]:
                if False in [s.evaluate() for s in self.statements]:
                    return False
                else:
                    return None
            return all(s.evaluate() for s in self.statements)
        
        if self.statement_type == 'NOT':
            # Deal with unknown values
            if self.statements.evaluate() == None:
                return None
            return not self.statements.evaluate()

    def get_baselevel_factors(self):
        # Only 1 statement
        if self.statement_type == 'NOT':
            if type(self.statements) == BaseLevelFactor:
                return [self.statements]
            else: # Abstract factor
                return self.statements.get_baselevel_factors()
            
        # Multiple statements
        lst = []
        for f in self.statements:
            if type(f) == BaseLevelFactor:
                lst.append(f)
            else: # Abstract factor
                lst.extend(f.get_baselevel_factors())
        return lst

    def set_baselevel_factors(self, vals):
        
        def change_if_present(blf, vals):
            if blf.identifier in vals.keys():
                return vals[blf.identifier]
            return blf.value

        # Only 1 statement
        if self.statement_type == 'NOT':
            if type(self.statements) == BaseLevelFactor:
                self.statements.value = change_if_present(self.statements, vals)
            else: # Abstract factor
                self.statements.set_baselevel_factors(vals)
            return
        
        # Multiple statements
        for f in self.statements:
            if type(f) == BaseLevelFactor:
                f.value = change_if_present(f, vals)
            else: # Abstract factor
                f.set_baselevel_factors(vals)
                
        return

    
    def __repr__(self, indent=0):
        if self.statement_type == 'NOT':
            return tabs(indent) + 'NOT ' + self.statements.__repr__()
        joiner = ' ' + self.statement_type + '\n'+tabs(indent)
        return tabs(indent) + joiner.join(s.__repr__(indent+1) for s in self.statements)


class AbstractFactor():
    def __init__(self, identifier, text, default, acceptfactors=None, rejectfactors=None):
        self.identifier = identifier
        self.text = text
        self.default = default
        self.acceptfactors = acceptfactors
        self.rejectfactors = rejectfactors
        
        
    def evaluate(self):
        if self.rejectfactors and self.rejectfactors.evaluate():
            return False
        if self.acceptfactors and self.acceptfactors.evaluate():
            return True
        return self.default

    def get_baselevel_factors(self):
        blfs = []
        if self.acceptfactors:
            if(isinstance(self.acceptfactors, BaseLevelFactor)): blfs.append(self.acceptfactors)
            else: blfs.extend(self.acceptfactors.get_baselevel_factors())
        if self.rejectfactors:
            if(isinstance(self.rejectfactors, BaseLevelFactor)): blfs.append(self.rejectfactors)
            else: blfs.extend(self.rejectfactors.get_baselevel_factors())
        return remove_duplicates(blfs)
    
    def set_baselevel_factors(self, vals):
        '''
        Sets the values of a set of baselevel factors
        :param vals: dictionary in the form {id:value}
        '''
        if self.acceptfactors:
            self.acceptfactors.set_baselevel_factors(vals)
        if self.rejectfactors:
            self.rejectfactors.set_baselevel_factors(vals)

    
    def __repr__(self, indent=0):
        string = tabs(indent) + str(self.identifier) + ': ' +  self.text + '[' + str(self.evaluate()) + ']'
        
        if self.rejectfactors: 
            string += '\n' + tabs(indent+1) + 'REJECT ' + str(self.identifier) + ' IF:\n'
            string += self.rejectfactors.__repr__(indent)
            
        if self.acceptfactors: 
            string += '\n' + tabs(indent+1) + 'ACCEPT ' + str(self.identifier) + ' IF:\n'
            string += self.acceptfactors.__repr__(indent)

        if self.default:
            string += '\n' + tabs(indent+1) + 'ACCEPT otherwise\n' + tabs(indent) 
        else:
            string += '\n' + tabs(indent+1) + 'REJECT otherwise\n' + tabs(indent)
        return string


class BaseLevelFactor():
    def __init__(self, identifier, text, value):
        self.identifier = identifier
        self.text = text
        self.value = value
        
    def evaluate(self):
        return self.value
    
    def set_baselevel_factors(self, vals):
        self.value = vals[self.identifier]
        
    def __repr__(self, indent=0):
        return ''.join(tab for x in range(0, indent)) + str(self.identifier) + ': ' +  self.text + '[' + str(self.value)+']'
    

class ADF(AbstractFactor):
    def __init__(self, identifier, text, default, acceptfactors=None, rejectfactors=None):
        super().__init__(identifier, text, default, acceptfactors, rejectfactors)
           
    def classify(self, X, columns):
        '''
        Classifies a set of instances X using the ADF
        :param X: 2D array, the input instances
        :param columns: list of strings containing the names of the 
        columns of X
        :param label: the name of the label feature
        '''
        columns = columns.drop(['text', self.identifier])
        preds = []
        for x in X:
            blfs = {col: bool(int(x[idx])) for idx, col in enumerate(columns)}
            self.set_baselevel_factors(blfs)
            preds.append(self.evaluate())
        return preds
    
    def explain(self):
        blfs = self.get_baselevel_factors()
        true_blfs = [b for b in blfs if b.value==True]
        false_blfs = [b for b in blfs if b.value==False]
        none_blfs = [b for b in blfs if b.value==None]

        explanation = "We examined the question: '" + self.text + "' and determine that this is " + str(self.evaluate()) + "." 
        explanation += "\nWe believe this to be the case, as "
        
        if true_blfs:
            explanation += "we can answer yes to the following questions:\n"
        
        for blf in true_blfs:
            explanation += '\t' + blf.text + '\n'
        
        if false_blfs:
            if true_blfs: 
                explanation += '\nWhile '
            explanation += "we can answer 'no' to the following questions:\n"
        for blf in false_blfs:
            explanation += '\t' + blf.text + '\n'
            
        if none_blfs:
            if true_blfs or false_blfs:
                explanation += "\nAnd "
            explanation += "we do not know the answer to the following questions:\n"
        for blf in none_blfs:
            explanation += '\t' + blf.text + '\n'

        return explanation
    
    def create_dataset(self, db_size=None):
        '''
        Creates a dataset from the ADF containing the label, 
        baselevel factors and the description of those baselevel factors
        '''

        def create_case(c, sentence_dict):
            '''
            Creates a case from an integer number (C)
            '''
            c = to_binary(c, num_variables)
            instance = {}

            # For each base level factor
            for idy, identifier in enumerate(sentence_dict.keys()):
                instance[identifier] = c[idy]

            # Get and set the label
            blfs = {k: bool(int(v)) for k, v in instance.items() 
                    if k != 'text' and k != self.identifier}
            self.set_baselevel_factors(blfs)
            instance[self.identifier] = self.evaluate()
            return instance
    
        #Creates a dict in the form {identifier:text} from the base level factors
        sentence_dict = {blf.identifier: blf.text 
                     for blf in self.get_baselevel_factors()}

        num_variables = len(sentence_dict)
        num_all_cases = int(math.pow(2, num_variables))
        cases = range(0, num_all_cases)
        if db_size:
            cases = random.sample(range(0, num_all_cases), db_size)

        df = [create_case(c, sentence_dict) for c in cases]

        #Return as pandas dataframes
        return pd.DataFrame(df)

    
def tabs(indent=0):
    return ''.join(tab for x in range(0, indent))

def to_binary(number, length):
    number = format(number, "b")
    return ''.join('1' for _ in range(0, length - len(number))) + number

def remove_duplicates(lst):
    new_lst = []
    for l in lst:
        if not l in new_lst:
            new_lst.append(l)
    return new_lst