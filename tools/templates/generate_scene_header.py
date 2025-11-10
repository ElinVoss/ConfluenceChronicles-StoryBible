#!/usr/bin/env python3
import sys, argparse

TEMPLATE = "Striketide • Ember Anneal • Final Temper • Casting {casting} — {location}\n{d}/{a}/{c}/{casting} — {location}\n"

def main():
  ap = argparse.ArgumentParser(description="Generate Te’Oga scene headers")
  ap.add_argument("--casting", required=True, help="Casting year")
  ap.add_argument("--d", required=True, help="Tide number")
  ap.add_argument("--a", required=True, help="Anneal number")
  ap.add_argument("--c", required=True, help="Crucible number")
  ap.add_argument("--location", required=True, help="Location string")
  args = ap.parse_args()
  print(TEMPLATE.format(casting=args.casting, d=args.d, a=args.a, c=args.c, location=args.location))

if __name__ == "__main__":
  main()
