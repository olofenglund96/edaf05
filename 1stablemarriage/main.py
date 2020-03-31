import sys

def parse_input():
  """
  Parse input and create dicts of men and women
  """
  lines = [ l.strip() for l in sys.stdin ]

  n = int(lines[0])
  del lines[0]

  nums = []
  for line in lines:
    nums += [int(l)-1 for l in line.split(' ')]

  women = {}
  men = {}

  used_nums = []
  for i in range(0, 2*n*(n+1), n+1): # loop over data in chunks as per input specification
    cnums = nums[i:i+n+1]
    idx = cnums[0]
    pref = cnums[1:]

    if idx not in used_nums:
      inv_pref = [0]*len(pref)
      for j, p in enumerate(pref): # invert preference lists to ensure performance later
        inv_pref[p] = j

      women[idx] = [-1, inv_pref]
      used_nums.append(idx)
    else:
      men[idx] = [0, pref]

  return men, women


if __name__ == '__main__':
  men, women = parse_input()

  # add all men as a tuple (index, propose_index, preference_list)
  free_men = [(key, *value) for key, value in men.items()]

  while len(free_men) > 0:
    mi, wi, pref = free_men.pop(0)
    preferred_woman = women[pref[wi]] # propose

    if preferred_woman[0] == -1:
      # woman has no man, successful propsal
      preferred_woman[0] = mi
    elif preferred_woman[1][preferred_woman[0]] > preferred_woman[1][mi]:
      # woman has a man but prefers this man
      old_man_index = preferred_woman[0]
      old_man = men[old_man_index]
      old_man[0] += 1
      free_men.append((old_man_index, *old_man))
      preferred_woman[0] = mi
    else:
      # proposal not successfull
      free_men.append((mi, wi+1, pref))

  # sort women to follow output specification
  women = {key:women[key] for key in sorted(women.keys())}

  for v in women.values():
    print(1 + v[0])
