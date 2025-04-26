"""
Abheek Tuladhar
HCP Period 4
Pokemon Matching Game
Play a classic matching game with the Eeveelutions!
"""

import pygame, sys, random, time
pygame.init()

WIDTH = 800
HEIGHT = WIDTH * 1.2

SIZE = (WIDTH, HEIGHT)
SURFACE = pygame.display.set_mode(SIZE)

pygame.display.set_caption("Pokemon Matching Game")

BLACK    = (0, 0, 0)
WHITE    = (255, 255, 255)

#Load images
BACK     = pygame.image.load("PokemonImages/Back.jpg").convert_alpha()
ESPEON   = pygame.image.load("PokemonImages/Espeon.jpg").convert_alpha()
FLAREON  = pygame.image.load("PokemonImages/Flareon.jpg").convert_alpha()
GLACEON  = pygame.image.load("PokemonImages/Glaceon.jpg").convert_alpha()
JOLTEON  = pygame.image.load("PokemonImages/Jolteon.jpg").convert_alpha()
LEAFEON  = pygame.image.load("PokemonImages/Leafeon.jpg").convert_alpha()
SYLVEON  = pygame.image.load("PokemonImages/Sylveon.jpg").convert_alpha()
UMBREON  = pygame.image.load("PokemonImages/Umbreon.jpg").convert_alpha()
VAPOREON = pygame.image.load("PokemonImages/Vaporeon.jpg").convert_alpha()
EEVEE    = pygame.image.load("PokemonImages/Eevee.png").convert_alpha()
BG       = pygame.image.load("PokemonImages/BG.jpg").convert_alpha()

SIZE = 120
#1:1.46 is the ratio of pokemon cards width to height
BACK     = pygame.transform.scale(BACK, (SIZE, SIZE * 1.46))
ESPEON   = pygame.transform.scale(ESPEON, (SIZE, SIZE * 1.46))
FLAREON  = pygame.transform.scale(FLAREON, (SIZE, SIZE * 1.46))
GLACEON  = pygame.transform.scale(GLACEON, (SIZE, SIZE * 1.46))
JOLTEON  = pygame.transform.scale(JOLTEON, (SIZE, SIZE * 1.46))
LEAFEON  = pygame.transform.scale(LEAFEON, (SIZE, SIZE * 1.46))
SYLVEON  = pygame.transform.scale(SYLVEON, (SIZE, SIZE * 1.46))
UMBREON  = pygame.transform.scale(UMBREON, (SIZE, SIZE * 1.46))
VAPOREON = pygame.transform.scale(VAPOREON, (SIZE, SIZE * 1.46))
EEVEE    = pygame.transform.scale(EEVEE, (80, 80))
BG       = pygame.transform.scale(BG, (WIDTH, HEIGHT))

#Sounds
winSound    = pygame.mixer.Sound("PokemonSounds/win.mp3")
bgSound     = pygame.mixer.Sound("PokemonSounds/bg.mp3")
cardClicked = pygame.mixer.Sound("PokemonSounds/cardClicked.mp3")

winSound.set_volume(0.5)
bgSound.set_volume(0.5)
cardClicked.set_volume(0.5)

bgSound.play(-1) #Play the background music in a loop


def show_message(words, font_name, size, x, y, color, bg=None, hover=False):
    """
    Credit to programming mentor, Valerie Klosky

    Parameters:
    -----------
    words : str
        The text to be displayed.
    font_name : str
        The name of the font to use.
    size : int
        The size of the font.
    x : int
        The x-coordinate of the center of the text.
    y : int
        The y-coordinate of the center of the text.
    color : tuple
        The RGB color of the text.
    bg : tuple, optional
        The RGB background color of the text. Defaults to None.
    hover : bool, optional
        Whether to change the text color on hover. Defaults to False.

    Returns:
    --------
    text_bounds : Rect
        The bounding box of the text.
    """

    font = pygame.font.SysFont(font_name, size, True, False)
    text_image = font.render(words, True, color, bg)
    text_bounds = text_image.get_rect()  #bounding box of the text image
    text_bounds.center = (x, y)  #center text within the bounding box

    #find position of mouse pointer
    mouse_pos = pygame.mouse.get_pos()  #returns (x,y) of mouse location

    if text_bounds.collidepoint(mouse_pos) and bg != None and hover:
        #Regenerate the image on hover
        text_image = font.render(words, True, bg, color) #swap bg and text color

    SURFACE.blit(text_image, text_bounds) #render on screen

    return text_bounds #bounding box returned for collision detection


def rank(attempts):
    """
    Returns a string based on the number of attempts made to win the game.

    Parameters:
    ----------
    attempts : int
        The number of attempts made to win the game.

    Returns:
    -------
    string
        A string representing the rank based on the number of attempts.
    """

    if attempts <= 8:
        return "DANG!"
    elif attempts <= 10:
        return "Good!"
    elif attempts <= 14:
        return "Nice!"
    elif attempts <= 18:
        return "Ok!"
    elif attempts <= 21:
        return "Average!"
    else:
        return "Bad Luck or just Bad?"


def drawScreen(cards, indexes, rects, gameOver, attempts, matches, average):
    """
    Draws the game screen with the current state of the cards and other information.

    Parameters:
    -----------
    cards : list
        A 2D list representing the current state of the cards.
    indexes : list
        A list of integers representing the indices of the flipped cards.
    rects : list
        A list of pygame Rect objects representing the positions of the cards.
    gameOver : bool
        A boolean indicating whether the game is over.
    attempts : int
        The number of attempts made to win the game.
    matches : int
        The number of matches made by the player.

    Returns:
    --------
    None
    """

    SURFACE.blit(BG, (0, 0))

    show_message("Matching Game", "Consolas", 50, WIDTH//2 + 90, HEIGHT//18, BLACK)
    show_message(f"Attempts: {attempts}", "Consolas", 30, WIDTH//2 - 110, HEIGHT- 30, BLACK, WHITE)
    show_message(f"Matches: {matches}", "Consolas", 30, WIDTH//2 + 110, HEIGHT- 30, BLACK, WHITE)
    show_message(f"Average Score: {average}", "Consolas", 30, WIDTH//2, HEIGHT-70, BLACK, WHITE)

    SURFACE.blit(EEVEE, (WIDTH//2 - 170, HEIGHT//18 - 50))

    # Get mouse position for hover effect
    mouse_pos = pygame.mouse.get_pos()

    for i in range(len(rects)):
        card_value = cards[i//4][i%4] #i//4 gives the row, i%4 gives the column
        rect = rects[i]

        if card_value != None:
            if i in indexes:
                SURFACE.blit(card_value, (rect.x, rect.y)) #draw the card where the rect was if it is flipped
            else:
                #Add hover
                if rect.collidepoint(mouse_pos):
                    #Make shadow rect
                    shadow_rect = pygame.Rect(rect.x + 3, rect.y + 3, rect.width, rect.height)
                    pygame.draw.rect(SURFACE, (150, 150, 150), shadow_rect)

                    #Draw the card slightly offset
                    card_rect = pygame.Rect(rect.x - 5, rect.y - 5, rect.width, rect.height)
                    SURFACE.blit(BACK, card_rect)
                else:
                    SURFACE.blit(BACK, (rect.x, rect.y)) #Blit it in the normal spot

    if gameOver:
        show_message("You Win!", "Consolas", 50, WIDTH//2, HEIGHT//2, BLACK, WHITE)
        show_message("Press Enter to play again", "Consolas", 30, WIDTH//2, HEIGHT//2 + 50, BLACK, WHITE)
        show_message(f"Score Ranking: {rank(attempts)}", "Consolas", 30, WIDTH//2, HEIGHT//2 + 100, BLACK, WHITE)
        #Stop backgound music and play win sound
        bgSound.stop()
        winSound.play(-1)


def shuffleCards():
    """
    Shuffles the cards and returns a 2D list representing the shuffled cards.

    Parameters:
    -----------
    None

    Returns:
    -------
    cards : list
        A 2D list representing the shuffled cards.
    """

    choices = [ESPEON, FLAREON, GLACEON, JOLTEON, LEAFEON, SYLVEON, UMBREON, VAPOREON, ESPEON, FLAREON, GLACEON, JOLTEON, LEAFEON, SYLVEON, UMBREON, VAPOREON]
    random.shuffle(choices) #Shuffle the cards so rounds are different each time

    cards = []
    for i in range(0, 16, 4):
        cards.append(choices[i:i+4]) #Appends a list of 4 of the shuffled cards to the 2D list

    return cards


def startVariables():
    """
    Initializes the game variables and returns them.

    Parameters:
    -----------
    None

    Returns:
    -------
    cards : list
        A 2D list representing the shuffled cards.
    flipped_cards : list
        A list of pygame Rect objects representing the flipped cards.
    rects : list
        A list of pygame Rect objects representing the positions of the cards.
    indexes : list
        A list of integers representing the indices of the flipped cards.
    gameOver : bool
        A boolean indicating whether the game is over.
    attempts : int
        The number of attempts made to win the game.
    matches : int
        The number of matches made by the player.
    """

    #Didn't want to repeat the code in main() so I made this function to initialize the variables
    cards = shuffleCards()
    flipped_cards = []
    rects = []
    indexes = []
    gameOver = False
    attempts = 0
    matches = 0
    average_done = False

    #This creates the rects for the click-detection
    for i in range(4):
        for j in range(4):
            rects.append(pygame.Rect(i*WIDTH//5 + 100, j*HEIGHT//5 + 100, SIZE, SIZE * 1.46))

    return cards, flipped_cards, rects, indexes, gameOver, attempts, matches, average_done


def main():
    """
    Main function, where all the action happens

    Parameters:
    -----------
    None

    None
    """

    #Initialize the game variables
    cards, flipped_cards, rects, indexes, gameOver, attempts, matches, average_done = startVariables()

    #These variables don't change at the start of each round, thus they aren't in the startVariables() function
    average = "N/A"
    average_score = 0
    rounds = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE: #end game
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and gameOver:
                cards, flipped_cards, rects, indexes, gameOver, attempts, matches, average_done = startVariables()
                winSound.stop()
                bgSound.play(-1)  # Restart background music

            if event.type == pygame.MOUSEBUTTONDOWN and not gameOver:
                mouse_pos = pygame.mouse.get_pos()
                for rect in rects:
                    try:
                        if rect.collidepoint(mouse_pos) and rect not in flipped_cards: #If the card isn't already flipped and got hit
                            cardClicked.play()
                            flipped_cards.append(rect) #Add it to the flipped cards list
                            indexes.append(rects.index(rect)) #Indexes hold which index of cards are flipped

                            if len(flipped_cards) == 2:
                                SURFACE.fill(WHITE)
                                attempts += 1
                                drawScreen(cards, indexes, rects, gameOver, attempts, matches, average) #Otherwise, there would be a 1 second delay in the score updating
                                pygame.display.update()

                                if cards[indexes[0]//4][indexes[0]%4] == cards[indexes[1]//4][indexes[1]%4]: #If the cards match
                                    matches += 1
                                    drawScreen(cards, indexes, rects, gameOver, attempts, matches, average) #Otherwise, there would be a 1 second delay in the score updating
                                    pygame.display.update()

                                    time.sleep(1) #Wait for 1 second before flipping the cards back to show user what they are
                                    for i in indexes:
                                        cards[i//4][i%4] = None #Remove the cards from the list

                                    flipped_cards = []
                                    indexes = []

                                else:
                                    time.sleep(1) #Wait for 1 second before flipping the cards back to show user what they are
                                    flipped_cards = []
                                    indexes = []

                    except AttributeError:
                        # This error occurs when the rect is None (already matched)
                        flipped_cards = []
                        indexes = []

            game_over_holder = True #Assume the game is over until proven otherwise

            for row in cards:
                for card in row:
                    if card != None:
                        game_over_holder = False
                        break
                if not game_over_holder:
                    break

            gameOver = game_over_holder #If all the cards are matched, game is over

            if gameOver and not average_done:
                average_score += attempts
                rounds += 1
                average = average_score/rounds
                average_done = True

        SURFACE.fill(WHITE)
        drawScreen(cards, indexes, rects, gameOver, attempts, matches, average)
        pygame.display.update()


main()
