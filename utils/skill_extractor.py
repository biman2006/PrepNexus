def extract_skill(text,skill_list):
    found_skill=[]

    text=text.lower()

    for skill in skill_list:
        if skill.lower() in text:
            found_skill.append(skill.lower())

    return list(set(found_skill))


