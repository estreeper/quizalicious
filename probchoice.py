import random

class ProbabalisticChoice(random.Random):

    def probabalisticchoice(self, probs, choices):
        cumul_probs = []
        total = 0
        rand_val = self.uniform(0, 1)
        #print rand_val
        item_num = 0

        for i in range(len(probs)):
            total += probs[i]
            cumul_probs.append(total)

        for prob in cumul_probs:
            if rand_val < prob:
                #print prob
                #print choices[item_num]
                return choices[item_num]
            item_num += 1
