#!/usr/bin/env python
import asyncio
import math
from naptha_sdk.task import Task as Agent
from naptha_sdk.utils import get_logger, load_yaml
import time

logger = get_logger(__name__)

async def run(inputs, worker_node_urls, *args, **kwargs):
    logger.info(f"Inputs: {inputs}")

    num_nodes = len(worker_node_urls)
    num_agents = inputs.num_agents
    agents_per_node = math.ceil(num_agents / num_nodes)

    ist = time.time()
    logger.info(f"Running {num_agents} agents...")
    tasks = []
    results = []
    for i in range(num_agents):
        node_index = min(i // agents_per_node, num_nodes - 1)
        name = f"Agent_{i}"
        agent = Agent(name=name, fn="random_number_agent", worker_node_url=worker_node_urls[node_index], *args, **kwargs)
        tasks.append(agent(agent_name=name))

    results = await asyncio.gather(*tasks)

    iet = time.time()
    logger.info(f"[Run time: {iet - ist} s]")

    logger.info(f"Results: {results}")

    return results 


if __name__ == "__main__":
    from keynesian_beauty_contest.schemas import InputSchema
    from naptha_sdk.schemas import AgentRunInput
    from naptha_sdk.client.node import Node

    cfg_path = "keynesian_beauty_contest/component.yaml"
    cfg = load_yaml(cfg_path)

    inputs = {
        "num_agents": 2,
    }
    agent_run = {"consumer_id": "user:18837f9faec9a02744d308f935f1b05e8ff2fc355172e875c24366491625d932f36b34a4fa80bac58db635d5eddc87659c2b3fa700a1775eb4c43da6b0ec270d", 
                "agent_name": "random_agent", "agent_source_url": "https://github.com/NapthaAI/keynesian_beauty_contest", "agent_version": "0.1", "worker_node_urls": ["http://localhost:7001"]} 
    agent_run = AgentRunInput(**agent_run)
    inputs = InputSchema(**inputs)
    orchestrator_node = Node("http://localhost:7001")
    worker_node_urls = agent_run.worker_node_urls

    response = asyncio.run(run(inputs, agent_run.worker_node_urls, orchestrator_node, agent_run, cfg))
    print(response)
    print("Agent Run: ", agent_run)