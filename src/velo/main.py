import argparse

from velo.commandes.init import init
from velo.commandes.refresh import refresh


def main():
    parser = argparse.ArgumentParser()
    sous_commandes = parser.add_subparsers(dest="commande")

    sous_commandes.add_parser("init")
    sous_commandes.add_parser("refresh")

    args = parser.parse_args()

    if args.commande == "init":
        init()
    elif args.commande == "refresh":
        refresh()


if __name__ == "__main__":
    main()