from .constants import actions


from .models import (
    Entity,
    Address,
    Intermediary,
    Officer,
    Other
)

# For easily access each of the model classes programmatically, create a key-value map.
MODEL_ENTITIES = {
    'Entity': Entity,

}