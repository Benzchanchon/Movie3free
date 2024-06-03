import pandas as pd

# สร้างชุดข้อมูล
data = {
    'Title': [
        'Mad Max: Fury Road', 'John Wick', 'The Dark Knight', 'Die Hard', 'Gladiator', 'Inception', 'The Avengers', 'Terminator 2: Judgment Day', 'Matrix', 'Mission: Impossible - Fallout',
        'The Hangover', 'Superbad', 'Step Brothers', 'Anchorman: The Legend of Ron Burgundy', 'Bridesmaids', 'Dumb and Dumber', 'Borat', 'Groundhog Day', 'Ferris Bueller\'s Day Off', 'The Big Lebowski',
        'The Shawshank Redemption', 'Forrest Gump', 'The Godfather', 'Fight Club', 'Good Will Hunting', 'A Beautiful Mind', 'Schindler\'s List', '12 Years a Slave', 'The Green Mile', 'The Pursuit of Happyness',
        'The Exorcist', 'A Nightmare on Elm Street', 'Halloween', 'The Conjuring', 'It', 'Get Out', 'Hereditary', 'The Shining', 'Paranormal Activity', 'The Ring',
        'Interstellar', 'Blade Runner 2049', 'The Matrix', 'Star Wars: Episode IV - A New Hope', 'The Terminator', 'Avatar', 'Jurassic Park', 'E.T. the Extra-Terrestrial', 'Back to the Future', 'Inception',
        'The Lord of the Rings: The Fellowship of the Ring', 'Harry Potter and the Sorcerer\'s Stone', 'Pan\'s Labyrinth', 'The Chronicles of Narnia: The Lion, the Witch and the Wardrobe', 'The Hobbit: An Unexpected Journey', 'Alice in Wonderland', 'Stardust', 'Pirates of the Caribbean: The Curse of the Black Pearl', 'The Princess Bride', 'Beauty and the Beast',
        'Titanic', 'The Notebook', 'Pride and Prejudice', 'La La Land', 'Before Sunrise', 'A Walk to Remember', 'Crazy Rich Asians', 'Love Actually', 'The Fault in Our Stars', '500 Days of Summer',
        'Se7en', 'The Usual Suspects', 'Sherlock Holmes', 'Gone Girl', 'The Girl with the Dragon Tattoo', 'Zodiac', 'The Departed', 'Memento', 'Prisoners', 'Mystic River',
        'The Sound of Music', 'Les Misérables', 'Chicago', 'La La Land', 'Mamma Mia!', 'West Side Story', 'The Greatest Showman', 'Moulin Rouge!', 'Grease', 'Beauty and the Beast',
        'The Last Dance', 'Blackfish', 'March of the Penguins', 'Free Solo', 'Planet Earth II', 'The Social Dilemma', '13th', 'Won\'t You Be My Neighbor?', 'Jiro Dreams of Sushi', 'An Inconvenient Truth',
        'The Lion King', 'Finding Nemo', 'Toy Story', 'Frozen', 'The Incredibles', 'Moana', 'Shrek', 'Aladdin', 'Coco', 'Beauty and the Beast',
        'Spirited Away', 'Toy Story', 'Up', 'The Lion King', 'Finding Nemo', 'How to Train Your Dragon', 'Frozen', 'Despicable Me', 'The Secret Life of Pets', 'Zootopia'
    ],
    'Genres': [
        'Action', 'Action', 'Action|Drama', 'Action', 'Action|Drama', 'Action|Sci-Fi', 'Action|Sci-Fi', 'Action|Sci-Fi', 'Action|Sci-Fi', 'Action|Adventure',
        'Comedy', 'Comedy', 'Comedy', 'Comedy', 'Comedy|Romance', 'Comedy', 'Comedy', 'Comedy|Romance', 'Comedy', 'Comedy',
        'Drama', 'Drama|Romance', 'Drama|Crime', 'Drama|Thriller', 'Drama', 'Drama', 'Drama|History', 'Drama|History', 'Drama', 'Drama|Biography',
        'Horror', 'Horror', 'Horror', 'Horror', 'Horror', 'Horror|Thriller', 'Horror|Drama', 'Horror|Thriller', 'Horror|Thriller', 'Horror|Mystery',
        'Sci-Fi|Adventure', 'Sci-Fi', 'Sci-Fi|Action', 'Sci-Fi|Fantasy', 'Sci-Fi|Action', 'Sci-Fi|Fantasy', 'Sci-Fi|Adventure', 'Sci-Fi|Fantasy', 'Sci-Fi|Comedy', 'Sci-Fi|Action',
        'Fantasy|Adventure', 'Fantasy|Adventure', 'Fantasy|Drama', 'Fantasy|Adventure', 'Fantasy|Adventure', 'Fantasy|Adventure', 'Fantasy|Romance', 'Fantasy|Adventure', 'Fantasy|Romance', 'Fantasy|Romance',
        'Romance|Drama', 'Romance|Drama', 'Romance|Drama', 'Romance|Musical', 'Romance|Drama', 'Romance|Drama', 'Romance|Comedy', 'Romance|Comedy', 'Romance|Drama', 'Romance|Comedy|Drama',
        'Mystery|Crime|Thriller', 'Mystery|Crime|Thriller', 'Mystery|Crime', 'Mystery|Thriller', 'Mystery|Crime|Thriller', 'Mystery|Crime', 'Mystery|Crime|Thriller', 'Mystery|Thriller', 'Mystery|Crime|Thriller', 'Mystery|Crime|Drama',
        'Musical|Drama', 'Musical|Drama', 'Musical|Comedy', 'Musical|Romance', 'Musical|Romance|Comedy', 'Musical|Drama', 'Musical|Drama', 'Musical|Drama|Romance', 'Musical|Romance|Comedy', 'Musical|Romance|Fantasy',
        'Documentary', 'Documentary', 'Documentary', 'Documentary', 'Documentary', 'Documentary', 'Documentary', 'Documentary', 'Documentary', 'Documentary',
        'Family|Animation', 'Family|Animation', 'Family|Animation', 'Family|Animation|Musical', 'Family|Animation', 'Family|Animation', 'Family|Animation', 'Family|Animation', 'Family|Animation', 'Family|Animation',
        'Animation|Fantasy', 'Animation|Family', 'Animation|Family|Adventure', 'Animation|Family', 'Animation|Family', 'Animation|Family', 'Animation|Family', 'Animation|Family', 'Animation|Family|Comedy', 'Animation|Family'
    ]
}

# สร้าง DataFrame
df = pd.DataFrame(data)

# บันทึก DataFrame เป็นไฟล์ Excel
excel_path = 'C:/Users/chanc/OneDrive/Desktop/movies_with_genres_10_per_category.xlsx'
df.to_excel(excel_path, index=False)

excel_path
