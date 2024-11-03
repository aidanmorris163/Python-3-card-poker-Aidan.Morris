import random 

 

 

# Asking EA player whether or not they want to place bet 

 

def askbet(num_players): 

    ante_bets = [] 

    pair_plus_bets = [] 

    for i in range(num_players): 

        ante_bet = float(input(f"Player {i + 1}, what is your ante bet? $"))           # Asking EA player  

        decision = input("Would you like to place a Pair Plus bet? (yes/no) ") 

 

        if decision.lower() == 'yes': 

            pair_plus_bet = float(input("What amount is your Pair Plus bet? $")) 

        else: 

            pair_plus_bet = 0 

            print("No Pair Plus bet placed.") 

 

        ante_bets.append(ante_bet) 

        pair_plus_bets.append(pair_plus_bet)       # Calling back players desions  

 

    return ante_bets, pair_plus_bets 

def set_number_of_players():
    while True:

            num_players = int(input("Enter the number of players (between 2 and 4): "))

            if 2 <= num_players <= 4:

                return num_players

            else:
                print("Please enter a valid number of players between 2 and 6.")
    
# Asks the user how many players there will be
# We added these lines after we presented after feedback was given. 
 

# Generate Deck - Shuffle Deck is soley from Mr. Pro Coder (Seperate Cards / Generates) 

 

def generate_deck(): 

    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades'] 

    values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'] 

    deck = [(i, values[i % 13], suits[i // 13]) for i in range(52)] 

    return deck 

 

def get_card_name(card): 

    _, value, suit = card 

    return f"{value} of {suit}" 

 

def shuffle_deck(deck): 

    random.shuffle(deck) 

 

    return deck 

 

 

# Give EA player 3 cards EA  

 

def deal_cards(deck, num_players, cards_per_player=3): 

    players = {f'Player {i + 1}': [] for i in range(num_players)} 

    for _ in range(cards_per_player): 

        for player in players: 

            players[player].append(deck.pop()) 

    return players 

 

 

# Asking EA player if they want to play or fold  

 

def choice(players_hands): 

    player_decision = {} 

    for player in players_hands.keys(): 

        decision = input(f"{player}, would you like to play or fold? ").lower() 

        if decision == 'play': 

            print(f"{player} is in the game") 

            player_decision[player] = 'play' 

        else: 

            print(f"{player} has folded.") 

            player_decision[player] = 'fold' 

    return player_decision 

 

 

 

# Give dealer 3 cards from the deck  

 

def deal_dealer_hand(deck, num_cards=3): 

    dealer_hand = [] 

    for _ in range(num_cards): 

        dealer_hand.append(deck.pop()) 

    return dealer_hand 

 

 

# Making sure dealer can player (have check for automatic) 

 

def dealer_qualifies(dealer_hand): 

    return any(card[1] in ['Q', 'K', 'A'] for card in dealer_hand) 

 

 

# Finding highest cards from EA players 

 

def get_hand_value(hand): 

    return max(card[1] for card in hand) 

 

#  

 

def evaluate_hand(hand): 

    values = sorted(card[1] for card in hand) 

    suits = [card[2] for card in hand] 

 

    is_flush = len(set(suits)) == 1 

    is_straight = values == ['10', 'J', 'Q'] or values == ['J', 'Q', 'K'] or values == ['Q', 'K', 'A'] or \
                  (values[0] == '2' and values[1] == '3' and values[2] == '4')  # Example for low straight 

                   

    counts = {value: values.count(value) for value in set(values)} 

    if 3 in counts.values(): 

        return "Three of a Kind" 

    elif is_straight and is_flush: 

        return "Straight Flush" 

    elif is_flush: 

        return "Flush" 

    elif is_straight: 

        return "Straight" 

    elif 2 in counts.values(): 

        return "Pair" 

    else: 

        return "High Card" 

 

def evaluate_pair_plus(players_hands, pair_plus_bets): 

    payouts = { 

        "Pair": 1, 

        "Flush": 4, 

        "Straight": 6, 

        "Three of a Kind": 30, 

        "Straight Flush": 40 

    } 

    results = {} 

     

    for player, hand in players_hands.items(): 

        hand_type = evaluate_hand(hand) 

        payout_multiplier = payouts.get(hand_type, 0) 

        payout = pair_plus_bets[int(player.split()[1]) - 1] * payout_multiplier 

        results[player] = payout 

     

    return results 

 

def compare_hands(players_hands, dealer_hand, ante_bets): 

    dealer_value = get_hand_value(dealer_hand) 

    results = {} 

     

    for player, hand in players_hands.items(): 

        player_value = get_hand_value(hand) 

        player_index = int(player.split()[1]) - 1  # Get player index from player name 

         

        if dealer_value < player_value: 

            results[player] = ante_bets[player_index] * 2 + ante_bets[player_index]
            # Win both ante and play bets
            print("player wins the game")

        else: 

            results[player] = -(ante_bets[player_index] * 2)  # Lose both bets 

            print(f"{player}, your total would be: ${-(ante_bets[player_index] * 2)} due to dealer's win.") 

 

    return results 

 

 

def main(): 
    num_players = set_number_of_players()
    ante_bets, pair_plus_bets = askbet(num_players) 

    

    deck = generate_deck() 

    shuffled_deck = shuffle_deck(deck) 

    players_hands = deal_cards(shuffled_deck, num_players, cards_per_player=3) 

 

    player_totals = {f'Player {i + 1}': ante_bets[i] + pair_plus_bets[i] for i in range(num_players)}  # Total money for each player 

 

    for player, hand in players_hands.items(): 

        hand_type = evaluate_hand(hand) 

        print(f"{player}'s hand: {[get_card_name(card) for card in hand]} - {hand_type}") 

 

    player_decisions = choice(players_hands) 

     

    dealer_hand = deal_dealer_hand(shuffled_deck) 

    dealer_hand_type = evaluate_hand(dealer_hand)  # Evaluate the dealer's hand type 

    print(f"Dealer's hand: {[get_card_name(card) for card in dealer_hand]} - {dealer_hand_type}")  # Output the dealer's hand type 

 

    results = {} 

     

    for player, decision in player_decisions.items(): 

        player_index = int(player.split()[1]) - 1  # Get player index from player name 

        if decision == 'fold': 

            results[player] = -(ante_bets[player_index] + pair_plus_bets[player_index])  # Reflect loss of ante and Pair Plus 

            print(f"{player} folds and loses ${ante_bets[player_index] + pair_plus_bets[player_index]}.") 

 

    if dealer_qualifies(dealer_hand): 

        print("Dealer qualifies.") 

        results.update(compare_hands(players_hands, dealer_hand, ante_bets)) 

    else: 

        print("Dealer does not qualify.") 

        for player in players_hands.keys(): 

            if player_decisions[player] == 'play': 

                player_index = int(player.split()[1]) - 1  # Get player index from player name 

                results[player] = ante_bets[player_index]  # Player wins even money on the ante bet 

                print(f"{player} wins even money on the ante: ${ante_bets[player_index]} back.") 

     

    # Update player totals based on results 

    for player, result in results.items(): 

        player_totals[player] += result 

 

    # Evaluate Pair Plus wins 

    pair_plus_results = evaluate_pair_plus(players_hands, pair_plus_bets) 

    for player, payout in pair_plus_results.items(): 

        if payout > 0: 

            print(f"{player} wins ${payout} from Pair Plus.") 

        else: 

            print(f"{player} loses ${pair_plus_bets[int(player.split()[1]) - 1]} on Pair Plus.") 

 

    # Add Pair Plus winnings to player totals 

    for player in player_totals.keys(): 

        player_totals[player] += pair_plus_results[player] 

 

    #for player, total in player_totals.items(): 

        #print(f"{player}: ${total}") 

 

if __name__ == "__main__": 

    main() 
