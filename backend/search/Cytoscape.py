from typing import List, Dict

# CytoscapeEntity is the base class for both Node and Relationship classes.
# It defines common properties and methods for both classes.
class CytoscapeEntity:
    def __init__(self, id: int, data: Dict[str, str]):
        self.id = id          # Unique ID for the entity
        self.group = None     # Specifies whether the entity is a node or an edge (relationship)
        self.data = data      # Dictionary containing entity properties
        self.classes = []     # List of CSS classes for styling the entity in Cytoscape



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
        self.group = "nodes"      # Assigns the group as 'nodes' for node entities
        self.classes.append(classes)

    # Converts the Node object to a dictionary, which can be used as an input for the Cytoscape library.
    def to_dict(self):
        return {
            "id": self.id,
            "group": self.group,
            "data": {"id": self.id, **self.data},
            "classes": self.classes,
        }

# The Relationship class represents relationships between nodes in the graph.
# It inherits from the CytoscapeEntity class.
class Relationship(CytoscapeEntity):
    def __init__(self, id: int, classes: str, data: Dict[str, str]):
        super().__init__(id, data)
        self.group = "edges"      # Assigns the group as 'edges' for relationship entities
        self.classes.append(classes)

    # Converts the Relationship object to a dictionary, which can be used as an input for the Cytoscape library.
    def to_dict(self):
        return {
            "id": self.id,
            "group": self.group,
            "data": self.data,
            "classes": self.classes
        }
