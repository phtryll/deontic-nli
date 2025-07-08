import os
import json
from source.cfg_utils import Rule

my_rules = [

        Rule(
            left="S",
            right=["[Premise]", "AFFIRMATION", "."],
            prob=0.33,
            features={}
        ),
        
        Rule(
            left="S",
            right=["[Hypothesis]", "DEONTIC_AFFIRMATION", "."],
            prob=0.34,
            features={}
        ),

        Rule(
            left="S",
            right=["[Premise]", "COMPOUND_PREMISE", "."],
            prob=0.33,
            features={}
        ),

        Rule(
            left="AFFIRMATION",
            right=["if", "PROP_1", "then", "PROP_2"],
            features={"name":"?n","verb":"?v","country":"?c","city":"?d"}
        ),  # p implies q
        
        Rule(
            left="DEONTIC_AFFIRMATION",
            right=["if", "MOD_1", "then", "MOD_2"],
            prob=0.5,
            features={"name":"?n","verb":"?v","country":"?c","city":"?d"}
        ),  # OB(p) implies OB(q)
        
        Rule(
            left="DEONTIC_AFFIRMATION",
            right=["MOD_2"],
            prob=0.5,
            features={"name":"?n","verb":"?v","country":"?c","city":"?d"}
        ),  # OB(q)
        
        Rule(
            left="COMPOUND_PREMISE",
            right=["AFFIRMATION", ".", "MOD_1"],
            features={"name":"?n","verb":"?v","country":"?c","city":"?d"}
        ),  # p implies q and OB(p)

        
        Rule(
            left="MOD_1",
            right=["it is obligatory that", "PROP_1"],
            features={"name":"?n","verb":"?v","country":"?c"}
        ),
        
        Rule(
            left="MOD_2",
            right=["it is obligatory that", "PROP_2"],
            features={"name":"?n","verb":"?v","country":"?c","city":"?d"}
        ),
        
        Rule(
            left="PROP_1",
            right=["p"],
            features={"name":"?n","verb":"?v","country":"?c"}
        ),
        
        Rule(
            left="PROP_2",
            right=["q"],
            features={"name":"?n","verb":"?v","country":"?c","city":"?d"}
        ),

        # Adding lexical items: geographic dependency case
        Rule(
            left="p",
            right=["NAME", "VERB", "in", "COUNTRY"],
            features={"name":"?n","verb":"?v","country":"?c"}
        ),
        
        Rule(
            left="q",
            right=["NAME", "VERB", "in", "CITY"],
            features={"name":"?n","verb":"?v","country":"?c","city":"?d"}
        ),

        # COUNTRY lexical rules
        Rule(left="COUNTRY", right=["Turkey"], features={"country":"Turkey"}),
        Rule(left="COUNTRY", right=["China"], features={"country":"China"}),
        Rule(left="COUNTRY", right=["Pakistan"], features={"country":"Pakistan"}),
        Rule(left="COUNTRY", right=["India"], features={"country":"India"}),
        Rule(left="COUNTRY", right=["Latvia"], features={"country":"Latvia"}),
        Rule(left="COUNTRY", right=["Russia"], features={"country":"Russia"}),
        Rule(left="COUNTRY", right=["Armenia"], features={"country":"Armenia"}),

        # CITY lexical rules
        Rule(left="CITY", right=["Istanbul"], features={"city":"Istanbul","country":"Turkey"}),
        Rule(left="CITY", right=["Guangzhou"], features={"city":"Guangzhou","country":"China"}),
        Rule(left="CITY", right=["Karachi"], features={"city":"Karachi","country":"Pakistan"}),
        Rule(left="CITY", right=["Ahmedabad"], features={"city":"Ahmedabad","country":"India"}),
        Rule(left="CITY", right=["Hyderabad"], features={"city":"Hyderabad","country":"India"}),
        Rule(left="CITY", right=["Riga"], features={"city":"Riga","country":"Latvia"}),
        Rule(left="CITY", right=["Shanghai"], features={"city":"Shanghai","country":"China"}),
        Rule(left="CITY", right=["Moscow"], features={"city":"Moscow","country":"Russia"}),
        Rule(left="CITY", right=["Yerevan"], features={"city":"Yerevan","country":"Armenia"}),
        Rule(left="CITY", right=["Chennai"], features={"city":"Chennai","country":"India"}),

        # Lexical rules: NAME choices
        Rule(left="NAME", right=["Alice"], features={"name":"Alice"}),
        Rule(left="NAME", right=["Bob"], features={"name":"Bob"}),
        Rule(left="NAME", right=["Carol"], features={"name":"Carol"}),
        Rule(left="NAME", right=["Dave"], features={"name":"Dave"}),
        Rule(left="NAME", right=["Eve"], features={"name":"Eve"}),
        Rule(left="NAME", right=["Frank"], features={"name":"Frank"}),
        Rule(left="NAME", right=["Grace"], features={"name":"Grace"}),
        Rule(left="NAME", right=["Heidi"], features={"name":"Heidi"}),
        Rule(left="NAME", right=["Ivan"], features={"name":"Ivan"}),
        Rule(left="NAME", right=["Judy"], features={"name":"Judy"}),
        Rule(left="NAME", right=["Karl"], features={"name":"Karl"}),
        Rule(left="NAME", right=["Laura"], features={"name":"Laura"}),
        Rule(left="NAME", right=["Mallory"], features={"name":"Mallory"}),
        Rule(left="NAME", right=["Nathan"], features={"name":"Nathan"}),
        Rule(left="NAME", right=["Olivia"], features={"name":"Olivia"}),
        Rule(left="NAME", right=["Peggy"], features={"name":"Peggy"}),
        Rule(left="NAME", right=["Quentin"], features={"name":"Quentin"}),
        Rule(left="NAME", right=["Rupert"], features={"name":"Rupert"}),
        Rule(left="NAME", right=["Sybil"], features={"name":"Sybil"}),
        Rule(left="NAME", right=["Trent"], features={"name":"Trent"}),

        # Lexical rules: VERB choices
        Rule(left="VERB", right=["lives"], features={"verb":"lives"}),
        Rule(left="VERB", right=["works"], features={"verb":"works"}),
        Rule(left="VERB", right=["visits"], features={"verb":"visits"}),
        Rule(left="VERB", right=["travels"], features={"verb":"travels"}),
        Rule(left="VERB", right=["eats"], features={"verb":"eats"}),
        Rule(left="VERB", right=["drinks"], features={"verb":"drinks"}),
        Rule(left="VERB", right=["reads"], features={"verb":"reads"}),
        Rule(left="VERB", right=["writes"], features={"verb":"writes"}),
        Rule(left="VERB", right=["plays"], features={"verb":"plays"}),
        Rule(left="VERB", right=["sings"], features={"verb":"sings"}),
        Rule(left="VERB", right=["runs"], features={"verb":"runs"}),
        Rule(left="VERB", right=["jumps"], features={"verb":"jumps"}),
        Rule(left="VERB", right=["drives"], features={"verb":"drives"}),
        Rule(left="VERB", right=["flies"], features={"verb":"flies"}),
        Rule(left="VERB", right=["speaks"], features={"verb":"speaks"}),
        Rule(left="VERB", right=["listens"], features={"verb":"listens"}),
        Rule(left="VERB", right=["teaches"], features={"verb":"teaches"}),
        Rule(left="VERB", right=["learns"], features={"verb":"learns"}),
        Rule(left="VERB", right=["creates"], features={"verb":"creates"}),
        Rule(left="VERB", right=["builds"], features={"verb":"builds"}),

]
