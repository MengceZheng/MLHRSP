# Improved Lattice-Based Attack on Mersenne Low Hamming Ratio Search Problem

## Introduction

This is a Python implementation of lattice-based attacks proposed in **Improved Lattice-Based Attack on Mersenne Low Hamming Ratio Search Problem**[^MLHRSP]. Some underlying functions are based on [Joachim Vandersmissen's crypto-attacks](https://github.com/jvdsn/crypto-attacks).

## Requirements

* [SageMath](https://www.sagemath.org/) with Python 3.9
* [PyCryptodome](https://pycryptodome.readthedocs.io/)

You can check your SageMath Python version using the following command:

```commandline
$ sage -python --version
Python 3.9.0
```

Note: If your SageMath Python version is older than 3.9.0, some features in given scripts might not work.

## Usage

To run this attack, you can simply execute the Python file **attack.py** with Sage using `sage -python attack.py` and then input several specific attack parameters:

```commandline
MLHRSP$ sage -python attack.py
PARI stack size set to 10000000000 bytes, maximum size set to 10000003072
Example Mersenne n: [521, 607, 1279, 2203, 2281, 3217, 4253, 4423, 9689, 9941, 11213, 19937, 21701, 23209, 44497, 86243, 110503, 132049, 216091, 756839]...
Input n (choosing from aboves): 521
Input w (satisfying 4*w^2 < n): 10
Input xi1 (0 to 1 & xi1+xi2=1): 0.5
Input xi2 (0 to 1 & xi1+xi2=1): 0.5
Input s (controlling lattices): 5
Input test times (for attacks): 5
Input type (basic or improved): basic
INFO:root:Test with n=521, w=10, xi1=0.5, xi2=0.5, and s=5 for 5 times:
INFO:root:Generating MLHRSP instance with 521-bit modulus p, 260-bit f, 260-bit g and Hamming weight 10...
INFO:root:Using basic solving strategy to find roots...
INFO:root:Trying s = 5...
INFO:root:Reducing a 21 x 21 lattice within 0.079 seconds...
INFO:root:Finding roots within 0.000 seconds...
INFO:root:Succeeded!
INFO:root:Found f = 926336713898634875680236437361794674151001286193830348763523916265255528824840
INFO:root:Found g = 926338480745594341772898995862544871634225261713857313472454401252981395685379
INFO:root:Generating MLHRSP instance with 521-bit modulus p, 260-bit f, 260-bit g and Hamming weight 10...
INFO:root:Using basic solving strategy to find roots...
INFO:root:Trying s = 5...
INFO:root:Reducing a 21 x 21 lattice within 0.051 seconds...
INFO:root:Finding roots within 0.000 seconds...
INFO:root:Succeeded!
INFO:root:Found f = 926336713898529563388568263196311482671038923649514732027271815275120074686976
INFO:root:Found g = 926336713912852035055491657460420203794119850253128016234908063976172787073025
INFO:root:Generating MLHRSP instance with 521-bit modulus p, 260-bit f, 260-bit g and Hamming weight 10...
INFO:root:Using basic solving strategy to find roots...
INFO:root:Trying s = 5...
INFO:root:Reducing a 21 x 21 lattice within 0.052 seconds...
INFO:root:Finding roots within 0.000 seconds...
INFO:root:Succeeded!
INFO:root:Found f = 926336713898529565022183606703886931625493885463816631238355717979455759581184
INFO:root:Found g = 926336934754412763530864589915683929191497883759871547054748028521108136296449
INFO:root:Generating MLHRSP instance with 521-bit modulus p, 260-bit f, 260-bit g and Hamming weight 10...
INFO:root:Using basic solving strategy to find roots...
INFO:root:Trying s = 5...
INFO:root:Reducing a 21 x 21 lattice within 0.052 seconds...
INFO:root:Finding roots within 0.000 seconds...
INFO:root:Succeeded!
INFO:root:Found f = 926450012966558477284094727880211488005268704440307504040639856421053841539088
INFO:root:Found g = 926337597322904450914081129211836978506887486832623057117330798452425248735233
INFO:root:Generating MLHRSP instance with 521-bit modulus p, 260-bit f, 260-bit g and Hamming weight 10...
INFO:root:Using basic solving strategy to find roots...
INFO:root:Trying s = 5...
INFO:root:Reducing a 21 x 21 lattice within 0.050 seconds...
INFO:root:Finding roots within 0.000 seconds...
INFO:root:Succeeded!
INFO:root:Found f = 926393253004603088751323541041795698827495227736026017295914512722972056290304
INFO:root:Found g = 926336741512254937217611456004964255463049535964482876580789698582005466267665
INFO:root:Success rate for n=521, w=10, xi1=0.5, xi2=0.5 using s=5 and basic strategy is 100.0%...
INFO:root:Average time is 0.169 seconds...
```

```commandline
MLHRSP$ sage -python attack.py
PARI stack size set to 10000000000 bytes, maximum size set to 10000003072
Example Mersenne n: [521, 607, 1279, 2203, 2281, 3217, 4253, 4423, 9689, 9941, 11213, 19937, 21701, 23209, 44497, 86243, 110503, 132049, 216091, 756839]...
Input n (choosing from aboves): 521
Input w (satisfying 4*w^2 < n): 10
Input xi1 (0 to 1 & xi1+xi2=1): 0.3
Input xi2 (0 to 1 & xi1+xi2=1): 0.7
Input s (controlling lattices): 7
Input test times (for attacks): 3
Input type (basic or improved): improved
INFO:root:Test with n=521, w=10, xi1=0.3, xi2=0.7, and s=7 for 3 times:
INFO:root:Generating MLHRSP instance with 521-bit modulus p, 156-bit f, 364-bit g and Hamming weight 10...
INFO:root:Using improved solving strategy to find roots...
INFO:root:Trying s = 7...
INFO:root:Reducing a 8 x 8 lattice within 0.033 seconds...
INFO:root:Finding roots within 0.000 seconds...
INFO:root:Succeeded!
INFO:root:Found f = 48526432441121454175749111031617524045822566464
INFO:root:Found g = 18788340662190665823115876099850597832897883632936986719934449872162903054289913777596587317236935053593804801
INFO:root:Generating MLHRSP instance with 521-bit modulus p, 156-bit f, 364-bit g and Hamming weight 10...
INFO:root:Using improved solving strategy to find roots...
INFO:root:Trying s = 7...
INFO:root:Reducing a 8 x 8 lattice within 0.027 seconds...
INFO:root:Finding roots within 0.000 seconds...
INFO:root:Succeeded!
INFO:root:Found f = 45672037779207066301295286054542485921038602240
INFO:root:Found g = 18861732622276849626238566134412922215936455230726383977147125062292663790599335652739279851997844454225477633
INFO:root:Generating MLHRSP instance with 521-bit modulus p, 156-bit f, 364-bit g and Hamming weight 10...
INFO:root:Using improved solving strategy to find roots...
INFO:root:Trying s = 7...
INFO:root:Reducing a 8 x 8 lattice within 0.026 seconds...
INFO:root:Finding roots within 0.000 seconds...
INFO:root:Succeeded!
INFO:root:Found f = 46396787499491077238669144926754931188850229248
INFO:root:Found g = 21136883244964499051005325371133704969248205215252168901274100866183830983213719200450150709293679053071450145
INFO:root:Success rate for n=521, w=10, xi1=0.3, xi2=0.7 using s=7 and improved strategy is 100.0%...
INFO:root:Average time is 0.177 seconds...
```

An alternative way to run the attack with the specific parameters n, h, xi1, xi2, s, and others requires passing them as command line arguments. For instance, to run the attack with n = 521, h = 10, xi1 = 0.5, xi2 = 0.5, and s = 5, please run `sage -python attack.py 521 10 0.5 0.5 5`:

```commandline
MLHRSP$ sage -python attack.py 521 10 0.5 0.5 5
PARI stack size set to 10000000000 bytes, maximum size set to 10000003072
INFO:root:Test with n=521, w=10, xi1=0.5, xi2=0.5, and s=5 for 5 times:
INFO:root:Generating MLHRSP instance with 521-bit modulus p, 260-bit f, 260-bit g and Hamming weight 10...
INFO:root:Using basic solving strategy to find roots...
INFO:root:Trying s = 5...
INFO:root:Reducing a 21 x 21 lattice within 0.058 seconds...
INFO:root:Finding roots within 0.000 seconds...
INFO:root:Succeeded!
INFO:root:Found f = 926337155664215651322090106350908675000927977082902916196176182944572018524164
INFO:root:Found g = 926336713898529563388567880817792101139624789818026156484183878349993264807937
INFO:root:Generating MLHRSP instance with 521-bit modulus p, 260-bit f, 260-bit g and Hamming weight 10...
INFO:root:Using basic solving strategy to find roots...
INFO:root:Trying s = 5...
INFO:root:Reducing a 21 x 21 lattice within 0.051 seconds...
INFO:root:Finding roots within 0.000 seconds...
INFO:root:Succeeded!
INFO:root:Found f = 955284736211228605577854647857951581723470369200818808324368440686374169870336
INFO:root:Found g = 985138267637886583069264812542977962492496737603144125929496844111732235305473
INFO:root:Generating MLHRSP instance with 521-bit modulus p, 260-bit f, 260-bit g and Hamming weight 10...
INFO:root:Using basic solving strategy to find roots...
INFO:root:Trying s = 5...
INFO:root:Reducing a 21 x 21 lattice within 0.051 seconds...
INFO:root:Finding roots within 0.000 seconds...
INFO:root:Succeeded!
INFO:root:Found f = 926336713898529563388620080701787010440399838592029152189084298644786394431488
INFO:root:Found g = 926336713898529563388567880069503263523399111923652243848938022605144207654913
INFO:root:Generating MLHRSP instance with 521-bit modulus p, 260-bit f, 260-bit g and Hamming weight 10...
INFO:root:Using basic solving strategy to find roots...
INFO:root:Trying s = 5...
INFO:root:Reducing a 21 x 21 lattice within 0.049 seconds...
INFO:root:Finding roots within 0.000 seconds...
INFO:root:Succeeded!
INFO:root:Found f = 926393253004604117191684126759896118300079735013880050245871189215030005465088
INFO:root:Found g = 926338481608733884288490245257757004774667537492300052827113262116955026882563
INFO:root:Generating MLHRSP instance with 521-bit modulus p, 260-bit f, 260-bit g and Hamming weight 10...
INFO:root:Using basic solving strategy to find roots...
INFO:root:Trying s = 5...
INFO:root:Reducing a 21 x 21 lattice within 0.053 seconds...
INFO:root:Finding roots within 0.000 seconds...
INFO:root:Succeeded!
INFO:root:Found f = 1391314322242127410636737435603477310347197530242133804014907120671150298890256
INFO:root:Found g = 926336713912009536722143200013604825551851736023049406635071753628755068715013
INFO:root:Success rate for n=521, w=10, xi1=0.5, xi2=0.5 using s=5 and basic strategy is 100.0%...
INFO:root:Average time is 0.157 seconds...
```

Additionally, to run the attack with n = 521, h = 10, xi1 = 0.75, xi2 = 0.25, and s = 5 for 3 times using improved strategy, please run `sage -python attack.py 521 10 0.75 0.25 5 3 improved`:

```commandline
MLHRSP$ sage -python attack.py 521 10 0.75 0.25 5 3 improved
PARI stack size set to 10000000000 bytes, maximum size set to 10000003072
INFO:root:Test with n=521, w=10, xi1=0.75, xi2=0.25, and s=5 for 3 times:
INFO:root:Generating MLHRSP instance with 521-bit modulus p, 390-bit f, 130-bit g and Hamming weight 10...
INFO:root:Using improved solving strategy to find roots...
INFO:root:Trying s = 5...
INFO:root:Reducing a 6 x 6 lattice within 0.013 seconds...
INFO:root:Finding roots within 0.000 seconds...
INFO:root:Succeeded!
INFO:root:Found f = 1260864198293797329257958149435360564716950360583523591289631983025953901788957625605228674755653089512437093454839808
INFO:root:Found g = 680897203100264399019806165366764208193
INFO:root:Generating MLHRSP instance with 521-bit modulus p, 390-bit f, 130-bit g and Hamming weight 10...
INFO:root:Using improved solving strategy to find roots...
INFO:root:Trying s = 5...
INFO:root:Reducing a 6 x 6 lattice within 0.006 seconds...
INFO:root:Finding roots within 0.000 seconds...
INFO:root:Succeeded!
INFO:root:Found f = 1891296297427239607474396856792919791401302680966706639721448869353743800698006460457724564297257443877427334520766464
INFO:root:Found g = 680897040840861841540807003941225103361
INFO:root:Generating MLHRSP instance with 521-bit modulus p, 390-bit f, 130-bit g and Hamming weight 10...
INFO:root:Using improved solving strategy to find roots...
INFO:root:Trying s = 5...
INFO:root:Reducing a 6 x 6 lattice within 0.005 seconds...
INFO:root:Finding roots within 0.000 seconds...
INFO:root:Succeeded!
INFO:root:Found f = 1260864199462334900350839703849931270658887553460852591892347044353192867230256492914459385541153858532085992152629248
INFO:root:Found g = 680575118438070178892031940063824707733
INFO:root:Success rate for n=521, w=10, xi1=0.75, xi2=0.25 using s=5 and improved strategy is 100.0%...
INFO:root:Average time is 0.114 seconds...
```

[^MLHRSP]: Zheng M., Yan W., "Improved Lattice-Based Attack on Mersenne Low Hamming Ratio Search Problem"
