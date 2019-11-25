import main_Standard
import main_Extra
import matplotlib.pyplot as plt



def main():
    _, max_values_standard, max_mass_standard = main_Standard.realize_algorithm()
    _, max_values_Extra, max_mass_Extra = main_Extra.realize_algorithm()
    show_results(max_values_standard,max_values_Extra,max_mass_standard,max_mass_Extra)

def show_results(max_values_standard,max_values_Extra,max_mass_standard,max_mass_Extra):
    plt.subplot(2, 2, 1)
    plt.title("Strategia ewolucyjna")
    plt.plot([step for step in range(len(max_values_standard))], [value for value in max_values_standard])
    plt.ylabel("Values")
    plt.xlabel("Epoch")

    plt.subplot(2, 2, 3)
    plt.plot([step for step in range(len(max_mass_standard))], [mass for mass in max_mass_standard])
    plt.ylabel("Mass")
    plt.xlabel("Epoch")

    plt.subplot(2, 2, 2)
    plt.title("Strategia ewolucyjna z rodzicami")
    plt.plot([step for step in range(len(max_values_Extra))], [value for value in max_values_Extra])
    plt.ylabel("Values")
    plt.xlabel("Epoch")

    plt.subplot(2, 2, 4)
    plt.plot([step for step in range(len(max_mass_Extra))], [mass for mass in max_mass_Extra])
    plt.ylabel("Mass")
    plt.xlabel("Epoch")

    plt.show()

if __name__ == "__main__":
    main()