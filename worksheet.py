import modules.bool_circ.bool_circ as bc

# n0 = node(0, 'a', {3:1, 4:1}, {1:1, 2:1})
# n1 = node(1, 'b', {0:1}, {2:2, 5:1})
# n2 = node(2, 'c', {0:1, 1:2}, {6:1})
# i0 = node(3, 'i0', {}, {0:1})
# i1 = node(4, 'i1', {}, {0:1})
# o0 = node(5, 'o0', {1:1}, {})
# o1 = node(6, 'o1', {2:1}, {})
# g0 = open_digraph([3,4], [5,6], [n0,n1,n2,i0,i1,o0,o1])


# print(n0)
# print(o1)

# print(g0)

# print([n0,n1,n2], [g0,g0])

# # depth half_adder
# for n in range(6):
#   print(n, len(bc.bool_circ.half_adder(n).topologic_sort()))

# print()

# # shortest path from input to output
# for n in range(6):
#   a = bc.bool_circ.half_adder(n)
#   m = len(a.topologic_sort()) # le plus grand c'est forcément la profondeur
#   for i in a.inputs_ids:
#     for o in a.outputs_ids:
#       p = a.shortest_path(i, o)[0]
#       if p < m :
#         m = p
#   print(n, m)

# print()

# ##### CLA

# # nombre de portes
# for n in range(4):
#   m = 0
#   cl = bc.bool_circ.carry_lookahead(n)
#   for _ in cl.nodes_not_io_ids: m += 1
#   print(n, m)

# print()

# # depth half_adder
# for n in range(6):
#   print(n, len(bc.bool_circ.carry_lookahead(n).topologic_sort()))

# print()

# # shortest path from input to output
# for n in range(4):
#   a = bc.bool_circ.carry_lookahead(n)
#   m = len(a.topologic_sort()) # le plus grand c'est forcément la profondeur
#   for i in a.inputs_ids:
#     for o in a.outputs_ids:
#       p = a.shortest_path(i, o)[0]
#       if p < m :
#         m = p
#   print(n, m)


# ratio nombre de noeud
import random as rd

n = 0
m = 0
N = 1e3
for i in range(int(N)):
  b = True
  while(b):
    try:
      b = bc.bool_circ.random(rd.randint(5, 20), 2, 3, 3)

      m += len(b.nodes_not_io_ids)
      b.simplify()
      n += len(b.nodes_not_io_ids)
      b = False

      print(100*n/m)
    except:
      pass
  