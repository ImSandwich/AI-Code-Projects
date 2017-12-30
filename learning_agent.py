'''A learning program based upon pg. 55 fig 2.15'''

import random 

num_probability = [1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0]
num_modifications = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]

def main():
    '''entry-point'''
    print("Program initialized.")
    while True:
        printTen()
        user_input = input()
        learning_agent(user_input)


def printTen():
    sum_probability = 0
    for i in range(0,10):
        sum_probability += num_probability[i]

    output = ""
    for i in range(0,10):
        pick = random.uniform(0, sum_probability)
        sub_sum = 0
        called = False
        for j in range(0,10):
            sub_sum += num_probability[j]
            if sub_sum >= pick:
                output += str(j) + ' '
                called = True
                break
        if called is False:
            print('pick {} error, largest is {}'.format(pick, sub_sum))
    print(num_probability)
    print(output)

def problem_generator():
    global num_probability
    global num_modifications

    for i in range(0,10):
        num_modifications[i] = random.uniform(float(-num_probability[i]), float(num_probability[i]) + 1.0)
    num_probability = [x+y for x,y in zip(num_probability, num_modifications)]


def learning_agent(user_input):
    global num_probability
    global num_modifications
    
    if user_input is '1':
        problem_generator()
    elif user_input is '0':
        num_probability = [x-y for x,y in zip(num_probability, num_modifications)] 
        problem_generator()

if __name__ == "__main__":
    main()
