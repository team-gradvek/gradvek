

def targetSimilarity(relationship):

    query = """
    CALL apoc.periodic.iterate(
        'myGraph',
        ['TARGET', {relationship}],
        {
            MOUSE_PHENOTYPE: {
                properties: {
                    strength: {
                        property: 'weight',
                        defaultValue: 1.0
                    }
                }
            }
        }
    );

    """
    return query

    