from board_position import Position

p = Position()
print(p.children)
print(p.p)

print('\n\n\n')
p.update_board("e2e4")
print(p.children)
print(p.p)

print('\n\n\n')
p.update_board("d7d5")
print(p.children)
print(p.p)
