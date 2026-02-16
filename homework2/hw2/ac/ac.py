import hydra
import numpy as np
import random
import torch
import torch.nn as nn
import torch.nn.functional as F

import utils


class Actor(nn.Module):
    def __init__(self, obs_shape, action_shape, hidden_dim, std=0.1):
        super().__init__()

        self.std = std
        self.policy = nn.Sequential(nn.Linear(obs_shape[0], hidden_dim),
                                    nn.ReLU(inplace=True),
                                    nn.Linear(hidden_dim, hidden_dim),
                                    nn.ReLU(inplace=True),
                                    nn.Linear(hidden_dim, action_shape[0]))

        self.apply(utils.weight_init)

    def forward(self, obs):
        mu = self.policy(obs)
        mu = torch.tanh(mu)
        std = torch.ones_like(mu) * self.std

        dist = utils.TruncatedNormal(mu, std)
        return dist


class Critic(nn.Module):
    def __init__(self, obs_shape, action_shape, num_critics,
                 hidden_dim):
        super().__init__()

        self.critics = nn.ModuleList([nn.Sequential(
            nn.Linear(obs_shape[0] + action_shape[0], hidden_dim), nn.LayerNorm(hidden_dim),
            nn.ReLU(inplace=True), nn.Linear(hidden_dim, hidden_dim), nn.LayerNorm(hidden_dim),
            nn.ReLU(inplace=True), nn.Linear(hidden_dim, 1))
            for _ in range(num_critics)])

        self.apply(utils.weight_init)

    def forward(self, obs, action):
        h_action = torch.cat([obs, action], dim=-1)
        return [critic(h_action) for critic in self.critics]


class ACAgent:
    def __init__(self, obs_shape, action_shape, device, lr,
                 hidden_dim, num_critics, critic_target_tau, stddev_clip, use_tb):
        self.device = device
        self.critic_target_tau = critic_target_tau
        self.use_tb = use_tb
        self.stddev_clip = stddev_clip

        # models
        self.actor = Actor(obs_shape, action_shape,
                           hidden_dim).to(device)

        self.critic = Critic(obs_shape, action_shape,
                             num_critics, hidden_dim).to(device)
        self.critic_target = Critic(obs_shape, action_shape,
                                    num_critics, hidden_dim).to(device)
        self.critic_target.load_state_dict(self.critic.state_dict())

        # optimizers
        self.actor_opt = torch.optim.Adam(self.actor.parameters(), lr=lr)
        self.critic_opt = torch.optim.Adam(self.critic.parameters(), lr=lr)

        self.train()
        self.critic_target.train()

    def train(self, training=True):
        self.training = training
        self.actor.train(training)
        self.critic.train(training)

    def act(self, obs, eval_mode):
        obs = torch.as_tensor(obs, device=self.device)
        dist = self.actor(obs.unsqueeze(0))
        if eval_mode:
            action = dist.mean
        else:
            action = dist.sample(clip=None)
        return action.cpu().numpy()[0]

    def update_critic(self, replay_iter):
        '''
        This function updates the critic and target critic parameters.

        Args:

        replay_iter:
            An iterable that produces batches of tuples
            (observation, action, reward, discount, next_observation),
            where:
            observation: array of shape [batch, D] of states
            action: array of shape [batch, action_dim]
            reward: array of shape [batch,]
            discount: array of shape [batch,]
            next_observation: array of shape [batch, D] of states

        Returns:

        metrics: dictionary of relevant metrics to be logged. Add any metrics
                 that you find helpful to log for debugging, such as the critic
                 loss, or the mean Bellman targets.
        '''

        metrics = dict()

        batch = next(replay_iter)
        obs, action, reward, discount, next_obs = utils.to_torch(
            batch, self.device)

        ### YOUR CODE HERE ###

        next_action = self.act(next_obs, False) + discount

        # run target critic nets to calculate Q
        target_critic_outputs = self.critic_target.forward(next_obs, next_action)
        sample_two = random.choices(target_critic_outputs, k=2)
        min_critic = min([p for p in sample_two]).item

        y = reward + discount * min_critic

        # compute the loss
        critic_outputs = self.critic.forward(next_obs, next_action)

        loss = torch.zeros(1)
        for critic_out in critic_outputs:
            sg_y = y.item() # do not send Q's gradient back to target critic
            loss += (critic_out - sg_y)**2

        # d: take gradient step
        self.critic_opt.zero_grad()
        loss.backward()
        self.critic_opt.step()

        # e: Update the target critic parameters, soft
        # self.critic: 在 update_critic 中主要被使用
        # self.critic_target: 用于估计Q值的，在训练actor时被使用
        utils.soft_update_params(self.critic, self.critic_target, self.critic_target_tau)


        #####################
        return metrics

    def update_actor(self, replay_iter):
        '''
        This function updates the policy parameters.

        Args:

        replay_iter:
            An iterable that produces batches of tuples
            (observation, action, reward, discount, next_observation),
            where:
            observation: array of shape [batch, D] of states
            action: array of shape [batch, action_dim]
            reward: array of shape [batch,]
            discount: array of shape [batch,]
            next_observation: array of shape [batch, D] of states

        Returns:

        metrics: dictionary of relevant metrics to be logged. Add any metrics
                 that you find helpful to log for debugging, such as the actor
                 loss.
        '''
        metrics = dict()

        batch = next(replay_iter)
        obs, _, _, _, _ = utils.to_torch(
            batch, self.device)

        ### YOUR CODE HERE ###

        assert len(obs.shape) == 2

        actions = self.actor.forward(obs)

        q_values = self.critic.forward(obs, actions)

        loss = - sum(q_values) / len(q_values)

        metrics["loss"] = loss.item()

        self.actor_opt.zero_grad()
        loss.backward()
        self.actor_opt.step()


        return metrics

    def bc(self, replay_iter):
        '''
        This function updates the policy with end-to-end
        behavior cloning

        Args:

        replay_iter:
            An iterable that produces batches of tuples
            (observation, action, reward, discount, next_observation),
            where:
            observation: array of shape [batch, D] of states
            action: array of shape [batch, action_dim]
            reward: array of shape [batch,]
            discount: array of shape [batch,]
            next_observation: array of shape [batch, D] of states

        Returns:

        metrics: dictionary of relevant metrics to be logged. Add any metrics
                 that you find helpful to log for debugging, such as the loss.
        '''

        metrics = dict()

        batch = next(replay_iter)
        obs, action, _, _, _ = utils.to_torch(batch, self.device)

        ### YOUR CODE HERE ###

        assert len(obs.shape) == 2 # (batch, D)

        dist = self.actor(obs)

        loss = -dist.log_prob(action)

        metrics["loss"] = loss.item()

        self.actor_opt.zero_grad()
        loss.backward()
        self.actor_opt.step()


        return metrics
