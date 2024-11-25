#!/usr/bin/env python
import asyncio
import math
import logging
import time
from naptha_sdk.agent import Agent
from naptha_sdk.schemas import OrchestratorRunInput


logger = logging.getLogger(__name__)

async def run(orchestrator_run: OrchestratorRunInput, *args, **kwargs):
    logger.info(f"Inputs: {orchestrator_run.inputs}")

    num_nodes = len(orchestrator_run.agent_deployments)
    num_agents = int(orchestrator_run.inputs.num_agents)
    agents_per_node = math.ceil(num_agents / num_nodes)

    ist = time.time()
    logger.info(f"Running {num_agents} agents...")
    tasks = []
    results = []
    for i in range(num_agents):
        node_index = min(i // agents_per_node, num_nodes - 1)
        name = f"Agent_{i}"
        agent = Agent(
            orchestrator_run = orchestrator_run,
            agent_index = node_index,
            *args,
            **kwargs
        )
        tasks.append(agent.call_agent_func(agent_name=name))

    results = await asyncio.gather(*tasks)

    iet = time.time()
    logger.info(f"[Run time: {iet - ist} s]")

    logger.info(f"Results: {results}")

    results = [result.results[0] for result in results]

    logger.info(f"Final results: {results}")

    return results