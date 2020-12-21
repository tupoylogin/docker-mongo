db.getSiblingDB('admin').createUser(
    {
        user: "root2",
        password: "root2",
        roles: [
            {
                role: "userAdminAnyDatabase",
                db: "admin"
            }]
    })