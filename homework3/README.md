## Setup

Create a new conda environment `cs224r` by running `./setup_env.sh`

Then run the following commands when you're under the `hw3/` folder.

```
conda activate cs224r
pip install -r requirements.txt
pip install -e .
```

## TODOs

The TODOs and descriptions for code that needs to be implemented has been provided in the homework PDF.


```bash
export PYTHONPATH="."

zeta=0.9

python cs224r/scripts/run_iql.py --env_name PointmassEasy-v0 \
--exp_name iql_zeta_${zeta}_rnd --use_rnd \
--num_exploration_steps=20000 \
--unsupervised_exploration \
--awac_lambda=1 \
--iql_expectile=${zeta}
```


## Runs

我要哈气了，开发机比apple M3慢10000倍.

```txt
Architecture:            x86_64
  CPU op-mode(s):        32-bit, 64-bit
  Address sizes:         40 bits physical, 57 bits virtual
  Byte Order:            Little Endian
CPU(s):                  32
  On-line CPU(s) list:   0-31
Vendor ID:               GenuineIntel
  Model name:            Intel(R) Xeon(R) Platinum 8336C CPU @ 2.30GHz
    CPU family:          6
    Model:               106
    Thread(s) per core:  1
    Core(s) per socket:  16
    Socket(s):           2
    Stepping:            6
    BogoMIPS:            4599.99
```


### 0.2

********** Iteration 49000 ************

Training agent...

Beginning logging procedure...
Timestep 49001
mean reward (100 episodes) -17.709999
best mean reward -16.930000
running time 771.871744
Train_EnvstepsSoFar : 490010
Train_AverageReturn : -17.709999084472656
Train_BestReturn : -16.93000030517578
TimeSinceStart : 771.8717439174652
Exploration Critic Loss : 504.2725830078125
Exploitation Critic V Loss : 0.1940365731716156
Exploitation Critic Q Loss : 1.477889895439148
Exploration Model Loss : 0.0224151611328125
Actor Loss : 0.8666563034057617
Eval_AverageReturn : -20.340425491333008
Eval_StdReturn : 5.886430263519287
Eval_MaxReturn : -12.0
Eval_MinReturn : -42.0
Eval_AverageEpLen : 21.340425531914892
Buffer size : 49001
Done logging...


## 0.9


********** Iteration 49000 ************

Training agent...

Beginning logging procedure...
Timestep 49001
mean reward (100 episodes) -18.400000
best mean reward -16.420000
running time 778.875578
Train_EnvstepsSoFar : 490010
Train_AverageReturn : -18.399999618530273
Train_BestReturn : -16.420000076293945
TimeSinceStart : 778.8755779266357
Exploration Critic Loss : 528.0133056640625
Exploitation Critic V Loss : 0.01745406538248062
Exploitation Critic Q Loss : 0.26605039834976196
Exploration Model Loss : 0.032958984375
Actor Loss : 0.8292597532272339
Eval_AverageReturn : -21.266666412353516
Eval_StdReturn : 6.935896873474121
Eval_MaxReturn : -10.0
Eval_MinReturn : -41.0
Eval_AverageEpLen : 22.266666666666666
Buffer size : 49001
Done logging...


感觉这个做得有点问题

## random

```
zeta=0.9

python cs224r/scripts/run_iql.py --env_name PointmassMedium-v0 \
--exp_name iql_zeta_${zeta}_random \
--num_exploration_steps=20000 \
--unsupervised_exploration \
--awac_lambda=1 \
--iql_expectile=${zeta}
```

********** Iteration 49000 ************

Training agent...

Beginning logging procedure...
Timestep 49001
mean reward (100 episodes) -38.029999
best mean reward -37.279999
running time 289.333076
Train_EnvstepsSoFar : 490010
Train_AverageReturn : -38.029998779296875
Train_BestReturn : -37.279998779296875
TimeSinceStart : 289.3330760002136
Exploration Critic Loss : 13.197015762329102
Exploitation Critic V Loss : 0.018704522401094437
Exploitation Critic Q Loss : 1.5630240440368652
Exploration Model Loss : 0.029388613998889923
Actor Loss : 1.3022501468658447
Eval_AverageReturn : -73.14286041259766
Eval_StdReturn : 31.222375869750977
Eval_MaxReturn : -25.0
Eval_MinReturn : -134.0
Eval_AverageEpLen : 74.14285714285714
Buffer size : 49001
Done logging...



## CQL

```bash
export PYTHONPATH="."

alpha=0.1 # 0, 0.1

python cs224r/scripts/run_cql.py --env_name PointmassHard-v0 \
--exp_name cql_alpha_${alpha}_rnd \
--use_rnd --unsupervised_exploration \
--offline_exploitation --cql_alpha=${alpha}

```


### aplha=0

********** Iteration 49000 ************

Training agent...

Beginning logging procedure...
Timestep 49001
mean reward (100 episodes) -57.950001
best mean reward -57.380001
running time 306.116581
Train_EnvstepsSoFar : 490010
Train_AverageReturn : -57.95000076293945
Train_BestReturn : -57.380001068115234
TimeSinceStart : 306.11658096313477
Exploration Critic Loss : 273.13916015625
Exploitation Critic Loss : 1.1551395654678345
Exploration Model Loss : 0.00994873046875
Exploitation Data q-values : -12.064812660217285
Exploitation OOD q-values : -11.483360290527344
Exploitation CQL Loss : 0.5814535617828369
Eval_AverageReturn : -58.117645263671875
Eval_StdReturn : 9.164396286010742
Eval_MaxReturn : -37.0
Eval_MinReturn : -80.0
Eval_AverageEpLen : 59.11764705882353
Buffer size : 10001
Done logging...


### alpha=0.1

********** Iteration 49000 ************

Training agent...

Beginning logging procedure...
Timestep 49001
mean reward (100 episodes) -58.950001
best mean reward -57.549999
running time 312.260257
Train_EnvstepsSoFar : 490010
Train_AverageReturn : -58.95000076293945
Train_BestReturn : -57.54999923706055
TimeSinceStart : 312.2602570056915
Exploration Critic Loss : 361.23126220703125
Exploitation Critic Loss : 1.0775182247161865
Exploration Model Loss : 0.033721923828125
Exploitation Data q-values : -11.529438972473145
Exploitation OOD q-values : -10.891311645507812
Exploitation CQL Loss : 0.6381275057792664
Eval_AverageReturn : -52.94736862182617
Eval_StdReturn : 12.377711296081543
Eval_MaxReturn : -41.0
Eval_MinReturn : -96.0
Eval_AverageEpLen : 53.94736842105263
Buffer size : 10001
Done logging...


### replace rnd by random

python cs224r/scripts/run_cql.py --env_name PointmassHard-v0 \
--exp_name cql_alpha_0.1_random \
--unsupervised_exploration \
--offline_exploitation --cql_alpha=0.1


********** Iteration 49000 ************

Training agent...

Beginning logging procedure...
Timestep 49001
mean reward (100 episodes) -57.070000
best mean reward -57.070000
running time 279.465715
Train_EnvstepsSoFar : 490010
Train_AverageReturn : -57.06999969482422
Train_BestReturn : -57.06999969482422
TimeSinceStart : 279.46571493148804
Exploration Critic Loss : 116.45223999023438
Exploitation Critic Loss : 0.920289158821106
Exploration Model Loss : 0.0730438232421875
Exploitation Data q-values : -12.949750900268555
Exploitation OOD q-values : -12.423408508300781
Exploitation CQL Loss : 0.5263423919677734
Eval_AverageReturn : -59.882354736328125
Eval_StdReturn : 16.222288131713867
Eval_MaxReturn : -37.0
Eval_MinReturn : -100.0
Eval_AverageEpLen : 60.8235294117647
Buffer size : 10001
Done logging...
