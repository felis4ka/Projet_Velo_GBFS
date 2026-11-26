import argparse

from velo.commandes.init import init


def main():
    parser = argparse.ArgumentParser()

    sous_commandes = parser.add_subparsers(dest="commande")

    sous_commandes.add_parser("init")

    args = parser.parse_args()

    if args.commande == "init":
        init()


if __name__ == "__main__":
    main()