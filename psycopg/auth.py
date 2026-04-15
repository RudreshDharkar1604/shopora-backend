from core.security import hash_password


async def check_user_exists(email, mobile_no, db):
    query = "SELECT user_id,password FROM ecom.users WHERE email = :email"
    params = {"email": email}
    if mobile_no:
        query += " OR mobile_no = :mobile_no"
        params["mobile_no"] = mobile_no
    result = await db.fetch_one(query, params)
    print("results are ",result)
    return result


async def register_user(
        first_name,last_name, mobile_no,email, password, 
        address, age, is_active, role , db
    ):
    hashed_password = hash_password(password)
    query = """
        INSERT INTO ecom.users (first_name, last_name, mobile_no, email, password, address, age, is_active,role_id) 
        VALUES (:first_name, :last_name, :mobile_no, :email, :password, :address, :age, :is_active, :role_id)
        RETURNING user_id
    """
    result = await db.execute(query, {
        "first_name": first_name,
        "last_name": last_name,
        "mobile_no": mobile_no,
        "email": email,
        "password": hashed_password,
        "address": address,
        "age": age,
        "is_active": is_active,
        "role_id": role
    })
    return result

async def login_controller(email,password,db):
    query = "SELECT user_id,mobile_no,email,is_active FROM ecom.users WHERE email = :email AND password = :password"
    result = await db.fetch_one(query, {"email": email, "password": password})
    return result

