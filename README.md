# calculating probability of various game..

## calc_win_percent_texas_holdem_poker.py

calc approximately texas holdem poker winner percent by simulation...
```
0 [7♠, J♠] : 2.90 %
1 [A♦, A♥] : 2.90 %
2 [10♠, 2♠] : 2.50 %
3 [Q♥, 8♥] : 85.00 %
4 [3♣, 5♦] : 6.70 %

shared cards: [9♣, J♥, 10♣]

example game:

shared cards: [9♣, J♥, 10♣, 8♦, 8♣] 

(3, 'straight', [Q♥, J♥, 10♣, 9♣, 8♥], [], 6, 2, 0)
(0, 'straight', [J♠, 10♣, 9♣, 8♦, 7♠], [], 6, 3, 0)
(1, 'two pair', [A♦, A♥], [8♦, 8♣], 8, 0, 6)
(2, 'two pair', [10♠, 10♣], [8♦, 8♣], 8, 4, 6)
(4, 'pair', [8♦, 8♣], [], 9, 6, 0)
```

##calc_win_percent_tienlen.py

https://vi.wikipedia.org/wiki/B%C3%A0i_Ti%E1%BA%BFn_l%C3%AAn

tính toán chính xác % bị/ko bị chặt cho từng bộ
