def calculate_readiness(resume_skills,role_data):
    core=set(role_data["core"])
    secondary=set(role_data["secondary"])
    advanced=set(role_data["advanced"])

    core_score=(
        len(core.intersection(resume_skills))/len(core)
    )*60 if core else 0

    secondary_score=(len(secondary.intersection(resume_skills))/len(secondary)
                     
                     )*30 if secondary else 0


    advanced_score=(
        len(advanced.intersection(resume_skills))/len(advanced)
    )*10 if advanced else 0 


    final_score=core_score+secondary_score+advanced_score


    return {
        "core_matched": core.intersection(resume_skills),
        "secondary_matched":secondary.intersection(resume_skills),
        "advanced_matched":advanced.intersection(resume_skills),

        "missing_core":core-resume_skills,
        "missing_secondary":secondary-resume_skills,
        "missing_advanced":advanced-resume_skills,


        "core_score":round(core_score,2),
        "secondary_score":round(secondary_score),
        "advanced_score":round(advanced_score),


        "readiness_score":round(final_score,2)
    }