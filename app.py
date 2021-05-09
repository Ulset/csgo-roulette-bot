from RouletteWrapper import RouletteWrapper

rw = RouletteWrapper(log_in=False)

# Fake money to start with
start_money = 1000

money = start_money

games_played = 0
games_won = 0
while True:
    if money < 0:
        raise ValueError("Alle pengene tapt")

    money = round(money, 2)
    bet = round(money * 0.05, 2)
    # Returns left of right based on what is least betted on
    rw.wait_for_timer(1.5)
    chosen_side = rw.get_bet_side()
    if chosen_side:
        games_played += 1
        print(f"Satser {bet} på {chosen_side}")
    else:
        print("Satser ingenting")

    winner = rw.get_winner()

    if chosen_side and chosen_side == winner:
        print("Vant")
        money += bet
        games_won += 1
    elif chosen_side and chosen_side != winner:
        print("Tapte")
        money -= bet
    print(f"Penger nå: {money}")
    if games_played > 0:
        print(f"Vunnet {games_won} av {games_played} ({round((games_won / games_played) * 100, 2)} %)\n")
