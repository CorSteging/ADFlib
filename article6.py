'''
An ADF for Article 6 of the European Convention on Human Rights, based on the paper:
"Explainable AI tools for legal reasoning about cases: A study on the European Court of Human Rights" by Collenette et al. 
Used in the paper "Improving Rationales with Small, Inconsistent and Incomplete Data" by Steging et al. 
'''

from ADFlib import *

#I1
I1 = BaseLevelFactor('I1', 'Is the applicant a victim?', False)


#I2
I2Q1 = BaseLevelFactor('I2Q1', 'Is the case well founded?', False)
I2F1Q1 = BaseLevelFactor('I2F1Q1', 'The case examines a fundamental aspect?', False)
I2F1Q2 = BaseLevelFactor('I2F1Q2', 'Have all Domestic courts have been exhausted?', False)

I2F1 = AbstractFactor(
    identifier = 'I2F1', 
    text = 'The victim suffered a disadvantage.',
    default = False,
    acceptfactors = Relationship('AND', [I2F1Q1, I2F1Q2])
)

I2 = AbstractFactor(
    identifier = 'I2', 
    text = 'The applicant was admissible',
    default = False,
    acceptfactors = Relationship('AND', [I2Q1, I2F1])
)

#I3
I3F1Q1 = BaseLevelFactor('I3F1Q1', 'Was the case conducted in a reasonable time?', False)
I3F1Q2 = BaseLevelFactor('I3F1Q2', 'Did the government cause any unreasonable delays?', False)
I3F2Q1 = BaseLevelFactor('I3F2Q1', 'The government was subjectively impartial?', False)
I3F2Q2 = BaseLevelFactor('I3F2Q2', 'The government was objectively impartial?', False)

I3F3Q1 = BaseLevelFactor('I3F3Q1', 'If the case was public, the public wouldn’t prejudice the outcome?', False)
I3F3Q2 = BaseLevelFactor('I3F3Q2', 'The safety of the public wouldn’t be impacted, if the case was public?', False)
I3F3Q3 = BaseLevelFactor('I3F3Q3', 'Any extra privacy is not required in this case?', False)
I3F3Q4 = BaseLevelFactor('I3F3Q4', 'The public would not hinder justice, if the case was public?', False)
I3F3Q5 = BaseLevelFactor('I3F3Q5', 'Was the case pronounced publicly?', False)
I3F3Q6 = BaseLevelFactor('I3F3Q6', 'Was the case conducted publicly?', False)

I3F4Q1 = BaseLevelFactor('I3F4Q1', 'Was there equality of arms?', False)

I3F5Q1 = BaseLevelFactor('I3F5Q1', 'Was the victim given appropriate access to Court?', False)

I3F6Q1 = BaseLevelFactor('I3F6Q1', 'Can the highest court be considered binding in its findings?', False)
I3F6Q2 = BaseLevelFactor('I3F6Q2', 'Was the case was reopened due to new facts or a fundamental defect in fairness?', False)
I3F6F1Q1 = BaseLevelFactor('I3F6F1Q1', 'Are there profound and long-standing differences in the case law?', False)
I3F6F1Q2 = BaseLevelFactor('I3F6F1Q2', 'Have tools have been used to overcome any difference in case law?', False)

I3F1 = AbstractFactor(
    identifier = 'I3F1', 
    text = 'Conducted in Reasonable Time.',
    default = False,
    acceptfactors = Relationship('AND', [I3F1Q2, I3F1Q1])
)

I3F2 = AbstractFactor(
    identifier = 'I3F2', 
    text = 'The case was independent and impartial.',
    default = False,
    acceptfactors = Relationship('AND', [I3F2Q1, I3F2Q2])
)


# (I3F3Q1 ∧ I3F3Q2 ∧ I3F3Q3 ∧ I3F3Q4 ∧ I3F3Q5 ∧ I3F3Q6)
# ∨ 
# ((¬I3F3Q1 ∨ ¬I3F3Q2 ∨ ¬I3F3Q3 ∨ ¬I3F3Q4) ∧ 
#  (¬I3F3Q5 ∧ ¬I3F3Q6))
I3F3 = AbstractFactor(
    identifier = 'I3F3', 
    text = 'The case was conducted publicly and had no exceptions.',
    default = False,
    acceptfactors = Relationship('OR', [
        Relationship('AND', [I3F3Q1, I3F3Q2, I3F3Q3, I3F3Q4, I3F3Q5, I3F3Q6]),
        Relationship('AND', [Relationship('OR', [Relationship('NOT', I3F3Q1), 
                                                 Relationship('NOT', I3F3Q2), 
                                                 Relationship('NOT', I3F3Q3), 
                                                 Relationship('NOT', I3F3Q4)
                                                ]),
                             Relationship('AND', [Relationship('NOT', I3F3Q5),
                                                  Relationship('NOT', I3F3Q6)
                                                 ])            
        ])
    ])
)


#I3F6F1Q 1 ∧ ¬I3F6F1Q2
I3F6F1 = AbstractFactor(
    identifier = 'I3F6F1', 
    text = 'There are conflicting decisions in case law which affect the fairness of the case.',
    default = False,
    acceptfactors = Relationship('AND', [I3F6F1Q1, Relationship('NOT', I3F6F1Q2)])
)


#(I3F6Q1 ∨ (¬I3F6Q1 ∧ I3F6Q2)) ∧ ¬I3F6F1
I3F6 = AbstractFactor(
    identifier = 'I3F6', 
    text = 'Legal certainty is upheld.',
    default = False,
    acceptfactors = Relationship('AND', [Relationship('OR', [I3F6Q1,
                                                             Relationship('AND', [Relationship('NOT', I3F6Q1),
                                                                                  I3F6Q2])
                                                            ]),
                                         Relationship('NOT', I3F6F1)
                                        ])
)

I3 = AbstractFactor(
    identifier = 'I3', 
    text = 'Fair and Public.',
    default = False,
    acceptfactors = Relationship('AND', [I3F1, I3F2, I3F3, I3F4Q1, I3F5Q1, I3F6])
)

#I4
I4Q1 = BaseLevelFactor('I4Q1', 'Was the victim presumed innocent?', False)
I4Q2 = BaseLevelFactor('I4Q2', 'Does the Prosecution bares the burden of proof?', False)
I4Q3 = BaseLevelFactor('I4Q3', 'Any doubts benefited applicant?', False)

I4 = AbstractFactor(
    identifier = 'I4', 
    text = 'The applicant was presumed innocent.',
    default = False,
    acceptfactors = Relationship('AND', [I4Q1, I4Q2, I4Q3])
)


#I5
I5Q1 = BaseLevelFactor('I5Q1', 'The applicant had time and facilities to prepare their defence?', False)
I5Q2 = BaseLevelFactor('I5Q2', 'The applicant could have free access to interpreter.', False)
I5F1Q1 = BaseLevelFactor('I5F1Q1', 'Was the applicant informed in the correct language?', False)
I5F1Q2 = BaseLevelFactor('I5F1Q2', 'Was the applicant given details of the case?', False)
I5F1Q3 = BaseLevelFactor('I5F1Q3', 'Was the applicant told what crime they had committed?', False)

I5F2Q1 = BaseLevelFactor('I5F2Q1', 'Has the applicant attempted to escape trial?', False)
I5F2Q2 = BaseLevelFactor('I5F2Q2', 'Has the applicant waived right to defend themselves?', False)
I5F2Q3 = BaseLevelFactor('I5F2Q3', 'The applicant was not prevented from accessing lawyers?', False)

I5F3Q1 = BaseLevelFactor('I5F3Q1', 'Did the applicant have access to legal assistance?', False)
I5F3Q2 = BaseLevelFactor('I5F3Q2', 'Did the applicant have access to free legal assistance if necessary?', False)

I5F4Q1 = BaseLevelFactor('I5F4Q1', 'Witnesses were examined under same conditions?', False)
I5F4Q2 = BaseLevelFactor('I5F4Q2', 'Witnesses had a valid reason for non attendance?', False)

I5F1 = AbstractFactor(
    identifier = 'I5F1', 
    text = 'The applicant was informed promptly.',
    default = False,
    acceptfactors = Relationship('AND', [I5F1Q1, I5F1Q2, I5F1Q3])
)


# I5F2Q3 ∧ ((I5F2Q2 ∧ ¬I5F2Q1) ∨ (¬I5F2Q1))
I5F2 = AbstractFactor(
    identifier = 'I5F2', 
    text = 'Opportunity to defend themselves in person.',
    default = False,
    acceptfactors = Relationship('AND', [I5F2Q3, 
                                         Relationship('OR', [Relationship('AND', [I5F2Q2, 
                                                                                  Relationship('NOT', I5F2Q1)]), 
                                                             Relationship('NOT', I5F2Q1)])])
)

I5F3 = AbstractFactor(
    identifier = 'I5F3', 
    text = 'Access to legal assistance.',
    default = False,
    acceptfactors = Relationship('AND', [I5F3Q1, I5F3Q2])
)

I5F4 = AbstractFactor(
    identifier = 'I5F4', 
    text = 'Able to examine witnesses.',
    default = False,
    acceptfactors = Relationship('AND', [I5F4Q1, I5F4Q2])
)

I5 = AbstractFactor(
    identifier = 'I5', 
    text = 'Had minimum rights.',
    default = False,
    acceptfactors = Relationship('AND', [I5F1, I5Q1, I5F2, I5F3, I5F4, I5Q2])
)

# The full ADF
art6_ADF = ADF(
    identifier = 'violation', 
    text = 'Violation of Article 6?',
    default = False,
    acceptfactors = Relationship('AND', [I1, I2, I3, I4, I5]),
)