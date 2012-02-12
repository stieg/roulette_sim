import random
import math
from optparse import OptionParser

class PAndTExp():
    def __init__(self, base = 10, max_depth = 7, max_wins = 10000000):
	self.base = base
	self.depth = 0
	self.max_depth = max_depth
	self.max_wins = max_wins
	self.spins = 0
	self.wins = 0

    def pitch_and_toss(self):
	"""
	Returns a number on the Roulette wheel.  Note 0 can be either 0 or 00.
	"""
	self.spins += 1

	num = random.randint(-1, 36)
	if num < 0:
	    num = 0

	if num > 0 and num % 2 == 0:
	    self.wins += 1
	    self.depth = 0
	else:
	    self.depth += 1

    def still_playing(self):
	return self.depth < self.max_depth and self.wins < self.max_wins

    def get_winnings(self):
	winnings = self.base * self.wins
	if self.max_wins != self.wins:
	    winnings -= (math.ldexp(self.base, self.max_depth) - self.base)

	return winnings

    def __str__(self):
	winnings = self.get_winnings()
	return '''
Final Stats:
   Wins:     %d
   Spins:    %d
   Winnings: %d
'''  % (self.wins, self.spins, winnings)

def main():
    """
    Play the strategy.  Simulate how many wins happen before you loose it all.
    """
    runs = 1000
    avg_winnings = 0
    tot_spins = 0

    parser = OptionParser()
    parser.add_option("-b", "--basebet", dest="basebet",
		      help="Initial betting level", default="10")
    parser.add_option("-l", "--maxlosses", dest="maxlosses",
		      help="Maximum number of consecutive losses", default="6")
    parser.add_option("-w", "--winstop", dest="winstop",
		      help="Stop after this many wins", default="10000000")
    parser.add_option("-s", "--simulations", dest="simulations",
		      help="Number of simulations to run", default="10")
    parser.add_option("-v", "--verbose", dest="verbose",
		      help="Print results of each simulation", default=False)

    (options, args) = parser.parse_args()

    runs = int(options.simulations)
    base = int(options.basebet)
    max_depth = int(options.maxlosses)
    max_wins = int(options.winstop)

    for i in range(0, runs):
	exp = PAndTExp(base = base, max_depth = max_depth,
		       max_wins = max_wins)

	while (exp.still_playing()):
	    exp.pitch_and_toss()

	if options.verbose:
	    print exp
	avg_winnings += exp.get_winnings()/runs
	tot_spins += exp.spins

    max_loss_poss = math.ldexp(base, max_depth) - base
    avg_spins = tot_spins/runs
    print """
Summary:
   Simulations:             %d
   Base bet:                $%d
   Average spins:           %d
   Max consecutive losses   %d
   Max possible loss        $%d
   Average total winnings:  $%d

""" % (runs, base, avg_spins, max_depth, max_loss_poss, avg_winnings)

random.seed()
main()
