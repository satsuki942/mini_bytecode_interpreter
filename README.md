命令セットを絞ったByteCodeインタープリター

命令セット：

コマンド：

fib-program
```
PUSH 10     # fib(n)
SAVE 1      # nをレジスタ上に登録
PUSH 0      # fib(n-1)とfib(n-2)の初期値
PUSH 1      #
SAVE 10     # fib(n-1)とfib(n-2)の初期値を登録
SAVE 9
LOAD 1      # nをレジスタ上からロード
PUSH 1      # n == 1を判定
EQ
JMP_IF 23   # n == 1ならプログラムを終了
LOAD 1      # nをレジスタ上からロード
PUSH -1     # n -= 1をする
ADD
SAVE 1      # n-1をレジスタ上に登録
LOAD 9      # fib(n-1)とfib(n-2)の値をロード
LOAD 10
ADD         # fib(n)の値を計算
SAVE 9      # fib(n)の値を登録
LOAD 9      # fib(n)とfib(n-1)のレジスタ上の値を交換
LOAD 10
SAVE 9
SAVE 10
JMP 6       # 再帰ポイントにジャンプ
LOAD 10     # fib(n)の返り値をロード
PRINT
HALT
```

fib-w-si-program
```
PUSH 10     # fib(n)
SAVE 1      # nをレジスタ上に登録
PUSH 0      # fib(n-1)とfib(n-2)の初期値
PUSH 1      #
SAVE 10     # fib(n-1)とfib(n-2)の初期値を登録
SAVE 9
LOAD 1      # nをレジスタ上からロード
PUSH 1      # n == 1を判定
EQ
JMP_IF 20   # n == 1ならプログラムを終了
LOAD 1      # nをレジスタ上からロード
PUSH -1     # n -= 1をする
ADD
SAVE 1      # n-1をレジスタ上に登録
LOAD 9      # fib(n-1)とfib(n-2)の値をロード
LOAD 10
ADD         # fib(n)の値を計算
SAVE 9      # fib(n)の値を登録
SWAP 9 10   # fib(n)とfib(n-1)のレジスタ上の値を交換
JMP 6       # 再帰ポイントにジャンプ
LOAD 10     # fib(n)の返り値をロード
PRINT
HALT
```