from utils.skill_extractor import normalize_skill
from app import display_skill
print(normalize_skill("react.js"))
print(normalize_skill("node.js"))
print(normalize_skill("ci/cd"))
print(display_skill("react.js"))
print(display_skill("node.js"))
print(display_skill("ci cd"))
