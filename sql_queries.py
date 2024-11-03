
CHOOSE_COUPLE_SQL =  '''
    SELECT a1.name AS male_name, a1.image_path AS male_image_path,
           a2.name AS female_name, a2.image_path AS female_image_path
    FROM Actors a1
    JOIN Actors a2 ON a1.gender != a2.gender
    WHERE a1.gender = 'M' AND a2.gender = 'F'  -- Filter for distinct genders after joining
    LIMIT 1;
'''

CREATE_TABLES = """
                CREATE TABLE Tasks (
                    name TEXT NOT NULL UNIQUE,
                    time INT NOT NULL,
                    energy INT NOT NULL,
                    image_path TEXT NOT NULL,
                    PRIMARY KEY (name)
                );
                INSERT INTO Tasks(name, time, energy, image_path) VALUES                
                    ('Cooking', 3, 3, 'assets/cooking.png'),
                    ('Cleaning', 3, 5 , 'assets/mop.png'),
                    ('GroceryShopping', 2, 2 , 'assets/vegetable.png'),
                    ('Child-care', 7,7 , 'assets/crawl.png'),
                    ('Elderly-care', 7,7 , 'assets/elderly.png'),
                    ('Garden', 5,4 , 'assets/gardening.png'),
                    ('PetCare', 1,1 , 'assets/dog.png'),
                    ('PayBills', 1,2 , 'assets/bill.png'),
                    ('Laundry', 2,3 , 'assets/laundry-machine.png'),
                    ('Washdishes', 2,1 , 'assets/washdishes.png'),
                    ('Care', 7,7, 'assets/care.png');
                
                CREATE TABLE Actors (
                    name TEXT NOT NULL UNIQUE,
                    gender Text NOT NULL,
                    image_path TEXT NOT NULL,
                    PRIMARY KEY (name)
                );
                    INSERT INTO Actors(name, gender,  image_path) VALUES                
                    ('black_man', 'M' ,'assets/dark_man.png'),
                    ('black_woman','F' ,'assets/black_woman.png'),
                    ('caucasian_male', 'M', 'assets/caucasian_male.png'),
                    ('caucasian_female','F', 'assets/caucasian_female.png'),
                    ('asian_female', 'F', 'assets/asian_female.png'),
                    ('asian_male', 'M', 'assets/asian_male.png');
            """

def get_texture(set_of_names):
    return f"""
            SELECT name, image_path
            FROM Tasks
            WHERE name IN {set_of_names}
            """