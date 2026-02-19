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
