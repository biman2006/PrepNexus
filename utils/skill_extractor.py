def extract_skill(text,skill_list):
    found_skill=[]

    text=text.lower()

    words=text.split()

    sorted_skills=sorted(skill_list,key=len, reverse=True)

    for skill in sorted_skills:
        skill_lower=skill.lower()

        if " " in skill.lower:
            if skill.lower in text:
                found_skill.append(skill_lower)

        else:
            if skill_lower in words:
                found_skill.append(skill_lower)


    return list(set(found_skill))
        