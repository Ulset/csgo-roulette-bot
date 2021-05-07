from RouletteWrapper import RouletteWrapper

rw = RouletteWrapper(log_in=False)

# Fake money to start with
start_money = 1000
MAX_LOSS_IN_ROW = 5


def calculate_bet(total_money, max_loss):
    return round((total_money / (2 ** max_loss)) / 2, 2)


money = start_money
bet = calculate_bet(money, MAX_LOSS_IN_ROW)
chance_of_failure = 0.5 ** MAX_LOSS_IN_ROW
print(f"Startet med {money} i kapital. Max antall tap før konkurs: {MAX_LOSS_IN_ROW}({chance_of_failure}% sjanse)")
while True:
    if money < 0:
        raise ValueError("Alle pengene tapt")

    while float(rw.get_timer()) > 1.5:
        pass

    # Returns left of right based on what is least betted on
    choosed_side = rw.get_least_betted_side()
    print(f"Satser {bet} på {choosed_side}")
    winner = rw.get_winner()

    if choosed_side == winner:
        print("Vant")
        money += bet
        bet = calculate_bet(money, MAX_LOSS_IN_ROW)
    else:
        print("Tapte")
        money -= bet
        bet = bet * 2
    print(f"Penger nå: {money}\n")
