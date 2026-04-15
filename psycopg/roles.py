async def get_all_roles(db):
    query = """
                SELECT role_id,role_name,description  
                FROM ecom.roles
                ORDER BY role_id ASC 
            """
    result = await db.fetch_all(query)
    return result


async def create_a_new_role(role_name,role_description,db,user_id=None):
    query = """
        INSERT INTO ecom.roles(role_name,description)
        VALUES(:role_name,:role_description)
        RETURNING role_id
    """
    print(f"Role name is {role_name} & {role_description} description .")
    result = await db.execute(query,{"role_name":role_name,"role_description":role_description})
    return result