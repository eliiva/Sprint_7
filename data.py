from utils import generate_random_string

wrong_payload_for_create = [
    {
        "password": generate_random_string(10),
        "firstName": generate_random_string(10)
    },
    {
        "login": generate_random_string(10),
        "firstName": generate_random_string(10)
    }
]

create_order_data = {
    "firstName": "Naruto",
    "lastName": "Uchiha",
    "address": "Konoha, 142 apt.",
    "metroStation": 4,
    "phone": "+7 800 355 35 35",
    "rentTime": 5,
    "deliveryDate": "2020-06-06",
    "comment": "Saske, come back to Konoha"
}

create_order_colors = [["GREY"], ["BLACK"], ["GREY", "BLACK"]]
