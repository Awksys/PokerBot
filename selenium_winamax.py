import selenium.webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, ElementNotInteractableException

import time

import undetected_chromedriver as uc
import chromedriver_autoinstaller

from selenium.webdriver import ActionChains

import random
import re

import simulator3

from math import sqrt

import json


strong_hands = [
    ['As', 'Ah'], ['Ah', 'As'], ['As', 'Ad'], ['Ad', 'As'], ['As', 'Ac'], ['Ac', 'As'], 
    ['Ah', 'Ad'], ['Ad', 'Ah'], ['Ah', 'Ac'], ['Ac', 'Ah'], ['Ad', 'Ac'], ['Ac', 'Ad'], 
    ['Ks', 'Kh'], ['Kh', 'Ks'], ['Ks', 'Kd'], ['Kd', 'Ks'], ['Ks', 'Kc'], ['Kc', 'Ks'], 
    ['Kh', 'Kd'], ['Kd', 'Kh'], ['Kh', 'Kc'], ['Kc', 'Kh'], ['Kd', 'Kc'], ['Kc', 'Kd'], 
    ['Qs', 'Qh'], ['Qh', 'Qs'], ['Qs', 'Qd'], ['Qd', 'Qs'], ['Qs', 'Qc'], ['Qc', 'Qs'], 
    ['Qh', 'Qd'], ['Qd', 'Qh'], ['Qh', 'Qc'], ['Qc', 'Qh'], ['Qd', 'Qc'], ['Qc', 'Qd'], 
    ['As', 'Ks'], ['Ks', 'As'], ['Ah', 'Kh'], ['Kh', 'Ah'], ['Ad', 'Kd'], ['Kd', 'Ad'], 
    ['Ac', 'Kc'], ['Kc', 'Ac']
]

strong_hands_plus = [
    ['As', 'Ah'], ['Ah', 'As'], ['As', 'Ad'], ['Ad', 'As'], ['As', 'Ac'], ['Ac', 'As'], 
    ['Ah', 'Ad'], ['Ad', 'Ah'], ['Ah', 'Ac'], ['Ac', 'Ah'], ['Ad', 'Ac'], ['Ac', 'Ad'], 
    ['Ks', 'Kh'], ['Kh', 'Ks'], ['Ks', 'Kd'], ['Kd', 'Ks'], ['Ks', 'Kc'], ['Kc', 'Ks'], 
    ['Kh', 'Kd'], ['Kd', 'Kh'], ['Kh', 'Kc'], ['Kc', 'Kh'], ['Kd', 'Kc'], ['Kc', 'Kd'],
]


card_positions = {
    "Ts": (7.69, 66.67), "9s": (15.38, 66.67), "8s": (23.08, 66.67), "7s": (30.77, 66.67), "6s": (38.46, 66.67),
    "5s": (46.15, 66.67), "4s": (53.85, 66.67), "3s": (61.54, 66.67), "2s": (69.23, 66.67), "As": (76.92, 66.67),
    "Ks": (84.62, 66.67), "Qs": (92.31, 66.67), "Js": (100, 66.67),
    
    "Th": (7.69, 33.33), "9h": (15.38, 33.33), "8h": (23.08, 33.33), "7h": (30.77, 33.33), "6h": (38.46, 33.33),
    "5h": (46.15, 33.33), "4h": (53.85, 33.33), "3h": (61.54, 33.33), "2h": (69.23, 33.33), "Ah": (76.92, 33.33),
    "Kh": (84.62, 33.33), "Qh": (92.31, 33.33), "Jh": (100, 33.33),
    
    "Tc": (7.69, 0), "9c": (15.38, 0), "8c": (23.08, 0), "7c": (30.77, 0), "6c": (38.46, 0),
    "5c": (46.15, 0), "4c": (53.85, 0), "3c": (61.54, 0), "2c": (69.23, 0), "Ac": (76.92, 0),
    "Kc": (84.62, 0), "Qc": (92.31, 0), "Jc": (100, 0),
    
    "Td": (7.69, 100), "9d": (15.38, 100), "8d": (23.08, 100), "7d": (30.77, 100), "6d": (38.46, 100),
    "5d": (46.15, 100), "4d": (53.85, 100), "3d": (61.54, 100), "2d": (69.23, 100), "Ad": (76.92, 100),
    "Kd": (84.62, 100), "Qd": (92.31, 100), "Jd": (100, 100),
}

def card_from_pos(x, y):
    for card, (cx, cy) in card_positions.items():
        if x == cx and y == cy:  
            return card
    return "Card not found"

def get_cards(parent_element):
    child_elements = parent_element.find_elements(By.XPATH, ".//div[contains(@style, 'background-position')]")
    background_positions = []
    for child in child_elements:
        style = child.get_attribute('style')
        if 'background-position' in style:
            start_index = style.find('background-position:') + len('background-position:')
            end_index = style.find(';', start_index)
            background_position = style[start_index:end_index].strip()
            background_positions.append(background_position)

    results_cards = []
    for position in background_positions:
        x_percent, y_percent = [float(value.replace('%', '')) for value in position.split(' ')]
        card = card_from_pos(x_percent, y_percent)
        results_cards.append(card)
    
    return results_cards

def set_iframe():
    try:
        iframes = driver.find_elements(By.TAG_NAME, 'iframe')        
        
        if iframes:
            driver.switch_to.frame(iframes[0])
        
        return len(iframes)
    except:
        return 0

def enter_game(rooms, min_players, max_players):
    global small_blind_value, big_blind_value

    for room in rooms:
        nb_p = room.find_element(By.CSS_SELECTOR, "div.gpmeRd")
        blinds = room.find_element(By.CSS_SELECTOR, "div.jKnBmp")

        try:
            small_blind = blinds.text.split('-')[0]  
            small_blind = small_blind.replace(',', '.')  
            small_blind_value = float(small_blind)
        except:
            continue
            
        try:
            big_blind = blinds.text.split('-')[1]  
            big_blind = big_blind.replace(',', '.')  
            big_blind_value = float(big_blind)
        except:
            continue
        
        text = nb_p.text
        print(text, big_blind_value)
        if '/' in text and min_BB <= big_blind_value <= max_BB:
            left_value, right_value = text.split('/')
            left_value = int(left_value.strip())
            right_value = int(right_value.strip())
            if left_value <= max_players and left_value >= min_players:
                action = ActionChains(driver)
                action.double_click(room).perform()
                return True

def setup_board(board):
    flop, turn, river = [], [], []
    
    if len(board) >= 3:
        flop = board[:3]
    if len(board) >= 4:
        turn = board[3:4]
    if len(board) == 5:
        river = board[4:5]
        
    return flop, turn, river

def random_sleep(a, b):
    time.sleep(round(random.uniform(a, b), 1))


def detect_same_player(player1, player2):
    def is_float(string):
        try:
            float(string)
            return True
        except ValueError:
            return False

    for word in player1.split():
        if word in player2 and not is_float(word):
            return True

def get_players(wait_time, detect_same_room):
    global player_stack, players

    try:       
        player_elements = WebDriverWait(driver, wait_time).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.pkr__c5rwez-5")))

        for player_element in player_elements:

            if len(players) < 5:
                players.append(player_element.text)

            if detect_same_room:
                count=0
                for player in players:
                    if detect_same_player(player, player_element.text):
                        count+=1
                    
                    if count == 2 or "Awksys" in player_element.text:
                        return True
                    
                return False

            if "Anondor" in player_element.text:
                score_element = WebDriverWait(player_element, wait_time).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.ersNmu")))
                player_stack = float(score_element.text.replace(',', '.'))

    except:
        player_stack = 0


def set_values(wait_time):
    global pot_value, nb_players, board, player_hand, costs, start_nb_players, player_stack, new_hand, players, can_quit

    try:
        pot_element = WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Pot total')]"))) 
        pot_value = float(pot_element.text.split(": ")[1].replace(',', '.'))
    except:
        pass

    try:
        board_element = WebDriverWait(driver, wait_time).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.pkr__wnbd9b-0")))
        board = get_cards(board_element)
    except:
        board=[]

    try:
        hand_elements = driver.find_elements(By.CSS_SELECTOR, "div.pkr__sc-1iojzon-2")

        if hand_elements == []:
            player_hand=[]
        
        nb_players = len(hand_elements)

        visible_hands=[]

        for hand_el in hand_elements:
            this_player_hand = get_cards(hand_el)
            if not 'Card not found' in this_player_hand:
                visible_hands.append(this_player_hand)

        
        if len(board) == 0 and nb_players > 1: 
            if not new_hand:
                new_hand=True
                can_quit = False
                
                player_hand=visible_hands[0]

                pot_value=round(small_blind_value+big_blind_value, 2)
                costs=0
                start_nb_players=nb_players

                print("new hand !")
                random_sleep(0.5,0.75)

        elif new_hand:
            new_hand = False
            
    except:

        new_hand = False
        can_quit = True
        player_hand = []

    get_players(wait_time, False)


def define_proba():
    global gain_prob, loss_prob, pot_odds, pot_value, player_stack, nb_players, player_hand, call_value, board, time_f, big_blind_value

    if len(board) > 0:
        flop, turn, river = setup_board(board)

        print(flop, turn, river)

        results = simulator3.simulate_poker(player_hand, nb_players-1, flop, turn, river, time_f=time_f)
    
    else:
        with open('new_results_simulation.json', 'r') as file:
            all_results = json.load(file)

        hand_key = f"{player_hand[0]}-{player_hand[1]}"
        reversed_hand_key = f"{player_hand[1]}-{player_hand[0]}"

        try:
            results = all_results[str(nb_players-1)][hand_key]
        except:
            results = all_results[str(nb_players-1)][reversed_hand_key]
        
        random_sleep(0.5,1)
            
    print(results)
    pot_max = player_stack * nb_players * 0.8

    if pot_value > pot_max:
        pot_value = pot_max

    max_pot_odds = [0.75, 0.55, 0.45, 0.35]

    factor_wins = risk_value-(len(board)/5)*0.15
    factor_ties = 0.1 * (start_nb_players/nb_players)

    loss_prob = results["loses"]

    gain_prob = results["wins"] * factor_wins + results["ties"] * factor_ties

    if len(board) == 0:
        gain_prob = gain_prob * 0.95

    #pot_odds = round(call_value/(pot_value+call_value),2)

    value = sqrt(10000*call_value/big_blind_value)/(65*pow(nb_players-1, 2))

    pot_odds = min(max_pot_odds[nb_players-2], max(0.12, round(call_value/(pot_value+call_value/max(0.25,value)),2)))
    

    print("Gain Prob:", gain_prob, factor_wins, factor_ties, "Pot odds:", pot_odds, "Call value:", call_value, "Nb joueurs:", nb_players, "Pot value:", pot_value)


def raise_pot(action_buttons, index):
    try:
        try:
            raise_parent = WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.iIfKWg")))
            raise_buttons = raise_parent.find_elements(By.XPATH, "./*")
            
            raise_buttons[index].click()  
        except:
            print("can't find raise")
        
        random_sleep(1,2)

        action_buttons[2].click()                 
    except:
        pass
     
def confirm_fold():
    try:
        confirm_parent = WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.kJHFSa")))
        confirm_buttons = confirm_parent.find_elements(By.XPATH, "./*")
        confirm_buttons[0].click()  
    except:
        print("no confirm fold")


def leave_room():
    try:
        random_sleep(1,2)
        leave_button = WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.jmPOpk")))
        leave_button.click()  

        random_sleep(0.5,1)

        try:
            quit_button = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, "//button[text()='Quitter']")))
            quit_button.click()
        except:
            print("no confirm")
            

    except:
        print("error leaving")

def login():
    global password, count_disconnect

    random_sleep(1,2)

    try:
        input_elements = driver.find_elements(By.CSS_SELECTOR, "input.sc-oeqTF")
        input_elements[1].click()
        random_sleep(0.5,1)
        input_elements[1].send_keys(password)

        login_button = driver.find_element(By.XPATH, "//button[contains(., 'Se connecter')]")
        random_sleep(0.5,1)
        login_button.click()

        count_disconnect += 1

        return True
    except:
        print("still connected")
        return False


def popup(restart):

    if restart:
        random_sleep(5,6)
        
        iframe = driver.execute_script("return document.getElementById('pokWEB');")
        if iframe:
            driver.switch_to.frame(iframe)
        else:
            print("no found iframe with JS")

    try:
        back_buttons = driver.find_elements(By.XPATH, "//span[contains(., 'Plus tard')]")
        random_sleep(0.25,0.5)
        back_buttons[0].click()

    except Exception as e:
        if restart:
            print(f"Error: {e}")

def cash_game():
    try:
        cash_game = WebDriverWait(driver, 0.5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.hAnPuV")))
        random_sleep(0.25,0.5)
        cash_game.click()
    except Exception as e:
        print(e)

def switch_no_money():
    try:
        switch = WebDriverWait(driver, 0.5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.pkr__sc-18qhqjl-7")))
        random_sleep(0.25,0.5)
        switch.click()
        random_sleep(0.25,0.5)
        no_money = driver.find_elements(By.XPATH, "//div[contains(., 'Play')]")[-1]
        random_sleep(0.25,0.5)
        no_money.click()
        random_sleep(0.25,0.5)
        switch.click()
    except Exception as e:
        print(e)
        

players=[]
min_BB = 0.5
max_BB = 0.5
count_comeback = 0
count_disconnect = 0

password = "aM120605*"

chromedriver_path = chromedriver_autoinstaller.install()

options = selenium.webdriver.ChromeOptions()
options.add_argument("--disable-search-engine-choice-screen")

driver = uc.Chrome(options, driver_executable_path=chromedriver_path, headless=False)
driver.set_page_load_timeout(300)
driver.maximize_window()


action = ActionChains(driver)

driver.get("https://www.winamax.fr/poker/launch_poker.php")

print("Waiting...")

try:
    risk_value = float(input("Give sensibility value (>1 more risks, default value=0.94): "))
except:
    risk_value = 0.88


while True:

    random_sleep(2,5)

    set_iframe()

    try:
        rooms = WebDriverWait(driver, 5.0).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.pkr__sc-3m2vag-0")))
        random.shuffle(rooms)

        print("trying to enter a room...")

        tries=0
        while tries < 10:
            if enter_game(rooms, 3, 4):
                break
            time.sleep(random.randint(1,2))
            tries+=1
        
        while tries < 20 and tries >= 10:
            if enter_game(rooms, 2, 4):
                break
            time.sleep(random.randint(1,2))
            tries+=1
        
        while tries == 20:
            if enter_game(rooms, 2, 5):
                break
            time.sleep(random.randint(1,2))
            
    except:
        print("you're probably not in the lobby")

    random_sleep(1,2)
    set_iframe()

    if get_players(2, True):
        print(players)
        continue
    else:
        players=[]

    try:
        free_spot = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.pkr__c5rwez-3")))
        free_spot.click()
            
    except:
        print("can't take a sit")

        random_sleep(1,2)

        try:
            wl_button = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button.fGTcQL")))
            random_sleep(0.5,1)
            wl_button.click()

            print("on waiting list...")
                
        except:
            print("can't enter waiting list")
        
        try:
            free_spot = WebDriverWait(driver, 5.0).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.pkr__c5rwez-3")))
            free_spot.click()
                
        except:
            print("can't take a sit")

    try:
        input_element = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input.pkr__sc-1efnult-1")))

        min_value = float(input_element.get_attribute("min"))
        max_value = float(input_element.get_attribute("max"))

        #final_value = round((float(min_value)+float(max_value))/2, 2)

        random_sleep(0,0.5)

        input_element.send_keys(str(max_value))

        print(min_value, max_value)

        random_sleep(0,0.5)

        quit_button = driver.find_element(By.XPATH, "//button[text()='Confirmer']")
        quit_button.click()

    except:
        try:
            wl_button = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button.eEWynQ")))
            random_sleep(0.5,1)
            wl_button.click()
                
        except:
            print("can't leave waiting list")

        print("can't confirm value to table")
        leave_room()

        if login():
            popup(True)
            cash_game()
            switch_no_money()
            random_sleep(1200,1800)

        continue


    board=[]
    player_hand=[]

    pot_value=0

    costs = 0
    player_stack=max_value

    nb_players=1
    start_nb_players=5

    time_f = 0.35

    new_hand = False

    time_in_room = 0  
    time_limit = 45 * 60
    start_time = time.time()

    count_no_stack = 0
    count_no_signal = 0
    count_no_players = 0
    
    response_time = 0.25
    action_bool = False
    can_quit = False

    print(set_iframe())

    while (time_in_room < time_limit and player_stack < max_value*2.5 and time_f > 0.3 and count_no_stack < 5 and count_no_players < 20) or not can_quit or player_hand in strong_hands_plus:
        time_in_room = time.time() - start_time

        set_values(response_time)

        if nb_players <= 1 and len(board) == 0:
            new_hand = False
        
        try:
            action_parent = WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.pkr__pbahk6-5")))
            action_buttons = action_parent.find_elements(By.XPATH, "./*")

            action_bool = True

            set_values(response_time*2)

            button_text = action_buttons[1].text

            button_text_filtered = re.sub(r'F\d+', '', button_text).strip()
            match = re.search(r'\d+,\d+|\d+', button_text_filtered)

            if match:
                value = match.group().replace(',', '.')
                call_value = float(value)
            else:
                call_value=0

            if player_hand in strong_hands and len(board) == 0 and call_value < 2.5*big_blind_value and random.randint(1,100) > 20:
                print("Strong hands")
                raise_pot(action_buttons, 6)
                continue
            
            if player_hand in strong_hands_plus and len(board) == 0 and random.randint(1,100) > 5 and call_value > 5*big_blind_value:
                print("Strong hands plus")
                try:
                    action_buttons[1].click()  
                except:
                    driver.execute_script("arguments[0].click();", action_buttons[1])
                continue
            
            else:
                if len(board) < 4 and call_value == 0:
                    try:
                        WebDriverWait(driver, 0.25).until(EC.element_to_be_clickable(action_buttons[1]))
                        random_sleep(0.25,0.5)
                        action_buttons[1].click() 
                        continue
                    except:
                        pass 

                print(player_hand, nb_players, pot_value, costs, call_value) 
                define_proba()   


                if len(board) == 4 and pot_value < 18*big_blind_value and gain_prob > 0.65 - ((nb_players-2)/10) and random.randint(1,100) > 10:
                    raise_pot(action_buttons, 2)
                    continue

                if loss_prob == 0:
                    print("0 chance to lose: All in")
                    raise_pot(action_buttons, 6)  
                    continue

                if len(board) == 5 and loss_prob < 0.01:
                    print("All in river")
                    raise_pot(action_buttons, 6)  
                    continue

            if gain_prob > pot_odds or call_value == 0:
                costs += call_value
                try:
                    action_buttons[1].click()  
                except:
                    driver.execute_script("arguments[0].click();", action_buttons[1])
            else:
                try:
                    action_buttons[0].click()
                except:
                    driver.execute_script("arguments[0].click();", action_buttons[0])
                
                new_hand = False
                can_quit = True
                player_hand = []
                confirm_fold()                

        except:
            action_bool = False
        
        print(player_hand, board)
        print("Total Pot:", pot_value, "Active Players:", nb_players, "Stack:", player_stack, "Time in room:", time_in_room/60, count_comeback, new_hand, can_quit)

        
        if player_hand == [] and board == [] and player_stack == 0:
            count_no_signal += 1

            if count_no_signal > 5:
                break             
                
        else:
            count_no_signal = 0

        try:
            back_button = WebDriverWait(driver, 0.25).until(EC.presence_of_element_located((By.XPATH, "//button[text()='Revenir']")))
            random_sleep(1,2)
            back_button.click()

            time_f-=0.02
            new_hand = False

            count_comeback += 1
        except:
            pass

        if player_stack < small_blind_value:
            count_no_stack += 1
        else:
            count_no_stack = 0

        if start_nb_players <= 3:
            print("start players: ", start_nb_players)
            count_no_players += 3
        elif start_nb_players <= 2:
            count_no_players += 4
        else :
            count_no_players = 0

        popup(False)
            

    print(count_no_stack, count_no_signal, player_stack, time_in_room/60)
    leave_room()
    random_sleep(60,120)