from .base_critic import BaseCritic
import torch
import torch.optim as optim
from torch.nn import utils
from torch import nn
import pdb
import numpy as np

from cs224r.infrastructure import pytorch_util as ptu

class IQLCritic(BaseCritic):

    def __init__(self, hparams, optimizer_spec, **kwargs):
        super().__init__(**kwargs)
        self.env_name = hparams['env_name']
        self.ob_dim = hparams['ob_dim']

        if isinstance(self.ob_dim, int):
            self.input_shape = (self.ob_dim,)
        else:
            self.input_shape = hparams['input_shape']

        self.ac_dim = hparams['ac_dim']
        self.double_q = hparams['double_q']
        self.grad_norm_clipping = hparams['grad_norm_clipping']
        self.gamma = hparams['gamma']

        self.optimizer_spec = optimizer_spec
        network_initializer = hparams['q_func']
        self.q_net = network_initializer(self.ob_dim, self.ac_dim)
        self.q_net_target = network_initializer(self.ob_dim, self.ac_dim)

        self.optimizer = self.optimizer_spec.constructor(
            self.q_net.parameters(),
            **self.optimizer_spec.optim_kwargs
        )
        self.learning_rate_scheduler = optim.lr_scheduler.LambdaLR(
            self.optimizer,
            self.optimizer_spec.learning_rate_schedule,
        )
        self.mse_loss = nn.MSELoss()
        self.q_net.to(ptu.device)
        self.q_net_target.to(ptu.device)

        # TODO define value function
        # HINT: see Q_net definition above and optimizer below
        # HINT: Define using same hparams as Q_net, but adjust output dimensions
        ### YOUR CODE START HERE ###

        # q_net output q values of all actions.
        # v_net output 1 v value for status (aka ob)
        self.v_net = network_initializer(self.ob_dim, 1)

        ### YOUR CODE END HERE ###

        self.v_optimizer = self.optimizer_spec.constructor(
            self.v_net.parameters(),
            **self.optimizer_spec.optim_kwargs
        )
        
        self.v_learning_rate_scheduler = optim.lr_scheduler.LambdaLR(
            self.v_optimizer,
            self.optimizer_spec.learning_rate_schedule,
        )
        self.iql_expectile = hparams['iql_expectile']

    def expectile_loss(self, diff):
        # TODO: Implement the expectile loss given the difference between q and v
        # HINT: self.iql_expectile provides the \zeta value as described 
        # in the problem statement.
        ### YOUR CODE START HERE ###
        #pass

        # 这不是都补全了吗？

        # when diff > 0 zeta else abs(zeta-1). zeta belongs to (0,1), so abs(zeta-1) = 1-zeta
        weight = torch.where(diff > 0, ptu.from_numpy(np.array(self.iql_expectile)), ptu.from_numpy(np.array(1 -  self.iql_expectile)))
        return weight * (diff**2)
        ### YOUR CODE END HERE ###


    def update_v(self, ob_no, ac_na):
        """
        Update value function using expectile loss
        """
        ob_no = ptu.from_numpy(ob_no)
        ac_na = ptu.from_numpy(ac_na).to(torch.long)

        # TODO: Compute loss for v_net
        # HINT: use target q network to train V
        # HINT: Use self.expectile_loss as defined above, 
        # passing in the difference between the computed targets and predictions
        ### YOUR CODE START HERE ###
        value_loss = None

        assert len(ob_no.shape) == 2, f'ob_no.shape is {ob_no.shape}'
        batch_size, ob_dim = ob_no.shape

        ac_na = ac_na.unsqueeze(-1)
        assert len(ac_na.shape) == 2, f'ac_na.shape is {ac_na.shape}'
        assert ac_na.shape[0] == batch_size, f'ac_na.shape is {ac_na.shape}'
        assert ac_na.shape[1] == 1, f'ac_na.shape is {ac_na.shape}'

        computed_target = self.q_net_target.forward(ob_no) # (batch_size, action_dim)

        computed_target = computed_target.gather(1, ac_na)

        assert computed_target.shape == (batch_size, 1), f'computed_target.shape is {computed_target.shape}'

        prediction = self.v_net.forward(ob_no)

        assert prediction.shape == (batch_size, 1), f'prediction.shape is {prediction.shape}'

        value_loss = self.expectile_loss(prediction-computed_target)
        assert value_loss.shape == (batch_size, 1), f'value_loss.shape is {value_loss}'

        value_loss = value_loss.mean()

        ### YOUR CODE END HERE ###
        

        self.v_optimizer.zero_grad()
        value_loss.backward()
        utils.clip_grad_value_(self.v_net.parameters(), self.grad_norm_clipping)
        self.v_optimizer.step()
        
        self.v_learning_rate_scheduler.step()

        return {'Training V Loss': ptu.to_numpy(value_loss)}



    def update_q(self, ob_no, ac_na, next_ob_no, reward_n, terminal_n):
        """
        Use target v network to train Q
        """
        ob_no = ptu.from_numpy(ob_no)
        ac_na = ptu.from_numpy(ac_na).to(torch.long)
        next_ob_no = ptu.from_numpy(next_ob_no)
        reward_n = ptu.from_numpy(reward_n)
        terminal_n = ptu.from_numpy(terminal_n)
        
        
        # TODO: Compute loss for updating Q_net parameters
        # HINT: Note that if the next state is terminal, 
        # its target reward value needs to be adjusted.
        ### YOUR CODE START HERE ###
        loss = None

        assert len(ob_no.shape) == 2, f'ob_no.shape is {ob_no.shape}'
        batch_size, ob_dim = ob_no.shape

        assert next_ob_no.shape == ob_no.shape, f'next_ob_no.shape is {next_ob_no.shape}'

        reward_n = reward_n.unsqueeze(-1)
        assert reward_n.shape == (batch_size, 1), f'reward_n.shape is {reward_n.shape}'

        terminal_n = terminal_n.unsqueeze(-1)
        assert terminal_n.shape == (batch_size, 1), f'terminal_n.shape is {terminal_n.shape}'

        v_out = self.v_net.forward(next_ob_no)
        assert v_out.shape == (batch_size, 1), f'v_out.shape is {v_out.shape}'

        assert 0<= terminal_n.max() <= 1
        assert 0<= terminal_n.min() <= 1

        q_out = self.q_net.forward(ob_no) # (batch_size, action_dim)

        ac_na = ac_na.unsqueeze(-1)

        q_out = q_out.gather(1, ac_na)

        assert q_out.shape == (batch_size, 1), f'q_out.shape is {q_out.shape}'

        v_out *= 1 - terminal_n

        loss = (reward_n + self.gamma * v_out - q_out) ** 2

        loss = loss.mean()


        ### YOUR CODE END HERE ###
        self.optimizer.zero_grad()
        loss.backward()
        utils.clip_grad_value_(self.q_net.parameters(), self.grad_norm_clipping)
        self.optimizer.step()
        
        self.learning_rate_scheduler.step()

        return {'Training Q Loss': ptu.to_numpy(loss)}

    def update_target_network(self):
        for target_param, param in zip(
                self.q_net_target.parameters(), self.q_net.parameters()
        ):
            target_param.data.copy_(param.data)

    def qa_values(self, obs):
        obs = ptu.from_numpy(obs)
        qa_values = self.q_net(obs)
        return ptu.to_numpy(qa_values)
