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


### 0.2


Beginning logging procedure...
Timestep 22001
mean reward (100 episodes) -18.559999
best mean reward -17.590000
running time 4611.057512
Train_EnvstepsSoFar : 220010
Train_AverageReturn : -18.559999465942383
Train_BestReturn : -17.59000015258789
TimeSinceStart : 4611.057512044907
Exploration Critic Loss : 5.7921295166015625
Exploitation Critic V Loss : 0.16871193051338196
Exploitation Critic Q Loss : 0.4433915913105011
Exploration Model Loss : 0.04188370704650879
Actor Loss : 1.0934960842132568
Eval_AverageReturn : -22.25
Eval_StdReturn : 6.526606559753418
Eval_MaxReturn : -9.0
Eval_MinReturn : -35.0
Eval_AverageEpLen : 23.25
Buffer size : 22001
Done logging...


## 0.9