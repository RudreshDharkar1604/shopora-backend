async def get_user_details_by_id(user_id,db):
    query = """
        SELECT user_id,first_name,last_name,mobile_no,email,address,age,is_active,role_name,description
        FROM ecom.users as u
        INNER JOIN ecom.roles as r 
            ON u.role_id = r.role_id
        WHERE user_id = :user_id
       """
    result = await db.fetch_one(query, {"user_id": user_id})
    return result

async def update_user_by_id(user_id,first_name,last_name,mobile_no,email,address,age,db):
    query = """
        UPDATE ecom.users
        SET first_name = :first_name,
            last_name = :last_name,
            mobile_no = :mobile_no,
            email = :email,
            address = :address,
            age = :age,
            updated_at = NOW()
        WHERE user_id = :user_id
        RETURNING user_id,first_name,last_name,mobile_no,email,address,age
       """
    result = await db.execute(query, {
        "user_id": user_id, 
        "first_name": first_name,
        "last_name": last_name, 
        "mobile_no": mobile_no,
        "email": email, 
        "address": address, 
        "age": age
    })
    return result