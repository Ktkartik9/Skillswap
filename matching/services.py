from skills.models import UserSkill


def get_matches(user):

    my_teaching_skills = UserSkill.objects.filter(
        user=user,
        skill_type=UserSkill.TEACH
    ).values_list(
        "skill_id",
        flat=True
    )

    my_learning_skills = UserSkill.objects.filter(
        user=user,
        skill_type=UserSkill.LEARN
    ).values_list(
        "skill_id",
        flat=True
    )

    if not my_teaching_skills or not my_learning_skills:
        return []

    potential_users = UserSkill.objects.filter(
        skill_type=UserSkill.TEACH,
        skill_id__in=my_learning_skills
    ).exclude(
        user=user
    ).values_list(
        "user_id",
        flat=True
    ).distinct()

    matches = []

    for user_id in potential_users:

        has_reverse_match = UserSkill.objects.filter(
            user_id=user_id,
            skill_type=UserSkill.LEARN,
            skill_id__in=my_teaching_skills
        ).exists()

        if has_reverse_match:
            matches.append(user_id)

    return matches