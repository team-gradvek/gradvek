from typing import List, Dict

# The base class for both Node and Relationship classes. It defines common properties
# and methods for both classes.
class CytoscapeEntity:
    def __init__(self, id: int, data: Dict[str, str]):
        self.id = id
        self.group = None
        self.data = data
        self.classes = []


# The Node class represents nodes in the graph. It inherits from the CytoscapeEntity class.
class Node(CytoscapeEntity):
    # NODE_PROPERTY_MAP defines a mapping between the node properties and their corresponding keys.
    NODE_PROPERTY_MAP = {
        "AdverseEvent": [
            ("meddraId", "meddraId"),
            ("name", "adverseEventId"),
            ("adverseEventId", "adverseEventId"), 
            ("id", "id"),
         ],
        "Drug": [
            ("chemblId", "chemblId"),
            ("name", "drugId"),
            ("drugId", "drugId"), 
            ("id", "id"),
        ],
        'Target': [
            ('ensembleId', 'ensembleId'),
            ('symbol', 'symbol'),
            ('name', 'name'),
            ('id', 'id'),
        ],
        "Pathway": [
            ("name", "pathwayCode"), 
            ("term", "topLevelTerm"),
            ("id", "id"),
            ("pathwayId", "pathwayId"),
        ],
        "MousePhenotype": [
            ("mousePhenotypeId", "mousePhenotypeId"), 
            ("name", "label"),
            ("id", "id"),
        ]
    }

    def __init__(self, id: int, classes: str, data: Dict[str, str]):
        super().__init__(id, data)
        self.group = "nodes"
        self.classes.append(classes)

    # Converts the Node object to a dictionary, which can be used as an input for the Cytoscape library.
    def to_dict(self):
        return {
            "id": self.id,
            "group": "nodes",
            "data": {"id": self.id, **self.data},
            "classes": self.classes,
        }

# The Relationship class represents relationships between nodes in the graph. It inherits from the CytoscapeEntity class.
class Relationship(CytoscapeEntity):
    def __init__(self, id: int, classes: str, data: Dict[str, str]):
        super().__init__(id, data)
        self.group = "edges"
        self.classes.append(classes)

    # Converts the Relationship object to a dictionary, which can be used as an input for the Cytoscape library.
    def to_dict(self):
        return {
            "id": self.id,
            "group": self.group,
            "data": self.data,
            "classes": self.classes
        }
