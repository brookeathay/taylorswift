import pandas as pd
import random

"""
I plan to create a Taylor Swift–themed Python program that helps users determine their favorite Taylor Swift song and album.
The program will run in a game format, guiding the user through a series of song brackets in which they rate songs.csv against each other.

The bracket process will be organized by album. First, the user will select an album and rate songs.csv from that album on a thirteen-point scale
(13 is Taylor Swift’s lucky number) to determine their favorite song within that album.
If two or more songs.csv receive the same rating, the user will choose which song wins using a bracket.
Each rating will be recorded and associated with the song’s album.
After completing brackets for multiple albums, the program will calculate the average rating for each album based on the user’s song ratings.
The favorite song from each album will then advance to a final bracket,
where the user will determine their overall favorite song by comparing the top songs.csv from each album.

Finally, the program will display the user’s favorite song overall and identify the user’s favorite album based on the highest average album rating.
The program will also generate a playlist recommendation featuring the user’s top 20 songs.csv.
I plan to include additional features while writing the program to make it interactive and fun.
"""


def get_albums(songs):
    """Returns all the album titles"""
    return songs['Album'].unique()


def print_albums(albums):
    """prints all the album titles"""
    print('Taylor Swift Albums: ')
    i = 1
    for album in albums:
        print(f'{i}. {album}')
        i += 1


def choose_album(albums):
    """User inputs chosen album number to rate using a valid number (1-12) and it will select corresponding album"""
    while True:
        choice = input("Select an album by number: ")
        if choice.isdigit():
            choice = int(choice)
            easter_eggs()
            if 1 <= choice <= len(albums):
                return albums[choice - 1]
        print("Invalid choice. Try again")


def get_songs_from_album(songs, album):
    """gets songs from choice album and returns as list of songs"""
    return songs[songs['Album'] == album]["Song"].tolist()


def print_songs(album_songs, album):
    """prints all the songs in the chosen album"""
    print(f'Songs in {album}: ')
    for song in album_songs:
        print(f'- {song}')


def rate_songs(song_list):
    """goes through all songs in choice album and rates on
    a scale from 1 to 13. If rating = 13, you get a message and increase lucky_count"""
    ratings = {}
    lucky_count = 0
    for song in song_list:
        while True:
            rating = input(f"✨Rate '{song}' from 1-13: ")
            if rating.isdigit():
                rating = int(rating)
                if 1 <= rating <= 13:
                    ratings[song] = rating
                    if rating == 13:
                        print("💎Lucky 13! Taylor would approve.")
                        lucky_count += 1
                        easter_eggs()
                    break
            print("Invalid rating. Try again.")
    return ratings, lucky_count


def print_ratings(ratings):
    """prints all the ratings from choice album songs"""
    print("Your ratings: ")
    for song, rating in ratings.items():
        print(f'✨{song}: {rating}')


def get_top_songs(ratings):
    """gets the top rated songs from choice album"""
    max_score = max(ratings.values())
    return [song for song, score in ratings.items() if score == max_score]


def bracket_winner(song_list):
    """Starts with first song in the list and puts against challenger (next song)
    The user picks between the songs and their choice become the winner and faces the next song
    in the list until it finishes. It returns overall winner"""
    songs = song_list.copy()
    random.shuffle(songs)
    winner = songs[0]
    for challenger in songs[1:]:
        print(f'Which do you prefer?')
        print(f'1. {winner}')
        print(f'2. {challenger}')
        while True:
            choice = input("Choose 1 or 2: ")
            if choice in ['1', '2']:
                break
            print("Invalid choice. Try again.")
        if choice == '2':
            winner = challenger
    return winner


def print_final_songs(final_songs):
    """prints the top song from each album"""
    print("Final bracket!")
    for song in final_songs:
        print(f'- {song}')


def calculate_album_average(ratings):
    """Calculates the albums average rating from sum of each song rating divided by length of album"""
    return sum(ratings.values()) / len(ratings)


def get_favorite_album(album_average_ratings):
    """Goes through album average rating to find which album has
    the greatest average rating and returns favorite album"""
    max_rating = None
    max_album = None
    for album, rating in album_average_ratings.items():
        if max_rating is None or rating > max_rating:
            max_rating = rating
            max_album = album
    return max_rating, max_album


def album_personality_result(max_album):
    """Based on favorite album, gives personality message, recommended artist, and swiftie title """
    album = max_album.lower()
    album_data = {
        "taylor swift": (
            "🌻 You're heartfelt and loyal. You believe in fairytales, handwritten notes, and love that feels forever.",
            "Olivia Dean", "The Daydream Believer"),
        "fearless": ("✨ You're brave in love. You run toward butterflies, not away from them.", "Sabrina Carpenter",
                     "The Golden Romantic"),
        "speak now": (
            "💜 You're dramatic in the best way. You feel everything deeply and say what others are too scared to.",
            "Conan Gray", "The Confessional Poet"),
        "red": ("🧣 You love hard and remember everything. Passionate, nostalgic, and a little chaotic.",
                "Gracie Abrams", "The Passionate Archivist"),
        "1989": ("🕶 You're confident and independent. Reinvention looks good on you.", "Tate McRae",
                 "The Pop Visionary"),
        "reputation": ("🐍 You're bold, magnetic, and misunderstood. You protect your heart but love fiercely.",
                       "Stray Kids", "The Untouchable Icon"),
        "lover": ("💘 You're soft but strong. Romantic, hopeful, and unapologetically emotional.", "ROSÉ",
                  "The Hopeless Romantic"),
        "folklore": ("🌲 You're introspective and poetic. You find beauty in quiet moments and untold stories.",
                     "Bon Iver", "The Story Weaver"),
        "evermore": (
            "🍂 You're thoughtful and emotionally layered. You sit with your feelings instead of running from them.",
            "Lana Del Rey", "The Autumn Philosopher"),
        "midnights": ("🌙 You're a late-night thinker. Self-aware, reflective, and a little mysterious.", "Djo",
                      "The Midnight Mastermind"),
        "the tortured poets department": (
            "🖋 You're intense and expressive. You turn heartbreak into art and overthink in italics.", "Gracie Abrams",
            "The Tortured Wordsmith"),
        "life of a showgirl": (
            "🎭 You live for the spotlight but feel everything when the curtain falls. Glitter on the outside, depth on the inside. You know how to perform — but only a few people see the real you.",
            "Chappell Roan", "The Spotlight Siren")
    }
    if album in album_data:
        message, artist, title = album_data[album]
        print("\n✨ YOUR ERA HAS BEEN CHOSEN ✨\n")
        print(message)
        print(f'\n👑 Your Swiftie Title: {title}')
        print(f'\n🎧 Recommended Artist: {artist}\n')
    else:
        print("You have elite taste. 🎶")


def mastermind_mode():
    """prints secret message if meet mastermind mode qualifications"""
    print("\n⚠️ MASTER MIND MODE ACTIVATED ⚠️\n")
    print("You didn’t just rate songs...")
    print("You calculated outcomes.")
    print("You noticed patterns.")
    print("You played strategically.")
    print("You are a mastermind. \n")
    print("👑 Swiftie Rank: The Architect")
    print("💎 Rarity: Legendary")
    print("🧠 Era Energy: Mastermind")
    print("\nYou were never guessing.")
    print("You were always in control.\n")
    input("Press enter to continue")


def easter_eggs():
    """randomly generates Easter egg 20% percent of the time it is called"""
    eggs = [
        "🐍 A snake slithers by... Reputation energy detected.",
        "🕯 A cardigan appears out of nowhere. Folklore found you.",
        "💄 You check the mirror. Red lipstick era activated.",
        "🌙 It's 2:13 AM. You should be sleeping. You're not.",
        "📓 You found a hidden lyric in the margins.",
        "🎭 The spotlight flickers. Showgirl mode watching.",
        "🧣 You smell autumn air and unfinished business.",
        "💎 A mastermind never reveals their strategy."
    ]
    if random.random() < 0.20:
        print("\n💎 EASTER EGG UNLOCKED 💎")
        print(random.choice(eggs))
        print()


def get_remaining(albums, album_average_ratings):
    """gets the remaining albums that have not been chosen and returns a list"""
    remaining = [a for a in albums if a not in album_average_ratings]
    return remaining


def main():
    try:
        songs = pd.read_csv("songs.csv")
    except FileNotFoundError:
        print("songs.csv not found.")
        return
    albums = get_albums(songs)
    final_songs = []
    album_average_ratings = {}
    all_song_ratings = {}
    lucky_13_count = 0
    while True:
        print_albums(albums)
        selected_album = choose_album(albums)
        if selected_album in album_average_ratings:
            print("You already rated this album!")
            continue
        print(f'🎤You selected: {selected_album}!')
        album_songs = get_songs_from_album(songs, selected_album)
        print_songs(album_songs, selected_album)
        ratings, album_lucky_count = rate_songs(album_songs)
        lucky_13_count += album_lucky_count
        top_songs = get_top_songs(ratings)
        all_song_ratings.update(ratings)
        if len(top_songs) == 1:
            winner = top_songs[0]
        else:
            winner = bracket_winner(top_songs)
        print(f'\n🎤{selected_album} winner: {winner}\n')
        final_songs.append(winner)
        average_rating = calculate_album_average(ratings)
        album_average_ratings[selected_album] = average_rating
        print(f'✨{selected_album} average rating is {average_rating:.2f}\n')
        easter_eggs()
        input("Press enter to continue")
        albums = get_remaining(albums, album_average_ratings)
        if len(albums) == 0:
            print("\n✨You've rated all albums!✨\n")
            break
        decision = input('\nDo you want to do another Album (Yes/No)? ')
        if decision.lower() == 'no':
            break
    print('\n🎤 THE ULTIMATE ERA SHOWDOWN 🎤\n')
    print_final_songs(final_songs)
    if len(final_songs) == 1:
        final_winner = final_songs[0]
    else:
        final_winner = bracket_winner(final_songs)
    print(f'\n🎤Your favorite Taylor Swift song is {final_winner}!\n')
    input("Press enter to continue!")
    max_rating, max_album = get_favorite_album(album_average_ratings)
    print(f'\n✨Your favorite Taylor Swift album is {max_album} with an average rating of {max_rating}\n')
    album_personality_result(max_album)
    top_50 = sorted(all_song_ratings.items(), key=lambda x: x[1], reverse=True)[0:50]
    input("Press enter to continue!")
    print("\n🎤Your Top 50 Songs: ")
    for song, rating, in top_50:
        print(f'\n{song} ({rating})')
    playlist_df = pd.DataFrame(top_50, columns=["Song", "Rating"])
    playlist_df.to_csv("your_top_50_taylor_playlist.csv", index=False)
    print("Playlist saved!")
    if lucky_13_count >= 13 and max_rating >= 12 and len(album_average_ratings) == len(albums):
        mastermind_mode()


if __name__ == '__main__':
    main()
