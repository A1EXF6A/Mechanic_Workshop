import logging
_logger = logging.getLogger(__name__)

env = env(user=1)
portal_group = env.ref('base.group_portal')

profiles = env['usuarios_taller.user_profile'].search([])
processed_emails = set()

for profile in profiles:
    if profile.email in processed_emails:
        _logger.info(f"Skipping duplicate email: {profile.email} (profile {profile.id})")
        print(f"Skipping duplicate email: {profile.email} (profile {profile.id})")
        continue
    
    processed_emails.add(profile.email)
    
    if not profile.partner_id:
        print(f"No partner for {profile.email}, skipping")
        continue
    
    # Check if res.users already exists
    existing_user = env['res.users'].search([
        '|', ('login', '=', profile.email), ('partner_id', '=', profile.partner_id.id)
    ], limit=1)
    
    if existing_user:
        profile.user_id = existing_user.id
        print(f"Linked existing user {existing_user.id} to profile {profile.email}")
    else:
        try:
            new_user = env['res.users'].with_context(no_reset_password=True).create({
                'name': f"{profile.nombre} {profile.apellido}",
                'login': profile.email,
                'password': profile.password,
                'partner_id': profile.partner_id.id,
                'groups_id': [(6, 0, [portal_group.id])],
            })
            profile.user_id = new_user.id
            print(f"Created portal user {new_user.id} for {profile.email}")
        except Exception as e:
            print(f"Error for {profile.email}: {e}")

env.cr.commit()
print("Migration complete!")
