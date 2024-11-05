import math
from datetime import datetime

bernoulli_cache = {0: 1}


def bernoulli(n):
    if n in bernoulli_cache:
        return bernoulli_cache[n]
    if n % 2 == 1 and n > 1:
        return 0
    b_n = 0
    for k in range(n):
        b_n -= math.comb(n + 1, k) * bernoulli(k) / (n + 1)
    bernoulli_cache[n] = b_n
    return b_n


def maclaurin_series_ln_sin_x_over_x(x, epsilon):
    f_x = 0
    n = 1
    term = epsilon + 1
    try:
        while abs(term) >= epsilon:
            B_2n = bernoulli(2 * n)
            term = ((-1) ** (n - 1) * (2 ** (2 * n)) * B_2n * (x ** (2 * n))) / (2 * n * math.factorial(2 * n))
            f_x += term
            n += 1
    except OverflowError:
        print("Помилка: обчислення переповнило доступні межі. Можливо, значення x або точність e занадто великі.")
        return None, None

    return f_x, n - 1


def save_results(filename, results):
    try:
        with open(f"{filename}.txt", "a", encoding="utf-8") as file:
            for result in results:
                date_str = result['date']
                x = result['x']
                epsilon = result['epsilon']
                f_x = result['f_x']
                N = result['N']
                file.write(f"{date_str} {x} {epsilon} {f_x:.12f} {N}\n")
    except Exception as e:
        print(f"Помилка запису у файл: {e}")


def main():
    results = []
    while True:
        x_input = input("Задайте аргумент функції (або 'Кінець' для завершення): ")
        if x_input.lower() == "кінець":
            break
        try:
            x = float(x_input)
            epsilon = float(input("Задайте точність обчислення (0 < e < 1): "))

            if not (0 < epsilon < 1):
                print("Помилка: точність повинна бути між 0 та 1.")
                continue

            if abs(x) >= math.pi:
                print(f"Помилка: значення x = {x} виходить за межі області визначення (-π, π).")
                continue

            f_x, N = maclaurin_series_ln_sin_x_over_x(x, epsilon)
            if f_x is None:
                continue

            print(f"f({x}, {epsilon}) = {f_x:.12f}")
            print(f"Кількість членів ряду: {N}")
            results.append({
                "date": datetime.now().strftime("%d.%m.%Y"),
                "x": x,
                "epsilon": epsilon,
                "f_x": f_x,
                "N": N
            })
        except ValueError:
            print("Помилка: введіть числові значення.")
        except NotImplementedError as e:
            print(str(e))

    if results:
        save_choice = input("Записати результати у файл? (Так/Ні): ")
        if save_choice.lower() == "так":
            filename = input("Введіть ім'я файлу (до 5 символів, тільки літери або цифри): ")

            if len(filename) < 1 or len(filename) > 5 or not filename.isalnum():
                print("Помилка: ім'я файлу повинно містити від 1 до 5 символів і містити тільки букви або цифри.")
            else:
                save_results(filename, results)
                print(f"Дані у файл {filename}.txt записано. Поточна кількість записів: {len(results)}")
        else:
            print("Дані у файл не записано.")


if __name__ == "__main__":
    main()
