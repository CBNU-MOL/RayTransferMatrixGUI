# 필요한 optics 정보 추가 가능
# 예시
# "LASESF-39": {
#         "n_air": 1.0,
#         "n_N_BK7": 1.5106,
#         "rad_curv": 38.6,
#         "c_thick": 4.1,
#         "f": 74.8,   
#         "fb": 72.0
#     }

optics_data = {
    "LA1050-B": {
        "n_air": 1.0,
        "n_N_BK7": 1.515,
        "rad_curv": 51.5,
        "c_thick": 9.7,
        "f": 99.7,
        "fb": 93.3
    },

    "LA1509-B": {
        "n_air": 1.0,
        "n_N_BK7": 1.515,
        "rad_curv": 51.5,
        "c_thick": 3.6,
        "f": 99.7,
        "fb": 97.3
    },
    "LA1805-B": {
        "n_air": 1.0, 
        "n_N_BK7": 1.515,
        "rad_curv": 15.5,
        "c_thick": 8.6,
        "f": 29.9,
        "fb": 24.2
    },

    "LA1131-B": {
        "n_air": 1.0, 
        "n_N_BK7": 1.515,
        "rad_curv": 25.8,
        "c_thick": 5.3,
        "f": 49.8,
        "fb": 46.3
    },

    "LA1608-B": {
        "n_air": 1.0, 
        "n_N_BK7": 1.515,
        "rad_curv": 38.6,
        "c_thick": 4.1,
        "f": 74.8,
        "fb": 72.0
    },

    "LA1433-B": {
        "n_air": 1.0, 
        "n_N_BK7": 1.515,
        "rad_curv": 77.3,
        "c_thick": 3.1,
        "f": 149.5,
        "fb": 147.5
    },



    "LA1708-B": {
        "n_air": 1.0, 
        "n_N_BK7": 1.515,
        "rad_curv": 103.0,
        "c_thick": 2.8,
        "f": 199.3,
        "fb": 197.5
    },

    "None": {
        "n_air": 1.0, 
        "n_N_BK7": 1,
        "rad_curv": 1,
        "c_thick": 0,
        "f": 0,
        "fb": 0
    },
}

if __name__ == "__main__":
    ''''''
    first_key = next(iter(optics_data))
    print(first_key)

    first_data =  optics_data[first_key]

    print(first_data)

    second_data =  first_data.get('n_air')
    print(second_data)

    second_data2 = first_data["n_air"]
    print(second_data2)

    print(optics_data.items())
    for key, val in optics_data.items():
        print(key)
        print(val["n_air"])