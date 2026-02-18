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

zeta=0.2
python cs224r/scripts/run_iql.py --env_name PointmassEasy-v0 \
--exp_name iql_zeta_${zeta}_rnd --use_rnd \
--num_exploration_steps=20000 \
--unsupervised_exploration \
--awac_lambda=1 \
--iql_expectile=${zeta}
```