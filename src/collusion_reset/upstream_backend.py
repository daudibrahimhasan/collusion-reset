"""Live adapter. Imported only on explicit opt-in; requires isolated dependencies."""

from copy import deepcopy
from dataclasses import asdict
import os
import sys
from uuid import uuid4
from unittest.mock import patch

from collusion_reset.episode_smoke import UPSTREAM, UPSTREAM_REVISION, check_upstream, live_command


class UpstreamBackend:
    mode = 'live-pilot-not-main-study'

    def __init__(self, model):
        if not model:
            raise ValueError('Select an explicit model before live execution')
        self.groq = None
        if model.startswith('groq/'):
            from collusion_reset.credentials import groq_settings
            self.groq = groq_settings(model)
        else:
            live_command(model, '.')  # Retain the OpenRouter free-route guard.
            if not os.environ.get('OPENROUTER_API_KEY'):
                raise ValueError('Set OPENROUTER_API_KEY securely in the environment')
        check_upstream()
        if str(UPSTREAM) not in sys.path:
            sys.path.insert(0, str(UPSTREAM))
        from experiments.models import AgentConfig, EpisodeRunConfig
        from experiments.prompts.system import initial_agent_messages
        from experiments.episode_runner import run_one_episode
        from experiments.memory.cross_episode import set_cross_episode_memory_from_results
        self.run_episode = run_one_episode
        self.memory = set_cross_episode_memory_from_results
        self.config_class = EpisodeRunConfig
        self.agent_configs = {a: AgentConfig(model=model, max_output_tokens=4096)
                              for a in ('alice', 'bob')}
        self.base = {a: initial_agent_messages(agent_id=a, max_rounds=5,
                                              reward_objective=True)
                     for a in ('alice', 'bob')}
        self.settings = {'model': model, 'upstream_revision': UPSTREAM_REVISION,
                         'agent_configs': {a: asdict(c) for a, c in self.agent_configs.items()},
                         'reward': True, 'reflection': True, 'verdict_review': True,
                         'max_rounds': 5, 'char_limit': 200, 'verdict_policy': 'raw-only',
                         'cross_episode_memory_scope': 'full-history'}
        self.invocation = uuid4().hex
        if self.groq:
            from collusion_reset.credentials import BoundedCompletion
            from experiments.agents import completion
            self.groq_completion = BoundedCompletion(completion, self.groq)
            self.settings.update(provider='groq', credential_slot=self.groq['slot'],
                                 max_requests=self.groq['max_requests'], account_fallback=False)

    def initial_state(self):
        return deepcopy(self.base)

    def restore_instructions(self, histories):
        for actor in self.base:
            if not histories[actor]:
                histories[actor] = deepcopy(self.base[actor])

    def episode(self, pair, histories, output, index):
        if any(task.get('task_type') != 'data_search' for task in pair):
            raise ValueError('Pilot permits SQLite data-search tasks only, no generated code execution')
        output.mkdir(parents=True, exist_ok=True)
        config = self.config_class(
            temp_run_id=f'cr_{self.invocation}_{output.name}', episode_index=index,
            usage_journal_path=output / 'usage.jsonl', usage_invocation_id=self.invocation)
        # Upstream normally drops old memory on context overflow. That would
        # silently change the intervention, so fail this trajectory instead.
        from contextlib import ExitStack
        with ExitStack() as stack:
            if self.groq:
                stack.enter_context(patch('experiments.agents.completion', self.groq_completion))
                stack.enter_context(patch('experiments.agents.LLM_MAX_RETRIES', 0))
            stack.enter_context(patch('experiments.episode_runner._drop_oldest_cross_episode_block',
                   side_effect=RuntimeError('Context overflow: history dropping forbidden')))
            result = self.run_episode(pair=pair, agent_configs=self.agent_configs,
                                      repo_root=UPSTREAM, config=config, agent_messages=histories)
        self.memory(histories, scope='full-history', episode_id=str(result['episode_id']),
                    max_memory_episodes_by_agent={'alice': -1, 'bob': -1})
        # Upstream result omits char_limit; retain the actual configured budget.
        result['char_limit'] = config.char_limit
        return result
