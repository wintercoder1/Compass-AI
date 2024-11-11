from dataclasses import dataclass, field
from dataclasses_json import dataclass_json

@dataclass_json
@dataclass
class TopicInfo():
    timestamp: int 
    normalized_topic_name: str 
    topic: str 
    lean: str 
    rating: int
    context: str 
    citation: str