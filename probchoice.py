import random

class ProbabalisticChoice(random.Random):

    def probabalisticchoice(self, pairs):
        """Takes a list of pairs and returns a chosen one of the elements from a pair.
        The pairs should be in the form (choice, probability)"""
        cumul_probs = []
        total = 0
        rand_val = self.uniform(0, 1)
        item_num = 0

        for i in range(len(pairs)):
            total += pairs[i][1]
            cumul_probs.append(total)

        for prob in cumul_probs:
            if rand_val < prob:
                return pairs[item_num][0]
            item_num += 1
