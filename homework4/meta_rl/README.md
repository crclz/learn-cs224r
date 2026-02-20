## Using Meta_RL Environment

Everything should already be installed on your AWS EC2 Instance if you used the given AMI.

All you need to do to be able to run the meta_rl folder's code is to switch to the meta_rl conda environment
```bash
conda deactivate
conda activatae meta_rl
```

## Run the Code

To run the DREAM code, invoke the following command:

```
python dream.py exp_name -b environment=\"map\"
```

This will create a directory `experiments/exp_name`, which will contain:

- A tensorboard subdirectory at `experiments/exp_name/tensorboard`, which logs
  statistics, such as accumulated returns vs. number of training episodes, and
  also vs. number of training steps.
- A visualization subdirectory at `experiments/exp_name/visualize`, which will
  contain videos of the learned agent.
- A checkpoints subdirectory at `experiments/exp_name/checkpoints`, which will
  periodically save model checkpoints.
- Metadata about the run, such as the configs used.

You can pass different values for `exp_name` as convenient.

To run the RL^2 code, similarly run:

```
python rl2.py exp_name -b environment=\"map\"
```

## answer

a What returns are achieved by only taking the move action to get to the goal, without riding any buses: i.e., directly walking to the goal?

4step -0.3 -0.3 -0.3 +1 = 0.1

b If the bus destinations (i.e., the problem ID) were known, what is the optimal returns that could be achieved in a single exploitation episode?

2step: 1. walk (-0.3) 2. teleport (+1) = 0.7

c Describe the exploration policy that discovers all of the bus destinations within the fewest number of timesteps.

walk right -> walk right (now on map, know all bus destinations)

d Given your answers in b and c, what is the optimal exploitation returns achievable by a meta-RL agent?

0.7


