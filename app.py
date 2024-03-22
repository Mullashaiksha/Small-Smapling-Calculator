import streamlit as st
import numpy as np
from scipy.stats import norm

def fun(p, n, k):
    zp = norm.ppf(1 - (p / 2))
    m = np.sqrt((2 * n) / (2 + k**2)) * (zp - k)
    pac = (2 * norm.cdf(m) - 1)
    asnc = n
    return pac, asnc

def calculate(p1, p2, p3):
    alpha = 0.05
    beta = 0.1
    asn1min = 10000
    asn2min = 10000
    asn3min = 10000
    nmin = 10000
    kmin = 3.50
    pa1min = 1
    pa2min = 1
    N = 1000
    Ci = 10.0
    Cf = 20.0
    C0 = 50.0
    Ddmin = 500
    Dnmin = 500
    TCmin = 5000
    pa3min = 1
    atimin = 1000
    AOQmin = 1

    for n in range(2, 1001):
        for k in np.arange(0.1, 4.6, 0.1):
            p = p1
            list1 = fun(p, n, k)
            pa1, asn1 = list1
            if pa1 >= 1 - alpha:
                p = p2
                list2 = fun(p, n, k)
                pa2, asn2 = list2
                if pa1 >= 1 - alpha and pa2 > 0 and pa2 <= beta:
                    p = p3
                    pa3, asn3 = fun(p, n, k)
                    AOQ = (p / 2) * pa3
                    ati = n + (1 - pa3) * (N - n)
                    Dd = (p / 2) * asn3 + (p / 2) * (1 - pa3) * (N - asn3)
                    Dn = (p / 2) * pa3 * (N - asn3)
                    TC = Ci * ati + Cf * Dd + C0 * Dn
                    if TC <= TCmin:
                        asn1min = asn1
                        asn2min = asn2
                        asn3min = asn3
                        nmin = n
                        kmin = k
                        pa1min = pa1
                        pa2min = pa2
                        TCmin = TC
                        pa3min = pa3
                        Ddmin = Dd
                        Dnmin = Dn
                        atimin = ati
                        AOQmin = AOQ

    output_text = f"Minimum values:\n nmin: {nmin}\n kmin: {kmin}\n pa1min: {pa1min}\n pa2min: {pa2min}\n"
    output_text += f"pa3min: {pa3min}\n atimin: {atimin}\n Ddmin: {Ddmin}\n Dnmin: {Dnmin}\n AOQmin: {AOQmin}\n TCmin: {TCmin}"
    return output_text

st.title('Small Sampling Calculator')

p1 = st.text_input('Value for p1:')
p2 = st.text_input('Value for p2:')
p3 = st.text_input('Value for p3:')
if st.button('Calculate'):
    try:
        p1 = float(p1)
        p2 = float(p2)
        p3 = float(p3)
        result = calculate(p1, p2, p3)
        st.write(result)
    except ValueError:
        st.error("Please enter valid numeric inputs.")
