from accountpool.scheduler import Scheduler
import argparse

parser = argparse.ArgumentParser(description='AccountPool')
parser.add_argument('website', type=str, help='website')
parser.add_argument('--processor', type=str, help='processor to run')
args = parser.parse_args()
website = args.website

if __name__ == '__main__':
    # if processor set, just run it
    if args.processor:
        getattr(Scheduler(), f'run_{args.processor}')(website)
    else:
        Scheduler().run(website)
