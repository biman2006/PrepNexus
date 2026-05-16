from data.role_weights import role_skill_weights
from utils.skill_extractor import normalize_skill
print(list(role_skill_weights.keys())[:10])
role="data scientist"
skills=set(normalize_skill(skill) for section in role_skill_weights[role].values() for skill in section)
print(skills)
