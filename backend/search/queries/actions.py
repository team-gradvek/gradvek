from neomodel import db


def get_actions(target):

    # Change cyper query if target symbol
    if target == "":
        cmd_filter = ""
    else:
        cmd_filter = f'WHERE toUpper(nt.symbol) = "{target}"'

    # Returns a list of lists of pair of actions and total count
    actions = db.cypher_query(
        f'''
        MATCH (:Drug)-[rt:TARGETS]-(:Target) 
        WITH DISTINCT rt.actionType AS actType 
        OPTIONAL MATCH (:Drug)-[rt2:TARGETS {{actionType: actType}}]-(nt:Target)
        {cmd_filter}
        RETURN actType, COUNT(rt2) 
        ORDER BY actType
        '''
    )[0]

    # Flat list out of list of lists
    flat_list = [pair for action in actions for pair in action]
    # Convert list to dictionary 
    lst_to_dict = [{'action':flat_list[i], 'count':flat_list[i+1]} for i in range(0,len(flat_list),2)]
    ACTIONS = lst_to_dict
    return ACTIONS