import random
import matplotlib.pyplot as plt

def play_monty_hall(num_doors, policy, is_banana_peel):
    """Simulates a single game of Monty Hall."""
    car_door = random.randint(0, num_doors - 1)
    player_choice = random.randint(0, num_doors - 1)
    
    # 1. Host opens a door
    if is_banana_peel:
        # Host accidentally opens ANY random door besides the player's
        available_for_host = [d for d in range(num_doors) if d != player_choice]
        host_opened = random.choice(available_for_host)
    else:
        # Standard: Host intentionally opens a GOAT door
        available_for_host = [d for d in range(num_doors) if d != player_choice and d != car_door]
        host_opened = random.choice(available_for_host)
        
    # 2. Check Banana Peel edge case
    # If the host accidentally reveals the car, the game is ruined.
    # The player's original choice is wrong, and they can't switch to the exposed car.
    if is_banana_peel and host_opened == car_door:
        return False 
        
    # 3. Player makes final choice
    if policy == 'stick':
        final_choice = player_choice
    elif policy == 'switch':
        # Player switches to a random closed door
        available_for_switch = [d for d in range(num_doors) if d != player_choice and d != host_opened]
        final_choice = random.choice(available_for_switch)
        
    return final_choice == car_door

def run_simulation(num_doors, policy, is_banana_peel, iterations=10000):
    """Runs the Monte Carlo simulation and tracks win rate over time."""
    wins = 0
    win_rate_history = []
    
    for i in range(1, iterations + 1):
        if play_monty_hall(num_doors, policy, is_banana_peel):
            wins += 1
        # Track win rate to observe how the approximation improves
        win_rate_history.append(wins / i) 
        
    return wins / iterations, win_rate_history

# ==========================================
# Main Execution and Plotting
# ==========================================
if __name__ == "__main__":
    doors_list = [3, 6, 9, 20, 100]
    iterations = 10000
    
    print(f"Running {iterations} iterations per configuration...\n")
    print(f"{'Doors':<6} | {'Policy':<7} | {'Standard Win %':<15} | {'Banana Peel Win %'}")
    print("-" * 55)

    # Setup plots
    fig, axes = plt.subplots(2, 1, figsize=(10, 12))
    
    for doors in doors_list:
        # Standard Game
        stick_win, stick_hist = run_simulation(doors, 'stick', is_banana_peel=False, iterations=iterations)
        switch_win, switch_hist = run_simulation(doors, 'switch', is_banana_peel=False, iterations=iterations)
        
        # Banana Peel Variant
        bp_stick_win, bp_stick_hist = run_simulation(doors, 'stick', is_banana_peel=True, iterations=iterations)
        bp_switch_win, bp_switch_hist = run_simulation(doors, 'switch', is_banana_peel=True, iterations=iterations)
        
        # Print tabular results
        print(f"{doors:<6} | {'Stick':<7} | {stick_win * 100:>13.2f}% | {bp_stick_win * 100:>16.2f}%")
        print(f"{doors:<6} | {'Switch':<7} | {switch_win * 100:>13.2f}% | {bp_switch_win * 100:>16.2f}%")
        print("-" * 55)
        
        # Plotting the approximation improvement (Law of Large Numbers)
        axes[0].plot(switch_hist, label=f'{doors} Doors')
        axes[1].plot(bp_switch_hist, label=f'{doors} Doors')

    # Configure Standard Plot
    axes[0].set_title('Standard Monty Hall: "Switch" Policy Win Rate Convergence')
    axes[0].set_xlabel('Iterations')
    axes[0].set_ylabel('Win Probability')
    axes[0].legend()
    axes[0].grid(True)

    # Configure Banana Peel Plot
    axes[1].set_title('Banana Peel Variant: "Switch" Policy Win Rate Convergence')
    axes[1].set_xlabel('Iterations')
    axes[1].set_ylabel('Win Probability')
    axes[1].legend()
    axes[1].grid(True)

    plt.tight_layout()
    plt.show()