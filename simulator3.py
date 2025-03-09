from treys import Card, Evaluator, Deck
from itertools import combinations
import random
from math import sqrt
import os

def print_better_hands(board, hand):
    Card.print_pretty_cards(board)
    Card.print_pretty_cards(hand)
    print("")

def convert_to_card_objects(card_list):
    return [Card.new(card) for card in card_list]

def simulate_poker(player_hand, num_opponent, flop=None, turn=None, river=None, time_f=1):
    evaluator = Evaluator()

    def get_opponent_hands(available_cards, num_opponent, limit):
        combinations = []
        for _ in range(limit):
            selected_cards = random.sample(available_cards, 2 * num_opponent)

            if selected_cards not in combinations:
                combinations.append(selected_cards)

        return combinations

    def compare_scores(board, player_hand, opponent_hands, stage):
        player_wins = 0
        player_ties = 0
        player_loses = 0
        total_hands = 0

        bluff_perc = 10

        player_score = evaluator.evaluate(player_hand, board)

        for opponent_combo in opponent_hands:
            opponents = [opponent_combo[i:i+2] for i in range(0, len(opponent_combo), 2)]  
        
            try:
                opponent_scores = [evaluator.evaluate(hand, board) for hand in opponents]
            except Exception as e:
                continue
            
            if stage == 0:
                th = 7462
            elif stage == 3:
                th = 6500
            elif stage == 4:
                th = 6000
            elif stage == 5: 
                th = 5500

            if random.randint(1,100) > bluff_perc and any(score > th for score in opponent_scores):
                continue
            
            if all(player_score < score for score in opponent_scores):
                player_wins += 1
                
            elif any(player_score == score for score in opponent_scores) and player_score == min(opponent_scores):
                player_ties += 1      
            else:
                player_loses += 1
                #print_better_hands(board, opponents[0])

            total_hands += 1
                
        if total_hands > 0:
            return player_wins / total_hands, player_ties / total_hands, player_loses / total_hands
        else:
            return 0, 0, 0
    
    def simulate_stage(n_simulations, visible_cards):
        global used_cards

        n_simulations = int(n_simulations)

        visible_cards = convert_to_card_objects(visible_cards)

        used_cards += visible_cards

        available_cards = [card for card in deck.cards if card not in used_cards]

        opponent_hands_combos = get_opponent_hands(available_cards, num_opponent, n_simulations)
        
        total_wins = 0
        total_ties = 0
        total_loses = 0

        remaining_deck = [card for card in deck.cards if card not in used_cards]
        possible_comb = list(combinations(remaining_deck, 5-len(visible_cards)))  
        random_comb = random.sample(possible_comb, min(int(n_simulations*0.8), len(possible_comb)))

        for combo in random_comb:
            board = visible_cards + list(combo) 

            wins, ties, loses = compare_scores(board, player_hand, opponent_hands_combos, len(visible_cards))
            total_wins += wins
            total_ties += ties
            total_loses += loses

        results['wins'] = total_wins / len(random_comb)
        results['ties'] = total_ties / len(random_comb)
        results['loses'] = total_loses / len(random_comb)
        
    results = {}


    global used_cards

    player_hand = convert_to_card_objects(player_hand)

    used_cards = player_hand[:] 

    deck = Deck()

    if flop == []:
        simulate_stage(time_f*500, [])
    elif turn == []:
        used_cards += [turn]
        simulate_stage(time_f*500, flop)
    elif river == []:
        used_cards += [flop + turn] 
        simulate_stage(time_f*2000, flop + turn)
    else:
        simulate_stage(time_f*5000, flop + turn + river)
        
    return results


if __name__ == "__main__":
    num_opponent = 2

    os.system('taskkill /F /IM chrome.exe /T')


    player_hand = ['As', 'Td'] 
    flop = ['Th', '6h', 'Ks']
    turn = ['5s']
    river = ['8d']

    results = simulate_poker(player_hand, num_opponent, flop=flop, turn=turn, river=river, time_f=0.5)

    for stage, win_percentage in results.items():
        print(f"Percentage {stage}: {win_percentage*100:.2f}%")
    
