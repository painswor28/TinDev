from django import template
register = template.Library()

@register.filter
def cpt(candidate, post):
    cskills = [x.strip(',').lower() for x in candidate.skills.split()]
    pskills = [x.strip(',').lower() for x in post.skills.split()]
    matches = 0
    for skill in pskills:
        if skill in cskills:
            matches += 1
    if(len(pskills)>0):
        skills_match = matches/len(pskills) * 70
    else:
        skills_match = 35
    type_matches = 0
    if post.title.lower() in candidate.profile_bio.lower():
        type_matches += 1
    if post.position_type.lower() in candidate.profile_bio.lower():
        type_matches += 1
    type_matches = type_matches / 2 * 20
    keywords = ['create', 'team', 'collaborate', 'innovate', 'fun']
    desc_words = [word for word in keywords if word in post.description]
    word_matches = 0
    if len(desc_words) > 0:
        for word in desc_words:
            if word in candidate.profile_bio.lower():
                word_matches += 1
        word_matches = word_matches / len(desc_words) * 10
    else:
        word_matches = 10

    return f'{int(skills_match + type_matches + word_matches + 0.5)}%'