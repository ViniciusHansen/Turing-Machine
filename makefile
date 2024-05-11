# Makefile para converter arquivos Dinf_to_Sipser.py e Sipser_to_Dinf.py

all: sameamount10.out odd.out

sameamount10.out: sameamount10.in Dinf_to_Sipser.py
    python3 Dinf_to_Sipser.py sameamount10.in

odd.out: odd.in Sipser_to_Dinf.py
    python3 Sipser_to_Dinf.py odd.in

clean:
    rm -f sameamount10.out odd.out
